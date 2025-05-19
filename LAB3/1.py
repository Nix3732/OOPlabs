from typing import Protocol
import re
import socket
import datetime


class LogFilterProtocol(Protocol):
    def match(self, text: str) -> bool:
        ...


class SimpleLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str):
        self.pattern = pattern

    def match(self, text: str) -> bool:
        return self.pattern in text


class ReLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str):
        self.regexp = re.compile(pattern)

    def match(self, text: str) -> bool:
        return bool(self.regexp.search(text))



class LogHandlerProtocol(Protocol):
    def handle(self, text: str):
        ...


class FileHandler(LogHandlerProtocol):
    def __init__(self, path: str):
        self.path = path

    def handle(self, text: str):
        with open(self.path, 'a+') as f:
            f.write(f'{datetime.datetime.now()}: {text}\n')
            f.close()


class SocketHandler(LogHandlerProtocol):
    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port

    def handle(self, text: str):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(f'{str(datetime.datetime.now())}: {text}'.encode('utf-8'))
        except Exception as e:
            print(f'Ошибка сокета: {e}')


class ConsoleHandler(LogHandlerProtocol):
    def handle(self, text: str):
        print(f'{datetime.datetime.now()}: {text}')


class SyslogHandler(LogHandlerProtocol):
    pass


class Logger:
    def __init__(self, filters: [LogFilterProtocol], handlers: [LogHandlerProtocol]):
        self.filters = filters
        self.handlers = handlers

    def print(self, text: str):
        for fltr in self.filters:
            if fltr.match(text):
                for hndlr in self.handlers:
                    hndlr.handle(text)


if __name__ == '__main__':
    text = [
        'INFO: System started',
        'WARNING: You are not using the last version',
        'DEBUG: Correct connection',
        'ERROR 500: Internal Server Error',
        'ERROR 404: Not found'
    ]

    handlers = [
        ConsoleHandler(),
        FileHandler('log.log'),
        SocketHandler('localhost', 135),
    ]

    filters = [
        SimpleLogFilter('INFO'),
        ReLogFilter(r'(ERROR|WARNING|DEBUG)')
    ]

    l = Logger(filters, handlers)

    for t in text:
        l.print(t)