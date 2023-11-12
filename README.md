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

__Nested Dictionary:__

__TOOD:__ Create a way to extract a CSV or XCEL file and turn it into a proper dictionary based on the type. Integrate with Splunk

__TODO:__ Add splunk HEC fromatter with proper chunck

__TODO:__ KVSTORE configuration tool.

## Releases

### v0.0.4

* Added Flatten Dictionary function.
* Added Hostname and FQDN System Hostname return.
* Added grabbing current username.

### v0.0.3

* Added delimeter option.
  * Allows you to specify the delimeter you want to use using an OR operation with `|`.
* __WARNING:__ this changes the default behavior to the original intent of turning a string to a string without using the default split(',').