# Key Press

Python package for capture and return keypress.

### Prerequisites

Developed and tested in Linux and Python 3


### Installing

    pip3 install ebx_keypress

or from source:

    python3 -m pip install [your_path]/ebx_keypress/


## Functions

### keypress

keypress():
Description: Capture pressed keys and combined keys and return as string

Return: String with pressed key

## Examples of use

```
import ebx_keypress

result_Keypress = ''

obj_keypress = ebx_keypress.Get_Key()

print("Press keys or Ctrl+C to Exit")

while result_Keypress != 'Ctrl+ C':
    result_Keypress = obj_keypress.keypress()
    print(result_Keypress)

    
```

## Versioning
```
=======================================================================================
== Log Changes: 
== Date:            2021-05-12
== Author:          Fausto Branco
== Version:         1.1.0
== Description:     Initial Version
=======================================================================================

```




