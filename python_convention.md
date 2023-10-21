# Python conventions used:

**Naming Conventions:** Use descriptive and meaningful names for variables, functions, classes, and modules. 
* Variable names should be lowercase with words separated by underscores (e.g., my_variable). 
* Function and method names should also be lowercase with words separated by underscores (e.g., calculate_average). 
* Module names should be lowercase with words separated by underscores (e.g., my_module.py). 

* Class names should follow the CamelCase convention (e.g., MyClass).

**Miscelinious conventions**:
* Use spaces after coma [2, 3, 5]
* Limit lines to a maximum of 79 characters to fit the screen properly. If you don't have an extention which does the work for you, just use shorter lines than avarage :) 
* Separate logical parts of code by 1 empty line for readability. All functions also should be separated, unless there is a group of similar functions. Then the function which does not belong to the group can be separated by 2 empty lines.

**Imports:** Import each module on a separate line. Group imports in the following order: standard library imports, third-party library imports, and local application imports.

**Comments and Documentation:** Write docstrings for functions, classes, and modules to provide documentation that can be accessed using tools like Python's built-in help() function. Example is below (Args and Return can be optional as long as they are crystal clear. Otherwise it's better to mention them)
```python
def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.

    Args:
        numbers (list): A list of numbers.

    Returns:
        float: The average of the numbers.
    """
    total = sum(numbers)
    average = total / len(numbers)
    return average`
