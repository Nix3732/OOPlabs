from injector import Injector
from config import config_debug, config_release, InjectorFactory
from interfaces import Interface1, Interface2, Interface3


def demo_lifecycles(injector):
    print("Singleton Interface1:")
    i1a = injector.get_instance(Interface1)
    i1b = injector.get_instance(Interface1)
    print(f"Same instance? {i1a is i1b}")
    i1a.do_work()

    print("\nScoped Interface2:")
    with injector.create_scope():
        i2a = injector.get_instance(Interface2)
        i2b = injector.get_instance(Interface2)
        print(f"Same instance in scope? {i2a is i2b}")
        i2a.do_task()

    print("\nPerRequest Interface3:")
    with injector.create_scope():
        i3a = injector.get_instance(Interface3)
        i3b = injector.get_instance(Interface3)
        print(f"Same instance? {i3a is i3b}")
        i3a.do_process()
        i3b.do_process()


def demo_config(injector, config_func):
    config_func(injector)
    i1 = injector.get_instance(Interface1)
    with injector.create_scope():
        i2 = injector.get_instance(Interface2)
        i3 = injector.get_instance(Interface3)

    print(f"Interface1 instance: {type(i1).__name__}")
    print(f"Interface2 instance: {type(i2).__name__}")
    print(f"Interface3 instance: {type(i3).__name__}")


def main():
    print("=== Debug Configuration ===")
    injector = InjectorFactory.create(debug_mode=True)
    demo_lifecycles(injector)
    print("\nSummary of instances in Debug config:")
    demo_config(injector, config_debug)

    print("\n=== Release Configuration ===")
    injector = InjectorFactory.create(debug_mode=False)
    demo_lifecycles(injector)
    print("\nSummary of instances in Release config:")
    demo_config(injector, config_release)


if __name__ == "__main__":
    main()
