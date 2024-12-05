# Performance Directory README

## Overview
This directory contains a collection of performance-related modules and scripts that demonstrate various Object-Oriented Programming (OOP) principles and programming concepts. The primary focus of this directory is to showcase how these concepts can be applied to improve the performance of Python applications.

## OOP Principles and Programming Concepts
1. Threading
Threading is a programming concept that allows multiple threads to execute concurrently within a single process. This can improve responsiveness and system utilization, especially in I/O-bound applications.

Definition: Threading is a technique for achieving concurrency in a program by dividing it into multiple threads that can run concurrently.

Example:
```python

import threading
import time

def print_numbers():
    for i in range(10):
        time.sleep(1)
        print(i)

def print_letters():
    for letter in 'abcdefghij':
        time.sleep(1)
        print(letter)

# Create threads
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# Start threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()
```
In this example, we create two threads that print numbers and letters concurrently. The `threading module` is used to create and manage threads.

2. Multiprocessing
Multiprocessing is a programming concept that allows multiple processes to execute concurrently, improving overall system performance.

Definition: Multiprocessing is a technique for achieving concurrency in a program by dividing it into multiple processes that can run concurrently.

Example:
```python
import multiprocessing
import time

def print_numbers():
    for i in range(10):
        time.sleep(1)
        print(i)

def print_letters():
    for letter in 'abcdefghij':
        time.sleep(1)
        print(letter)

# Create processes
process1 = multiprocessing.Process(target=print_numbers)
process2 = multiprocessing.Process(target=print_letters)

# Start processes
process1.start()
process2.start()

# Wait for both processes to finish
process1.join()
process2.join()
```
In this example, we create two processes that print numbers and letters concurrently. The multiprocessing module is used to create and manage processes.

3. Inheritance
Inheritance is a fundamental concept in OOP that allows one class to inherit the properties and behavior of another class.

Definition: Inheritance is a mechanism in which one class can inherit the properties and behavior of another class.

Example:
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def bark(self):
        print(f"{self.name} the {self.breed} is barking")

my_dog = Dog("Fido", "Golden Retriever")
my_dog.eat()  # Output: Fido is eating
my_dog.bark()  # Output: Fido the Golden Retriever is barking
```
In this example, the `Dog` class inherits the `eat` method from the `Animal` class and adds its own `bark` method.

4. Abstract Classes
Abstract classes are classes that cannot be instantiated and are designed to be inherited by other classes.

Definition: An abstract class is a class that cannot be instantiated and is designed to be inherited by other classes.

Example:
```python
from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log(self, message):
        pass

class FileLogger(Logger):
    def log(self, message):
        print(f"Logging to file: {message}")

class ConsoleLogger(Logger):
    def log(self, message):
        print(f"Logging to console: {message}")

# Cannot instantiate Logger class
try:
    logger = Logger()
except TypeError:
    print("Cannot instantiate abstract class")

file_logger = FileLogger()
file_logger.log("Hello, world!")  # Output: Logging to file: Hello, world!

console_logger = ConsoleLogger()
console_logger.log("Hello, world!")  # Output: Logging to console: Hello, world!
```
In this example, the `Logger` class is an abstract class that defines the `log` method, which must be implemented by any subclass.

5. Polymorphism

Polymorphism is the ability of an object to take on multiple forms, depending on the context in which it is used.

Definition: Polymorphism is the ability of an object to take on multiple forms, depending on the context in which it is used.

Example:
```python
class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

def calculate_area(shape: Shape):
    return shape.area()

circle = Circle(5)
rectangle = Rectangle(4, 6)

print(calculate_area(circle))  # Output: 78.5
print(calculate_area(rectangle))  # Output: 24
```
In this example, the `calculate_area` function takes a `Shape` object as an argument and calls its area method. The `Circle` and `Rectangle` classes are subclasses of `Shape` and implement their own `area` methods. The calculate_area function can work with objects of either class, demonstrating polymorphism.

6. Decorators
Decorators are a special type of function that can modify or extend the behavior of another function.

Definition: A decorator is a function that takes another function as an argument and returns a new function that "wraps" the original function.

Example:
```python
import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to execute")
        return result
    return wrapper

@timer_decorator
def example_function():
    time.sleep(2)
    print("Example function executed")

example_function()
```
In this example, the `timer_decorator` function takes a function `func` as an argument and returns a new function `wrapper` that wraps the original function. The `wrapper` function measures the execution time of the original function and prints the result. The `example_function` is decorated with the `timer_decorator` using the `@` syntax.


Performance Decorator

The performance_decorator.py file contains a decorator that measures the execution time of a function and prints the result. The decorator can be used to measure the performance of any function.

```python
import time
from functools import wraps

def performance_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to execute")
        return result
    return wrapper
```
This decorator can be used to measure the performance of any function, for example:

```python
@performance_decorator
def example_function():
    time.sleep(2)
    print("Example function executed")

example_function()
```
This will print the execution time of the `example_function` function.