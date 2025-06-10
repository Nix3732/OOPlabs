from contextlib import contextmanager
from typing import Callable, Optional, Type, Union
import inspect
from lifestyle import LifeStyle


class Injector:
    def __init__(self):
        self._registrations = {}
        self._singletons = {}
        self._scoped_instances_stack = []

    def register(self, interface_type: Type,
                 class_or_factory: Union[Type, Callable],
                 life_style: LifeStyle = LifeStyle.PerRequest,
                 params: Optional[dict] = None):
        self._registrations[interface_type] = (class_or_factory, life_style, params or {})

    def get_instance(self, interface_type: Type):
        if interface_type not in self._registrations:
            raise Exception(f"Interface {interface_type} not registered")

        class_or_factory, life_style, params = self._registrations[interface_type]

        if life_style == LifeStyle.Singleton:
            if interface_type not in self._singletons:
                instance = self._create_instance(class_or_factory, params)
                self._singletons[interface_type] = instance
            return self._singletons[interface_type]

        elif life_style == LifeStyle.Scoped:
            if not self._scoped_instances_stack:
                raise Exception("No active scope")
            current_scope = self._scoped_instances_stack[-1]
            if interface_type not in current_scope:
                instance = self._create_instance(class_or_factory, params)
                current_scope[interface_type] = instance
            return current_scope[interface_type]

        else:
            return self._create_instance(class_or_factory, params)

    def _create_instance(self, class_or_factory: Union[Type, Callable], params: dict):
        if callable(class_or_factory) and not isinstance(class_or_factory, type):
            return class_or_factory(self)

        ctor = class_or_factory.__init__
        sig = inspect.signature(ctor)
        args = {}
        for name, param in sig.parameters.items():
            if name == 'self':
                continue
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            if name in params:
                args[name] = params[name]
            else:
                if param.annotation != inspect.Parameter.empty:
                    dep_type = param.annotation
                    args[name] = self.get_instance(dep_type)
                else:
                    if param.default != inspect.Parameter.empty:
                        continue
                    raise Exception(f"Cannot resolve parameter '{name}' for {class_or_factory}")

        return class_or_factory(**args)

    @contextmanager
    def create_scope(self):
        self._scoped_instances_stack.append({})
        try:
            yield
        finally:
            self._scoped_instances_stack.pop()
