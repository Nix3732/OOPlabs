from injector import Injector
from lifestyle import LifeStyle
from interfaces import Interface1, Interface2, Interface3
from implementations import (
    Class1Debug, Class1Release,
    Class2Debug, Class2Release,
    Class3Debug, Class3Release)


def config_debug(injector: Injector):
    injector.register(Interface1, Class1Debug, LifeStyle.Singleton)
    injector.register(Interface2, Class2Debug, LifeStyle.Scoped)
    injector.register(Interface3, Class3Debug, LifeStyle.PerRequest)


def config_release(injector: Injector):
    injector.register(Interface1, Class1Release, LifeStyle.Singleton)
    injector.register(Interface2, Class2Release, LifeStyle.Scoped)
    injector.register(Interface3, Class3Release, LifeStyle.PerRequest)


class InjectorFactory:
    @staticmethod
    def create(debug_mode) -> Injector:
        injector = Injector()
        if debug_mode:
            config_debug(injector)
        else:
            config_release(injector)
        return injector