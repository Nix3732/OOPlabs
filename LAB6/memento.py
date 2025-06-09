import json
import os
from typing import Dict, Any


class KeyboardMemento:
    def __init__(self, key_bindings: Dict[str, str]):
        self._key_bindings = key_bindings.copy()

    def get_state(self) -> Dict[str, str]:
        return self._key_bindings.copy()


class KeyboardStateSaver:
    def __init__(self, filename="keyboard_bindings.json"):
        self.filename = filename

    def _get_default_bindings(self) -> Dict[str, str]:
        return {
            "ctrl+plus": "volume_up",
            "ctrl+minus": "volume_down",
            "ctrl+p": "media_player",
            "ctrl+l": "clear_screen"
        }

    def _get_current_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()

    def save_state(self, memento: KeyboardMemento) -> bool:
        try:
            state_data = {
                "version": "1.0",
                "key_bindings": memento.get_state(),
                "metadata": {
                    "saved_at": self._get_current_timestamp()
                }
            }
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False)
            print(f"Keyboard state saved to {self.filename}")
            return True
        except Exception as e:
            print(f"Error saving keyboard state: {e}")
            return False

    def load_state(self) -> KeyboardMemento:
        try:
            if not os.path.exists(self.filename):
                print(f"File {self.filename} not found, using default bindings")
                return KeyboardMemento(self._get_default_bindings())
            with open(self.filename, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            key_bindings = state_data.get("key_bindings", {})
            version = state_data.get("version", "unknown")
            print(f"Loaded keyboard state (version: {version}) from {self.filename}")
            return KeyboardMemento(key_bindings)
        except Exception as e:
            print(f"Error loading keyboard state: {e}")
            print("Using default bindings")
            return KeyboardMemento(self._get_default_bindings())

    def backup_state(self, memento: KeyboardMemento) -> bool:
        backup_filename = f"{self.filename}.backup"
        try:
            state_data = {
                "version": "1.0",
                "key_bindings": memento.get_state(),
                "metadata": {
                    "backed_up_at": self._get_current_timestamp()
                }
            }
            with open(backup_filename, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False)
            print(f"Backup created: {backup_filename}")
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

    def get_saved_info(self) -> Dict[str, Any]:
        try:
            if not os.path.exists(self.filename):
                return {"exists": False}
            with open(self.filename, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            return {
                "exists": True,
                "version": state_data.get("version", "unknown"),
                "bindings_count": len(state_data.get("key_bindings", {})),
                "metadata": state_data.get("metadata", {})
            }
        except Exception as e:
            return {"exists": True, "error": str(e)}
