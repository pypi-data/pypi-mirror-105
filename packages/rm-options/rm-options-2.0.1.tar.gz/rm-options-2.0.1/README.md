
# rm-options

[![PyPI version](https://badge.fury.io/py/rm-options.svg)](https://badge.fury.io/py/rm-options)
![build state](https://github.com/MartinR2295/rm-options/actions/workflows/build.yml/badge.svg
)
![build state](https://github.com/MartinR2295/rm-options/actions/workflows/test.yml/badge.svg
)

Python package for easier cli options handling.

## Features

- long names and short names (-h and --help)
- default values
- auto generated usage
- value parsing (to get int, float, ... values)
- required logic
- automatic interactive input option for needed options
- multiple values for one option

Example output for the automatic generated usage:
```shell
Usage
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
python test.py

Required Options
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
--name -n: your name {value needed}
--test -t: test {value needed} {default: t}

Optional Options
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
--all: any text
--delete: delete something {value needed}
--force -f: force in int {value needed}
--help -h: show usage
--measures -m: force in int {value needed} {multiple values possible}
--more: more text
--values: some values {value needed} {multiple values possible}
```

## Install

```shell
pip install rm-options
```

## Usage

Import the package, and create an option handler.
```python
from rmoptions import RMOptionHandler
option_handler = RMOptionHandler()
```

Create an option with the option handler.
```python
name_option = option_handler.create_option("name", "defines the name")
```

Parse, check and map all options
```python
result = option_handler.check()
```

Show error and usage if check wasn't successful.
```python
if not result:
    option_handler.print_error()
    option_handler.print_usage()
    exit()
```

Use the parsed value of an option.
```python
anyFunction(name_option.value)
```

## Advanced Possibilities

Create an option with a short name (default: None)
```python
name_option = option_handler.create_option("name", "defines the name", short_name="n")
```

Create an option which is required by the script (default: False)
```python
name_option = option_handler.create_option("name", "defines the name", required=True)
```

Define a default value for the option (default: None)
```python
name_option = option_handler.create_option("name", "defines the name", default_value="john")
```

Define if an option needs a value (default: False)
```python
name_option = option_handler.create_option("name", "defines the name", needs_value=True)
```

Define if an option can handle multiple values (with a space as seperator) (default: False)
```python
name_option = option_handler.create_option("name", "defines the name", multiple_values=True)
```

Define a mapper class, which maps the value to a specific type (default: None)\
It's also possible to write custom mappers.
```python
from rmoptions.mapper import IntMapper
name_option = option_handler.create_option("name", "defines the name", mapper=IntMapper)
print(type(name_option.value)) #outputs: int
```

### Option Handler

Prevent the interactive mode, where the script will ask the user for missing values.
If you set this option to False (default: True), the check function will directly return False if something is missing.
```python
option_handler = RMOptionHandler(ask_for_missing_values=False)
```

There are also other possibilities for the RMOptionHandler.
```python
option_handler = RMOptionHandler(usage_title="Usage", 
                                 usage_description="python {}".format(sys.argv[0]),
                                 help_option_short_name="h", 
                                 help_option_long_name="help", 
                                 help_option_description="show usage",
                                 ask_for_missing_values=True, 
                                 ask_for_required_options=True, 
                                 automatic_help_command=True)
```

## Custom Mapper

You also can define custom mappers for any type you want.\
In this example I created a custom mapper for a class named 'Node'.

```python
# class for the example
class Node(object):
    def __init__(self, x, y, name, color):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
```

Now I want to accept command line arguments to create objects of this class.\
In my case I would define the format as {x},{y},{name},{color}.\
So if the user inputs `python myscript.py --node 1,5,MyNode,#f00` it should map this input automatically to Node objects.\
So we'll write a custom mapper.

```python
from rmoptions.mapper import BaseMapper
from .node import Node

# Override the BaseMapper class from rmoptions.mapper
class NodeMapper(BaseMapper):

    # override the init function
    def __init__(self):
        BaseMapper.__init__(self)

    # override the get_target_type_name function.
    # This is needed for the error messages.
    # Simply write the name of the target class here.
    def get_target_type_name(self):
        return "Node"

    # this is the real map class. 
    # Here you'll get the value of the option, 
    # which you should parse here.
    # If it's work return the object, and if it's not working return None.
    # For multiple_values = True: If you have multiple values for an option,
    # this function will be called for every element in the value's list.
    # So you will everytime get single values in this function, and never a list.
    def map(self, value):
        try:
            value = value.split(",")
            return Node(int(value[0]),int(value[1]),value[2],value[3])
        except ValueError:
            return None

```

You also can use this mapper for multiple values.\
So it's also working for options like `python myscript.py --node 1,5,MyNode,#f00 10,15,MyNode2,#f50`

## Example

If you want to see a full project (with custom-mapper and a lot of options) with this package look here: https://github.com/MartinR2295/University-Exercises-Artificial-Intelligence/tree/main/traveling_salesman\

Easy example to start with a script
```python
from rmoptions import RMOptionHandler
from rmoptions.mapper import IntMapper

def main():
    option_handler = RMOptionHandler()
    name_option = option_handler.create_option("name", "your name", required=True)
    height_option = option_handler.create_option("height", "height of the grid in blocks",
                                                 needs_value=True, required=True, mapper=IntMapper)
    width_option = option_handler.create_option("width", "width of the grid in blocks", short_name="w",
                                                needs_value=True, required=True, mapper=IntMapper)

    if not option_handler.check():
        option_handler.print_error()
        option_handler.print_usage()
        exit()

    #do anything with the options
    area = height_option.value*width_option.value
    print("Hello {}, the calculated area is: {}".format(name_option.value, area))

if __name__ == '__main__':
    main()
```



