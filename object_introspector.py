from typing import Any, Dict, List, Tuple
import inspect
from collections import defaultdict


def analyze_object_attributes(obj: Any) -> Dict[str, Any]:
    """
    Analyzes an object's attributes and methods, organizing them systematically.

    This function performs deep introspection on a Python object, separating its
    attributes into data attributes (sorted lexicographically) and methods. Each
    data attribute is paired with its type information.

    Args:
        obj: Any Python object to analyze

    Returns:
        A dictionary with two main keys:
        - 'data_attributes': List of tuples (attribute_name, attribute_type)
          sorted lexicographically by attribute name
        - 'methods': Dictionary categorizing methods by their types
          (instance, class, static)

    Example:
        class Person:
            name = "John"  # class attribute
            def __init__(self):
                self.age = 30  # instance attribute

            def greet(self):  # instance method
                return f"Hello, {self.name}!"

        person = Person()
        result = analyze_object_attributes(person)
        # Result will contain sorted attributes with types and categorized methods
    """
    # Initialize the result structure
    result = {
        "data_attributes": [],  # Will store (name, type) tuples
        "methods": {"instance_methods": [], "class_methods": [], "static_methods": []},
    }

    # Get all attributes including inherited ones
    for attr_name in dir(obj):
        # Skip magic methods and private attributes
        if attr_name.startswith("__"):
            continue

        try:
            attr = getattr(obj, attr_name)

            # Check if it's a method
            if inspect.ismethod(attr) or inspect.isfunction(attr):
                # Determine method type
                if inspect.ismethod(attr):
                    if attr.__self__ is type(obj):
                        result["methods"]["class_methods"].append(attr_name)
                    else:
                        result["methods"]["instance_methods"].append(attr_name)
                elif isinstance(attr, staticmethod):
                    result["methods"]["static_methods"].append(attr_name)
                else:
                    result["methods"]["instance_methods"].append(attr_name)
            else:
                # It's a data attribute - store name and type
                attr_type = type(attr).__name__
                result["data_attributes"].append((attr_name, attr_type))

        except Exception as e:
            # Handle attributes that can't be accessed
            result["data_attributes"].append((attr_name, "inaccessible"))

    # Sort data attributes lexicographically by name
    result["data_attributes"].sort(key=lambda x: x[0])

    # Sort method lists
    for method_list in result["methods"].values():
        method_list.sort()

    return result


def print_object_analysis(obj: Any) -> None:
    """
    Prints a formatted analysis of an object's attributes and methods.

    This function presents the results of analyze_object_attributes in a
    readable format, with data attributes sorted lexicographically and
    displayed with their types.

    Args:
        obj: Any Python object to analyze

    Example:
        class Person:
            name = "John"
            def greet(self): pass

        person = Person()
        print_object_analysis(person)
        # Output will show sorted attributes with types and methods
    """
    analysis = analyze_object_attributes(obj)

    print(f"\nAnalysis of {type(obj).__name__} object:")

    print("\nData Attributes (name: type):")
    for attr_name, attr_type in analysis["data_attributes"]:
        print(f"  - {attr_name}: {attr_type}")

    print("\nMethods:")
    for method_type, methods in analysis["methods"].items():
        if methods:  # Only print non-empty categories
            print(f"\n  {method_type.replace('_', ' ').title()}:")
            for method in methods:
                print(f"    - {method}")
