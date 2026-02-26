"""File-based storage backend for configuration management.

This module provides a file-based storage implementation for managing
service configurations across different environments with versioning support.
Each configuration version is stored as a separate JSON file, organized in
a directory structure by service and environment.
"""
import json
import os
import uuid
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Optional


def _resolve_file_path(config_path: Path, version: Optional[str]) -> Optional[Path]:
    """Resolve the file path for a specific version or the latest version.
    
    Args:
        config_path: Directory path containing configuration version files.
        version: Optional version UUID. If provided, returns a path to that specific version.
                If None, returns a path to the most recently modified file.
    
    Returns:
        Path to the configuration file, or None if no files exist.
    """
    if version:
        return config_path / f"{version}.json"

    files = sorted(config_path.glob("*.json"), key=os.path.getmtime, reverse=True)
    return files[0] if files else None


class FileConfigStorage:
    """File-based storage backend for configuration management.
    
    Stores configurations as JSON files organized by service and environment.
    Each configuration version is stored in a separate file named by its UUID.
    Directory structure: {base_path}/{service}/{environment}/{version}.json
    
    Attributes:
        base_path: Root directory for all configuration storage.
    """

    def __init__(self, base_path: str):
        """Initialize the file-based configuration storage.
        
        Args:
            base_path: Root directory path where configurations will be stored.
                      Creates the directory if it doesn't exist.
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _config_path(self, service: str, environment: str) -> Path:
        """Get or create the directory path for a service/environment pair.
        
        Args:
            service: Name of the service.
            environment: Name of the environment (e.g., "dev", "staging", "prod").
        
        Returns:
            Path object pointing to the service/environment directory.
        """
        path = self.base_path / service / environment
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save(self, service: str, environment: str, data: dict[str, Any], created_by: str) -> dict[str, Any]:
        """Save a new configuration version.
        
        Creates a new UUID-based version and stores the configuration as a JSON file.
        
        Args:
            service: Name of the service.
            environment: Name of the environment.
            data: Configuration key-value data to store.
            created_by: Username or identifier of the creator.
        
        Returns:
            Dictionary containing the complete stored record including service,
            environment, version, data, created_at, and created_by fields.
        """
        version = str(uuid.uuid4())
        created_at = datetime.now(tz=UTC).isoformat()

        record = {
            "service": service,
            "environment": environment,
            "version": version,
            "data": data,
            "created_at": created_at,
            "created_by": created_by
        }

        file_path = self._config_path(service, environment) / f"{version}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)

        return record

    def get(self, service: str, environment: str, version: Optional[str]) -> Optional[dict[str, Any]]:
        """Retrieve a configuration version.
        
        Args:
            service: Name of the service.
            environment: Name of the environment.
            version: Optional version UUID. If None, retrieves the latest version.
        
        Returns:
            Dictionary containing the configuration record, or None if not found.
        """
        config_path = self._config_path(service, environment)
        file_path = _resolve_file_path(config_path, version)

        if not file_path or not file_path.exists():
            return None

        with open(file_path, encoding="utf-8") as file:
            return json.load(file)

    def list_versions(self, service: str, environment: str) -> list[str]:
        """List all version UUIDs for a service/environment pair.
        
        Args:
            service: Name of the service.
            environment: Name of the environment.
        
        Returns:
            List of version UUID strings. Returns an empty list if no versions exist.
        """
        config_path = self._config_path(service, environment)
        return [f.stem for f in config_path.glob("*.json")]
