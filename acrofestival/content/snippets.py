import os
from typing import Any, Dict

import yaml
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured

CACHE_VERSION_KEY = "content_snippets:version"
CACHE_MERGED_KEY = "content_snippets:merged"


class ContentSnippets:
    _instance = None
    _yaml_defaults: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._yaml_defaults:
            self._load_yaml_defaults()

    def _load_yaml_defaults(self) -> None:
        env = os.getenv("DJANGO_ENV", "development")
        snippets_dir = os.path.join(settings.ROOT_DIR, "config", "snippets")
        snippet_filenames = [
            "general.yml",
            "winteracro.yml",
            "urbanacro.yml",
            "dap.yml",
            "snippets.yml",
            f"snippets_{env}.yml",
        ]

        defaults: Dict[str, Any] = {}
        for filename in snippet_filenames:
            file_path = os.path.join(snippets_dir, filename)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    file_snippets = yaml.safe_load(f) or {}
                    defaults.update(file_snippets)

        if not defaults:
            raise ImproperlyConfigured(
                "No snippets files found in config/snippets directory."
            )

        self._yaml_defaults = defaults

    def _get_merged(self) -> Dict[str, Any]:
        version = cache.get(CACHE_VERSION_KEY, 0)
        cache_key = f"{CACHE_MERGED_KEY}:v{version}"
        merged = cache.get(cache_key)
        if merged is not None:
            return merged

        merged = dict(self._yaml_defaults)

        # Local import to avoid AppRegistryNotReady at process start.
        from acrofestival.content.models import ContentSnippet

        for key, value in ContentSnippet.objects.values_list("key", "value"):
            merged[key] = value

        cache.set(cache_key, merged, timeout=None)
        return merged

    def get_snippet(self, key: str, default: str = "") -> str:
        return str(self._get_merged().get(key, default))

    def yaml_default(self, key: str, default: str = "") -> str:
        return str(self._yaml_defaults.get(key, default))

    def yaml_keys_for_files(self, filenames):
        """Return the set of keys defined in the given YAML filenames."""
        snippets_dir = os.path.join(settings.ROOT_DIR, "config", "snippets")
        keys = set()
        for filename in filenames:
            file_path = os.path.join(snippets_dir, filename)
            if not os.path.exists(file_path):
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                keys.update(data.keys())
        return keys

    @staticmethod
    def bump_version() -> None:
        """Invalidate the merged cache for all workers."""
        try:
            cache.incr(CACHE_VERSION_KEY)
        except ValueError:
            cache.set(CACHE_VERSION_KEY, 1)

    def reload(self) -> None:
        """Reload YAML defaults from disk and invalidate the cache."""
        self._yaml_defaults = {}
        self._load_yaml_defaults()
        self.bump_version()


def get_snippet(key: str, default: str = "") -> str:
    return ContentSnippets().get_snippet(key, default)
