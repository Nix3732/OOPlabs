from Protocols import PropertyChangedListenerProtocol, DataChangedProtocol


class LoggerListener(PropertyChangedListenerProtocol):
    def on_property_changed(self, obj: DataChangedProtocol, property_name):
        print(f"[Logger] Свойство '{property_name}' изменено в {obj}")