class DataProcessor:
    def __init__(self):
        pass

    def extract_fields(self, dataset, fields_map):
        """
        Extract specific fields from original dataset mapping to new names.
        fields_map: dict mapping original_field -> target_name
        """
        for row in dataset:
            extracted = {}
            for original, target in fields_map.items():
                # Handle nested fields via dot notation (e.g. "metadata.id")
                extracted[target] = self._get_nested(row, original)
            yield extracted

    def _get_nested(self, data, path):
        parts = path.split('.')
        for part in parts:
            if isinstance(data, dict):
                data = data.get(part)
            else:
                return None
        return data
