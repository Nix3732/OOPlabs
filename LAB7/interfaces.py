from abc import ABC, abstractmethod


class Interface1(ABC):
    @abstractmethod
    def do_work(self):
        pass


class Interface2(ABC):
    @abstractmethod
    def do_task(self):
        pass


class Interface3(ABC):
    @abstractmethod
    def do_process(self):
        pass
