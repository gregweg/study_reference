# Singleton
# When to use: When you need exactly one instance of a class (e.g., config, logging).
# When not to use: When unit testing or global state can cause side effects.
class Singleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


# Factory Method
# When to use: When you want to delegate instantiation logic to subclasses or handle dynamic object creation.
# When not to use: When object creation is simple and does not require extra abstraction.
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

def pet_factory(pet="dog"):
    pets = dict(dog=Dog(), cat=Cat())
    return pets.get(pet, Dog())


# Abstract Factory
# When to use: When you need to create families of related objects.
# When not to use: When products are unrelated or don't follow a common theme.
class DogFactory:
    def get_pet(self):
        return Dog()

    def get_food(self):
        return "Dog Food"

class CatFactory:
    def get_pet(self):
        return Cat()

    def get_food(self):
        return "Cat Food"

def get_factory(pet="dog"):
    return DogFactory() if pet == "dog" else CatFactory()


# Builder
# When to use: When creating complex objects step by step.
# When not to use: For simple objects with few parameters.
class Burger:
    def __init__(self):
        self.ingredients = []

    def add(self, ingredient):
        self.ingredients.append(ingredient)

    def __str__(self):
        return ", ".join(self.ingredients)

class BurgerBuilder:
    def build_veggie_burger(self):
        burger = Burger()
        burger.add("Lettuce")
        burger.add("Tomato")
        burger.add("Patty")
        return burger


# Prototype
# When to use: When object creation is expensive or should be copied.
# When not to use: When objects are simple and easily created.
import copy

class Prototype:
    def __init__(self):
        self.objects = {}

    def register(self, name, obj):
        self.objects[name] = obj

    def clone(self, name, **attrs):
        obj = copy.deepcopy(self.objects.get(name))
        obj.__dict__.update(attrs)
        return obj


# Adapter
# When to use: To make two incompatible interfaces work together.
# When not to use: When classes already share the same interface.
class EuropeanSocket:
    def voltage(self):
        return 230

class USASocketAdapter:
    def __init__(self, euro_socket):
        self.euro_socket = euro_socket

    def voltage(self):
        return 110


# Decorator
# When to use: To add responsibilities to objects dynamically.
# When not to use: When subclassing would be clearer or more efficient.
def uppercase_decorator(func):
    def wrapper():
        return func().upper()
    return wrapper

@uppercase_decorator
def greet():
    return "hello"


# Facade
# When to use: To provide a simple interface to a complex system.
# When not to use: When direct access to subsystems is required.
class CPU:
    def freeze(self): return "Freezing CPU"

class Memory:
    def load(self): return "Loading memory"

class Computer:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()

    def start(self):
        return f"{self.cpu.freeze()}, {self.memory.load()}"


# Composite
# When to use: When you want to treat individual objects and groups of objects the same way.
# When not to use: When the hierarchy is flat and simple.
class Component:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, component):
        self.children.append(component)

    def display(self, depth=0):
        result = "  " * depth + self.name + "\n"
        for child in self.children:
            result += child.display(depth + 1)
        return result


# Observer
# When to use: When multiple objects need to be notified of state changes.
# When not to use: When a single object updates state and no notifications are required.
class Subject:
    def __init__(self):
        self._observers = []

    def register(self, obs):
        self._observers.append(obs)

    def notify(self, message):
        for obs in self._observers:
            obs.update(message)

class Observer:
    def update(self, message):
        print(f"Observer received: {message}")


# Strategy
# When to use: To select an algorithm at runtime.
# When not to use: When there’s only one way to accomplish a task.
class StrategyA:
    def execute(self): return "Strategy A"

class StrategyB:
    def execute(self): return "Strategy B"

class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def execute(self):
        return self.strategy.execute()


# Command
# When to use: To encapsulate a request as an object.
# When not to use: When a simple function call suffices.
class Light:
    def on(self): return "Light ON"
    def off(self): return "Light OFF"

class Command:
    def execute(self): pass

class OnCommand(Command):
    def __init__(self, light): self.light = light
    def execute(self): return self.light.on()

class OffCommand(Command):
    def __init__(self, light): self.light = light
    def execute(self): return self.light.off()


# Main function to demonstrate each pattern
if __name__ == "__main__":
    print("Singleton:", Singleton() is Singleton())

    print("Factory Method:", pet_factory("cat").speak())

    factory = get_factory("dog")
    print("Abstract Factory:", factory.get_pet().speak(), factory.get_food())

    burger = BurgerBuilder().build_veggie_burger()
    print("Builder:", burger)

    prototype = Prototype()
    burger_clone = Burger()
    prototype.register("veggie", burger_clone)
    clone = prototype.clone("veggie")
    print("Prototype:", clone)

    adapter = USASocketAdapter(EuropeanSocket())
    print("Adapter:", adapter.voltage())

    print("Decorator:", greet())

    computer = Computer()
    print("Facade:", computer.start())

    root = Component("root")
    child = Component("child")
    root.add(child)
    print("Composite:\n" + root.display())

    subject = Subject()
    obs1 = Observer()
    obs2 = Observer()
    subject.register(obs1)
    subject.register(obs2)
    subject.notify("Hello Observers")

    context = Context(StrategyA())
    print("Strategy:", context.execute())

    light = Light()
    command = OnCommand(light)
    print("Command:", command.execute())