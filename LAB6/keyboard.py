from typing import Dict, List, Optional
from command import Command, MediaPlayerCommand, ClearScreenCommand, VolumeUpCommand, VolumeDownCommand, KeyCommand
from output_manager import OutputManager
from memento import KeyboardStateSaver, KeyboardMemento


class Keyboard:
    def __init__(self):
        self.output_manager = OutputManager()
        self.state_saver = KeyboardStateSaver()
        self.command_history: List[Command] = []
        self.history_position = -1
        self.key_bindings: Dict[str, str] = {}
        self._init_commands()
        self._load_key_bindings()

    def _init_commands(self):
        self.volume_up_cmd = VolumeUpCommand(20)
        self.volume_down_cmd = VolumeDownCommand(20)
        self.media_player_cmd = MediaPlayerCommand()
        self.clear_screen_cmd = ClearScreenCommand(self.output_manager)

    def add_key_binding(self, key_combination: str, command_type: str):
        self.key_bindings[key_combination.lower()] = command_type
        print(f"Key binding added: {key_combination} -> {command_type}")
        self._save_key_bindings()

    def remove_key_binding(self, key_combination: str):
        key = key_combination.lower()
        if key in self.key_bindings:
            del self.key_bindings[key]
            print(f"Key binding removed: {key_combination}")
            self._save_key_bindings()
        else:
            print(f"Key binding not found: {key_combination}")

    def press_key(self, key: str) -> bool:
        key_lower = key.lower()
        if key_lower in self.key_bindings:
            command_type = self.key_bindings[key_lower]
            command = self._create_command(command_type)
            if command:
                return self._execute_command(command)
        if len(key) == 1 and key.isprintable():
            command = KeyCommand(key, self.output_manager)
            return self._execute_command(command)
        print(f"Unknown key or combination: {key}")
        return False

    def _create_command(self, command_type: str) -> Optional[Command]:
        if command_type == "volume_up":
            return self.volume_up_cmd
        elif command_type == "volume_down":
            return self.volume_down_cmd
        elif command_type == "media_player":
            return self.media_player_cmd
        elif command_type == "clear_screen":
            return self.clear_screen_cmd
        else:
            print(f"Unknown command type: {command_type}")
            return None

    def _execute_command(self, command: Command) -> bool:
        try:
            result = command.execute()
            if self.history_position < len(self.command_history) - 1:
                self.command_history = self.command_history[:self.history_position + 1]
            self.command_history.append(command)
            self.history_position = len(self.command_history) - 1
            if isinstance(command, KeyCommand):
                self.output_manager.log_current_state()
            else:
                self.output_manager.log_command(result)
            return True
        except Exception as e:
            print(f"Error executing command: {e}")
            return False

    def undo(self) -> bool:
        if self.history_position >= 0:
            command = self.command_history[self.history_position]
            try:
                result = command.undo()
                self.history_position -= 1
                if isinstance(command, KeyCommand):
                    self.output_manager.log_command("undo")
                    self.output_manager.log_current_state()
                else:
                    self.output_manager.log_command(result)
                return True
            except Exception as e:
                print(f"Error undoing command: {e}")
                return False
        else:
            print("Nothing to undo")
            return False

    def redo(self) -> bool:
        if self.history_position < len(self.command_history) - 1:
            self.history_position += 1
            command = self.command_history[self.history_position]
            try:
                result = command.execute()
                if isinstance(command, KeyCommand):
                    self.output_manager.log_command(" redo")
                    self.output_manager.log_current_state()
                else:
                    self.output_manager.log_command(result)
                return True
            except Exception as e:
                print(f"Error redoing command: {e}")
                return False
        else:
            print("Nothing to redo")
            return False

    def _save_key_bindings(self):
        memento = KeyboardMemento(self.key_bindings)
        self.state_saver.save_state(memento)

    def _load_key_bindings(self):
        memento = self.state_saver.load_state()
        self.key_bindings = memento.get_state()

    def show_bindings(self):
        print("\nCurrent key bindings:")
        if not self.key_bindings:
            print("No key bindings defined")
        else:
            for key, command in self.key_bindings.items():
                print(f"  {key} -> {command}")

    def show_history(self):
        print(f"\nCommand history (position: {self.history_position}):")
        for i, cmd in enumerate(self.command_history):
            marker = " <-- current" if i == self.history_position else ""
            print(f"  {i}: {cmd.get_description()}{marker}")

    def clear_history(self):
        self.command_history.clear()
        self.history_position = -1
        print("Command history cleared")

    def get_stats(self):
        return {
            "total_commands": len(self.command_history),
            "current_position": self.history_position,
            "key_bindings": len(self.key_bindings),
            "current_text_length": len(self.output_manager.get_text())
        }
