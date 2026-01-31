import sys
import os
from rich.console import Console
from rich.panel import Panel
import questionary
from core.loader import DatasetLoader
from core.inspector import DatasetInspector
from core.processor import DataProcessor
from core.exporter import DataExporter

console = Console()

def main():
    console.print(Panel(
        "[bold green]DataExtractor Pro[/bold green]\n[italic]HF Dataset Multi-Formatter[/italic]",
        border_style="green",
        title="v1.0.0",
        expand=False
    ))

    # 1. Get Dataset ID
    dataset_id = questionary.text(
        "Enter HuggingFace Dataset ID (e.g., 'tatsu-lab/alpaca' or URL):"
    ).ask()

    if not dataset_id:
        return

    # Extract ID from URL if necessary
    if "huggingface.co/datasets/" in dataset_id:
        dataset_id = dataset_id.split("huggingface.co/datasets/")[-1].split("?")[0]

    loader = DatasetLoader()
    inspector = DatasetInspector()

    # 2. Check Access & Auth
    with console.status("[bold green]Checking dataset access...") as status:
        try:
            has_access, is_private = loader.check_access(dataset_id)
        except Exception as e:
            console.print(f"[red]Error checking dataset:[/red] {e}")
            return

    if not has_access:
        console.print("[yellow]Authentication required for this dataset.[/yellow]")
        token = questionary.password("Enter your HuggingFace Access Token:").ask()
        if not loader.authenticate(token):
            console.print("[red]Authentication failed![/red]")
            return

    # 3. Load Configurations & Splits
    configs = loader.get_configs(dataset_id)
    config_name = "default"
    if len(configs) > 1:
        config_name = questionary.select(
            "Select dataset configuration:",
            choices=configs
        ).ask()
    
    splits = loader.get_splits(dataset_id, config=config_name)
    split_name = splits[0]
    if len(splits) > 1:
        split_name = questionary.select(
            "Select dataset split:",
            choices=splits
        ).ask()

    # 4. Inspect Structure
    with console.status(f"[bold green]Loading schema for {dataset_id} [{config_name}/{split_name}]...") as status:
        ds = loader.load(dataset_id, config=config_name, split=split_name, streaming=True)
        sample = inspector.get_sample(ds, n=5)
        hierarchy = inspector.analyze_hierarchy(sample)

    inspector.display_structure(hierarchy)

    # 5. Field Selection
    available_fields = list(hierarchy.keys())
    selected_fields = questionary.checkbox(
        "Select fields to extract:",
        choices=available_fields
    ).ask()

    if not selected_fields:
        console.print("[yellow]No fields selected. Exiting.[/yellow]")
        return

    # Renaming (Optional move to more intuitive flow later)
    fields_map = {f: f for f in selected_fields}
    if questionary.confirm("Do you want to rename any fields?").ask():
        for f in selected_fields:
            new_name = questionary.text(f"Rename '{f}' to:", default=f).ask()
            fields_map[f] = new_name

    # 6. Export Format
    out_format = questionary.select(
        "Select output format:",
        choices=["JSONL", "CSV"]
    ).ask()

    output_filename = f"extracted_{dataset_id.replace('/', '_')}.{out_format.lower()}"
    output_path = questionary.text(
        "Enter output file path:",
        default=os.path.join("data", output_filename)
    ).ask()

    # 7. Execution
    processor = DataProcessor()
    exporter = DataExporter()

    console.print(f"\n[bold green]Extracting data to {output_path}...[/bold green]")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    extracted_iter = processor.extract_fields(ds, fields_map)
    
    try:
        if out_format == "JSONL":
            exporter.to_jsonl(extracted_iter, output_path)
        else:
            exporter.to_csv(extracted_iter, output_path)
        
        console.print(f"\n[bold blue]Success![/bold blue] Dataset saved to [underline]{output_path}[/underline]")
    except Exception as e:
        console.print(f"[red]Export failed:[/red] {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        sys.exit(0)
