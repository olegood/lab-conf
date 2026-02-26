import json
import os
import uuid
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Optional


def _resolve_file_path(config_path: Path, version: Optional[str]) -> Optional[Path]:
    """Resolve the file path for a specific version or the latest version."""
    if version:
        return config_path / f"{version}.json"

    files = sorted(config_path.glob("*.json"), key=os.path.getmtime, reverse=True)
    return files[0] if files else None


class FileConfigStorage:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _config_path(self, service: str, environment: str) -> Path:
        path = self.base_path / service / environment
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save(self, service: str, environment: str, data: dict[str, Any], created_by: str) -> dict[str, Any]:
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
        with open(file_path, "w") as f:
            json.dump(record, f, indent=2)

        return record

    def get(self, service: str, environment: str, version: Optional[str]) -> Optional[dict[str, Any]]:
        config_path = self._config_path(service, environment)
        file_path = _resolve_file_path(config_path, version)

        if not file_path or not file_path.exists():
            return None

        with open(file_path) as file:
            return json.load(file)

    def list_versions(self, service: str, environment: str) -> list[str]:
        config_path = self._config_path(service, environment)
        return [f.stem for f in config_path.glob("*.json")]
