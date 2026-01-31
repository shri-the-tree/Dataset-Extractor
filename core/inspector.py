from rich.table import Table
from rich.console import Console

class DatasetInspector:
    def __init__(self):
        self.console = Console()

    def inspect_schema(self, dataset):
        """Get the fields and types from the dataset features"""
        # Take a peek at initial features
        if hasattr(dataset, "features"):
            return dataset.features
        return {}

    def get_sample(self, dataset, n=5):
        """Get a small sample for structure analysis"""
        sample = []
        try:
            # For iterable datasets
            it = iter(dataset)
            for _ in range(n):
                sample.append(next(it))
        except StopIteration:
            pass
        return sample

    def analyze_hierarchy(self, sample):
        """Recursively analyze nested structures in a sample"""
        hierarchy = {}
        if not sample:
            return hierarchy

        # Analyze the first row as a representative
        row = sample[0]
        for key, value in row.items():
            hierarchy[key] = self._detect_type(value)
        
        return hierarchy

    def _detect_type(self, value):
        if isinstance(value, dict):
            return {k: self._detect_type(v) for k, v in value.items()}
        elif isinstance(value, list):
            if len(value) > 0:
                return f"List[{self._detect_type(value[0])}]"
            return "List[Empty]"
        return type(value).__name__

    def display_structure(self, hierarchy):
        """Pretty print the structure to CLI"""
        table = Table(title="Dataset Structure Found")
        table.add_column("Field", style="cyan")
        table.add_column("Type/Hierarchy", style="magenta")

        for key, val in hierarchy.items():
            table.add_row(key, str(val))
        
        self.console.print(table)
