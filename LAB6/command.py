from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def get_description(self):
        ...

    @abstractmethod
    def execute(self):
        ...

    @abstractmethod
    def undo(self):
        ...


class MediaPlayerCommand(Command):
    def __init__(self):
        self.is_playing = False

    def get_description(self):
        return "Toggle Media Player"

    def execute(self):
        if not self.is_playing:
            self.is_playing = True
            return "media player launched"
        else:
            self.is_playing = False
            return "media player stopped"

    def undo(self):
        if self.is_playing:
            self.is_playing = False
            return "media player closed"
        else:
            self.is_playing = True
            return "media player launched"


class ClearScreenCommand(Command):
    def __init__(self, output_manager):
        self.output_manager = output_manager
        self.backup_text = ""

    def get_description(self):
        return "Clear Screen"

    def execute(self):
        self.backup_text = self.output_manager.get_text()
        self.output_manager.clear()
        return "screen cleared"

    def undo(self):
        self.output_manager.restore_text(self.backup_text)
        return "screen restored"


class VolumeUpCommand(Command):
    def __init__(self, volume_step=10):
        self.volume_step = volume_step
        self.current_volume = 50

    def get_description(self):
        return f"Volume Up (+{self.volume_step}%)"

    def execute(self):
        self.current_volume = min(100, self.current_volume + self.volume_step)
        return f"volume increased +{self.volume_step}%"

    def undo(self):
        self.current_volume = max(0, self.current_volume - self.volume_step)
        return f"volume decreased -{self.volume_step}%"


class VolumeDownCommand(Command):
    def __init__(self, volume_step=10):
        self.volume_step = volume_step
        self.current_volume = 50

    def get_description(self):
        return f"Volume Down (-{self.volume_step}%)"

    def execute(self):
        self.current_volume = max(0, self.current_volume - self.volume_step)
        return f"volume decreased -{self.volume_step}%"

    def undo(self):
        self.current_volume = min(100, self.current_volume + self.volume_step)
        return f"volume increased +{self.volume_step}%"


class KeyCommand(Command):
    def __init__(self, char, output_manager):
        self.char = char
        self.output_manager = output_manager
        self.executed = False

    def execute(self):
        self.output_manager.add_text(self.char)
        self.executed = True
        return f"Inserted '{self.char}'"

    def undo(self):
        if self.executed and self.output_manager.can_backspace():
            removed_char = self.output_manager.backspace()
            self.executed = False
            return f"Removed '{removed_char}'"
        else:
            raise Exception("Nothing to undo for KeyCommand")

    def get_description(self):
        return f"Insert '{self.char}'"
