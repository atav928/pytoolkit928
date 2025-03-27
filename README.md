# PyToolkit

Python General tools.

**Table of Contents:**
1. [Installation](#installation)
2. [Utilities](#utilities)
   1. [Manipulating Strings](#manipulating-strings)
      1. [String to List](#string-to-list)
      2. [Camel and Snake Cases](#camel-and-snake-cases)
   2. [Dataclass Base](#dataclass-base)
   3. [Maniuplating Dictionaries](#maniuplating-dictionaries)
      1. [Search Utilities](#search-utilities)
   4. [Files](#files)

## Installation

Source: [https://pypi.org/project/pytoolkit928/](https://pypi.org/project/pytoolkit928/)

```bash
>>> python -m pip install pytoolkit928
```

## Utilities

**NOTE:** There are 2 utils files that will be fixed in later releases. Currently `pyoolkit.utils` holds basic utilities and `pytoolkit.utilities` holds primarily dataclass and dict reformat utilities.

### Manipulating Strings

#### String to List

`string_or_list` function allows you to interpret a string and return a list. Provides you the option of adding a delimeter using an OR function to return a possible string that you may be expecting possible commond delimeters. Such as: `",|:|\|, "`.

__Example:__

```bash
>>> from pytoolkit.utils import string_or_list

>>> test = 'string1,string2 string3|string4'
>>> string_or_list(test)
['string1,string2 string3|string4']
>>> string_or_list(test,delimeters=',| ')
['string1', 'string2', 'string3|string4']
>>> string_or_list(test,delimeters=',| |\|')
['string1', 'string2', 'string3', 'string4']
```

#### Camel and Snake Cases

**Camel_to_Snake Case:**

Converts camelCase into snake_case values. This funcition uses regular expressions to also handle `special characters` found in some non-standard formats.

```bash
>>> from pytoolkit.utils import camel_to_snake
>>> camel_to_snake(name='someValue.1')
'some_value1'
# To use a list of values and return them use `output='list'`
>>> camel_to_snake(name=['someValue.1', 'someValue', 'nextValue', 'lastTimeModifiedValue'], output='list')
['some_value1', 'some_value', 'next_value', 'last_time_modified_value']
```

**Snake_to_Camel Case:**

Converts snake_case values into camelCase.

```bash
>>> from pytoolkit.utils import snake_to_camel
>>> snake_to_camel(name='last_time_modified_value')
'lastTimeModifiedValue
```

### Dataclass Base

Used for basic extended functionality for dataclass declerations. Includes the ability to create a dataclass from a ``dictionary`` or from ``**kwargs``. Also, includes a conversion from ``Dataclass`` to a Python ``dictionary``.

__Usage:__

```python
from typing import Optional
from dataclasses import dataclass

from pytoolkit.utilities import BaseMonitor, NONETYPE

@dataclass
class Sample(BaseMonitor):
    key1: str
    key2: str
    key3: int
    key5: Optional[str] = NONETYPE

# create a sample module
_dict = {"key1": "value1", "key2": "value2", "key3": 3}

sample1 = Sample.create_from_dict(_dict)
sample2 = Sample.create_from_kwargs(**_dict)

print(sample1)
print(sample2)
print(sample1.to_dict())
```

__OUTPUT:__

```bash
>>> print(sample1)
Sample(key1='value1', key2='value2', key3=3, key5=<object object at 0x10c8e8b70>)
>>> print(sample2)
Sample(key1='value1', key2='value2', key3=3, key5=<object object at 0x10c8e8b70>)
>>> print(sample1.to_dict())
{'key1': 'value1', 'key2': 'value2', 'key3': 3}
```

### Maniuplating Dictionaries

__Flatten a Dictionary:__

```python
import json
from pytoolkit import utilities

sample_dict = {"key1":"value","key2": "value2", "metadata": {"key1": "meta_value1","key2":"meta_value2"}}

# Convert dictionary into a flat dictionary
flat_dict = utilities.flatten_dict(sample_dict)

# Convert dictionary back into a nested ditionary
nest_dict = utilities.nested_dict(flat_dict)

print(f"This is a Flattened Dictionary:\n{json.dumps(flat_dict,indent=1)}")
print(f"This is a Nested Dictionary:\n{json.dumps(nest_dict,indent=1)}")
```

__OUTPUT:__

```bash
This is a Flattened Dictionary:
{
 "key1": "value",
 "key2": "value2",
 "metadata.key1": "meta_value1",
 "metadata.key2": "meta_value2"
}

This is a Nested Dictionary:
{
 "key1": "value",
 "key2": "value2",
 "metadata": {
  "key1": "meta_value1",
  "key2": "meta_value2"
 }
}
```

The above is using the default `'.'` seperator value. There is a mix of commands that can be passed to adjust how the dictionary is expressed. This is useful for expressing data in otherformats that do not allow for nested dictionaries, but need a way to recreate the original formated datastructure.

__Nested Dictionary:__

__TOOD:__ Create a way to extract a CSV or XCEL file and turn it into a proper dictionary based on the type. Integrate with Splunk

__TODO:__ Add splunk HEC fromatter with proper chunck

__TODO:__ KVSTORE configuration tool.


**Sanatize dictionary data**

```python
from pytoolkit.utils import sanatize_data

test_dict = {
    "value1": "one",
    "value2": "two",
    "subvalue01": {
        "password": "welcome123",
        "username": "testuser",
    }
}

sanatized_dict = sanatize_data(data=test_dict)
print(sanatize_dict)
# {"value1": "one", "value2": "two", "subvalue01": { "password": "[MASKED]", "username": "testuser"}}
```

#### Search Utilities

`extract_matches` function allows you to extract matches and non matches from a list of strings using a conditional function.

__Sample Code:__

```python
from datetime import datetime, timezone, timedelta

from pytoolkit.utilities import extract_matches

# This function searches for data that is extracted from a file into a list and does a compare of the datetime to match values in a dataframe that are older than a certain time.
m = extract_matches(iterable=m.matches, condition=lambda x: [bool(datetime.strptime(str(x.stem).split('_', maxsplit=1)[-1],'%Y%m%dT%H%M') < datetime.now(timezone.utc) - timedelta(days=days))])

```

The aove code passes a `lambda` function that allows you to create a single or list of conditions that each line is used to search and return a match and non-match dataclass which can be exported using:

```python
m.match
m.no_match
```

### Files

Reads different file types:

* yaml
* json
* csv
* text
* ini

Read in files and manipulate them using standard functions and `pandas` library.

```python
from pytoolkit.files import readfile

```
