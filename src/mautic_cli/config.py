from __future__ import annotations

import json
from pathlib import Path

DEFAULT_CONFIG_DIR = Path.home() / ".mautic-cli"


class ConfigManager:
    def __init__(self, config_dir: Path = DEFAULT_CONFIG_DIR):
        self.config_dir = config_dir

    def _config_path(self, profile: str = "default") -> Path:
        if profile == "default":
            return self.config_dir / "config.json"
        return self.config_dir / f"config.{profile}.json"

    def load(self, profile: str = "default") -> dict:
        path = self._config_path(profile)
        if not path.exists():
            return {}
        return json.loads(path.read_text())

    def save(self, data: dict, profile: str = "default") -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        path = self._config_path(profile)
        path.write_text(json.dumps(data, indent=2))

    def delete(self, profile: str) -> bool:
        path = self._config_path(profile)
        if path.exists():
            path.unlink()
            return True
        return False

    def list_profiles(self) -> list[str]:
        if not self.config_dir.exists():
            return []
        profiles = []
        for path in sorted(self.config_dir.glob("config*.json")):
            name = path.stem  # "config" or "config.staging"
            if name == "config":
                profiles.append("default")
            elif name.startswith("config."):
                profiles.append(name[7:])  # strip "config."
        return profiles
