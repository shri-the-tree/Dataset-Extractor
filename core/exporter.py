import json
import csv

class DataExporter:
    @staticmethod
    def to_jsonl(iterable, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in iterable:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

    @staticmethod
    def to_csv(iterable, output_path):
        # We need to peek at the first item to get headers
        try:
            first = next(iterable)
        except StopIteration:
            return
        
        fieldnames = list(first.keys())
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(first)
            for item in iterable:
                writer.writerow(item)

    @staticmethod
    def to_json(iterable, output_path):
        # Convert entire iterable to list and dump
        data = list(iterable)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
