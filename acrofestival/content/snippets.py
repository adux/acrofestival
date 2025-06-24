import os
from typing import Any, Dict

import yaml
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class ContentSnippets:
    _instance = None
    _snippets: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._snippets:
            self.load_snippets()

    def load_snippets(self) -> None:
        """Load snippets from multiple YAML files based on environment"""
        env = os.getenv("DJANGO_ENV", "development")
        snippets_dir = os.path.join(settings.ROOT_DIR, "config", "snippets")
        
        # Define the files to load in order
        snippet_filenames = [
            "general.yml",
            "winteracro.yml", 
            "urbanacro.yml",
            "dap.yml",
            "snippets.yml",  # Legacy file - keep for backward compatibility
            f"snippets_{env}.yml"  # Environment-specific overrides
        ]
        
        self._snippets = {}
        
        for filename in snippet_filenames:
            file_path = os.path.join(snippets_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    file_snippets = yaml.safe_load(f) or {}
                    # Merge snippets, later files override earlier ones
                    self._snippets.update(file_snippets)
        
        if not self._snippets:
            raise ImproperlyConfigured(
                "No snippets files found in config/snippets directory. "
                "Create at least one of: general.yml, winteracro.yml, urbanacro.yml, dap.yml, or snippets.yml"
            )

    def get_snippet(self, key: str, default: str = "") -> str:
        """Get a snippet by key with optional default value"""
        return str(self._snippets.get(key, default))

    def reload(self) -> None:
        """Force reload snippets from file"""
        self._snippets = {}
        self.load_snippets()


def get_snippet(key: str, default: str = "") -> str:
    """Helper function for template tag to retrieve a content snippet."""
    return ContentSnippets().get_snippet(key, default)