from interfaces import Interface1, Interface2, Interface3


class Class1Debug(Interface1):
    def do_work(self):
        print("Class1Debug doing work")


class Class1Release(Interface1):
    def do_work(self):
        print("Class1Release doing work")


class Class2Debug(Interface2):
    def __init__(self, interface1: Interface1):
        self.interface1 = interface1

    def do_task(self):
        print("Class2Debug doing task and calling Interface1:")
        self.interface1.do_work()


class Class2Release(Interface2):
    def __init__(self, interface1: Interface1):
        self.interface1 = interface1

    def do_task(self):
        print("Class2Release doing task and calling Interface1:")
        self.interface1.do_work()


class Class3Debug(Interface3):
    def __init__(self, interface1: Interface1, interface2: Interface2):
        self.interface1 = interface1
        self.interface2 = interface2

    def do_process(self):
        print("Class3Debug processing with Interface1 and Interface2:")
        self.interface1.do_work()
        self.interface2.do_task()


class Class3Release(Interface3):
    def __init__(self, interface1: Interface1, interface2: Interface2):
        self.interface1 = interface1
        self.interface2 = interface2

    def do_process(self):
        print("Class3Release processing with Interface1 and Interface2:")
        self.interface1.do_work()
        self.interface2.do_task()
