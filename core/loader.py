from huggingface_hub import HfApi, login
from datasets import load_dataset, get_dataset_config_names, get_dataset_split_names
import os

class DatasetLoader:
    def __init__(self):
        self.api = HfApi()

    def check_access(self, dataset_id):
        """Check if dataset is public or requires authentication"""
        try:
            info = self.api.dataset_info(dataset_id)
            return True, info.private
        except Exception as e:
            if "401" in str(e) or "403" in str(e):
                return False, True
            raise e

    def authenticate(self, token):
        """Login to HuggingFace"""
        try:
            login(token=token)
            return True
        except Exception:
            return False

    def get_configs(self, dataset_id):
        """Get available configurations/subsets for the dataset"""
        try:
            return get_dataset_config_names(dataset_id)
        except Exception:
            return ["default"]

    def get_splits(self, dataset_id, config="default"):
        """Get available splits for a configuration"""
        try:
            return get_dataset_split_names(dataset_id, config)
        except Exception:
            return ["train"]

    def load(self, dataset_id, config="default", split=None, streaming=True):
        """Load the dataset (streaming by default for efficiency)"""
        return load_dataset(dataset_id, config, split=split, streaming=streaming)
