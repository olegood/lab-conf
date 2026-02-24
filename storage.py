import json
import uuid
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict


class FileConfigStorage:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _config_path(self, service: str, environment: str) -> Path:
        path = self.base_path / service / environment
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save(self, service: str, environment: str, config: dict[str, Any], created_by: str) -> Dict[str, Any]:
        version = str(uuid.uuid4())
        created_at = datetime.now(tz=UTC).isoformat()

        record = {
            'service': service,
            'environment': environment,
            'version': version,
            'config': config,
            'created_at': created_at,
            'created_by': created_by
        }

        file_path = self._config_path(service, environment) / f'{version}.json'
        with open(file_path, 'w') as f:
            json.dump(record, f, indent=2)

        return record

    def list_versions(self, service: str, environment: str) -> list[str]:
        config_path = self._config_path(service, environment)
        return [f.stem for f in config_path.glob('*.json')]
