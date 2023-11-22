# PyToolkit

Python General tools

## Utilities

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
