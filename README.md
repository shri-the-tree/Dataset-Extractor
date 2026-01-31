# DataExtractor Pro 🚀

**DataExtractor Pro** is a high-performance, developer-focused CLI tool designed to bridge the gap between messy, unformatted HuggingFace datasets and actionable training data for LLMs and Machine Learning models.

Stop spending hours writing custom scripts to handle schema mismatches. DataExtractor Pro identifies, analyzes, and transforms datasets through an intuitive interactive interface.

## 🌟 Key Features

- **HuggingFace Native**: Seamlessly pulls datasets via ID or URL. Supports private repositories with secure token authentication.
- **Deep Structural Inspection**: Recursively analyzes dataset hierarchies, including nested JSON objects and complex lists.
- **Memory-Efficient Streaming**: Built on top of the `datasets` streaming API. Process datasets of any size (thousands to millions of rows) without exhausting RAM.
- **Dot-Notation Field Extraction**: Effortlessly extract nested data using dot-notated paths (e.g., `metadata.user.response`).
- **Interactive Remapping**: Rename fields on the fly to match your training script requirements (e.g., `text_v1` -> `instruction`).
- **Multi-Format Export**: One-click export to **JSONL, CSV, or JSON**, automatically organized into a local `data/` directory.

## 🛠️ Technical Architecture

The tool follows a modular "Pipeline" design:

- **Loader**: Manages HF API connections, authentication, and streaming configurations.
- **Inspector**: Analyzes schema features and identifies data types and nesting levels.
- **Processor**: Handles field selection, mapping, and extraction logic using generator patterns to maintain a low memory footprint.
- **Exporter**: A dedicated factory module for extensible file formatting.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A HuggingFace Access Token (optional, for private/gated datasets)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shri-the-tree/Dataset-Extractor.git
   cd Dataset-Extractor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Simply launch the interactive CLI:
```bash
python main.py
```

**Step-by-Step Workflow:**
1. **Source Selection**: Paste a HuggingFace Dataset ID or full URL.
2. **Path Discovery**: The tool automatically detects available subsets (configs) and splits (train, validation, harmful, etc.).
3. **Select & Transform**: Choose the fields you want and rename them if necessary.
4. **Export**: Choose your format and let the tool handle the heavy lifting.

## 📂 Project Structure

```text
├── core/
│   ├── loader.py       # HF Hub Integration
│   ├── inspector.py    # Schema & Hierarchy Analysis
│   ├── processor.py    # Field Mapping Logic
│   └── exporter.py     # CSV/JSONL/JSON Writers
├── data/               # Default output directory
├── main.py             # CLI Entrypoint
└── requirements.txt    # Production dependencies
```

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Developed for rapid LLM fine-tuning and data engineering workflows.*
