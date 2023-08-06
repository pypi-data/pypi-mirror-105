# Print Box

Class with functions to delimit a box on screen (With a border or not) and print strictly inside the created box, with scroll to the new lines.

### Prerequisites

Developed and tested in Linux and Python 3.6


### Installing

    pip3 install ebx_printbox

or from source:

    python3 -m pip install [your_path]/ebx_printbox/



## Functions
### pyBox

pyBox(x, y, x2, y2, border=False, clear_screen=False):

**Description**: Create a instance of a box, with sizes, border and information if will perform a clear screen

|Parameter|Description|
|---|---|
|**x**:|Line of box beginning on screen|
|**y**:|Column of box beginning on screen|
|**x2**:|Line of box end on screen|
|**y2**:|Column of box end on screen|
|**border**:|Draw a border (will reduce 2 lines and 2 columns of useful box)|
|**clear_screen**:|Clear screen before draw a box|

Return: Box object

---


### box_clear

box_clear()

**Description**: Clear buffer. Necessary on new print calls

Return: None

---

### box_print

box_print(txt_String, new_Line=True):

**Description**: Print anything on a delimited box created by pyBox()

|Parameter|Description|
|---|---|
|**txt_String**:|Text to print (accept Text_Color contants)|
|**new_Line**:|Print on new line (True) or over last line (False)|
  
Return: None
              

## Examples of use

**example1.py**

```
import ebx_printbox
from time import sleep

# Box(Line:16, Column: 1 to Line: 52, Column: 120 - No Border, No Clear Screen)
obj_Box1 = ebx_printbox.pyBox(16, 1, 52, 120, False, True)
obj_Box1.create_box()

for i in range(501):
    obj_Box1.box_print('Text: ' + str(
        i) + ' Lorem ipsum dolor sit amet, ad suas sale eam, falli suavitate corrumpit an sit. Latine viderer ex vis. '
             'Ex maiorum fuisset aliquando vix, in cum dicant gloriatur. Ei elit argumentum cum, quod blandit an eum.')
    sleep(1)  # Time in seconds.

```

### Results:

[![asciicast](https://asciinema.org/a/414005.svg)](https://asciinema.org/a/414005)

---

**example2.py**
```
import ebx_printbox
from time import sleep


class text_color:
    fg_Black = "\033[0;30m"
    fg_Red = "\033[0;31m"
    fg_Green = "\033[0;32m"
    fg_Yellow = "\033[0;33m"
    fg_Blue = "\033[0;34m"
    fg_Magenta = "\033[0;35m"
    fg_Cyan = "\033[0;36m"
    fg_White = "\033[0;37m"
    fg_Bright_Black = "\033[0;90m"
    fg_Bright_Red = "\033[0;91m"
    fg_Bright_Green = "\033[0;92m"
    fg_Bright_Yellow = "\033[0;93m"
    fg_Bright_Blue = "\033[0;94m"
    fg_Bright_Magenta = "\033[0;95m"
    fg_Bright_Cyan = "\033[0;96m"
    fg_Bright_White = "\033[0;97m"
    text_reverse = "\033[;7m"
    text_underline = "\033[1;4m"
    text_reset_underline = "\033[1;24m"
    text_reset = "\033[0;0m"
    bg_Black = "\033[1;40m"
    bg_Red = "\033[1;41m"
    bg_Green = "\033[1;42m"
    bg_Yellow = "\033[1;43m"
    bg_Blue = "\033[1;44m"
    bg_Magenta = "\033[1;45m"
    bg_Cyan = "\033[1;46m"
    bg_White = "\033[1;47m"
    bg_Bright_Black = "\033[1;100m"
    bg_Bright_Red = "\033[1;101m"
    bg_Bright_Green = "\033[1;102m"
    bg_Bright_Yellow = "\033[1;103m"
    bg_Bright_Blue = "\033[1;104m"
    bg_Bright_Magenta = "\033[1;105m"
    bg_Bright_Cyan = "\033[1;106m"
    bg_Bright_White = "\033[1;107m"


obj_Box1 = ebx_printbox.pyBox(16, 1, 20, 120, False, True)
obj_Box1.create_box()

num_IP = dict()
num_IP['DC'] = 'dc-1'
num_IP['IP'] = '192.168.1.1'

for i in range(15):
    obj_Box1.box_print(
        '[' + text_color.fg_Bright_Red + 'BACKUPING ' + text_color.text_reset + '] JVM on %s  -  %s \r' % (
            '192.168.1.' + str(i), num_IP['IP']), True)
    sleep(1)  # Time in seconds.
    obj_Box1.box_print(
        '[' + text_color.fg_Bright_Red + 'CHANGING  ' + text_color.text_reset + '] JVM on %s  -  %s \r' % (
            '192.168.1.' + str(i), num_IP['IP']), False)
    sleep(1)  # Time in seconds.
    obj_Box1.box_print(
        '[' + text_color.fg_Bright_Red + 'APPLYING  ' + text_color.text_reset + '] JVM on %s  -  %s \r' % (
            '192.168.1.' + str(i), num_IP['IP']), False)
    sleep(1)  # Time in seconds.
    obj_Box1.box_print(
        '[' + text_color.fg_Green + 'RESTARTING' + text_color.text_reset + '] JVM on %s  -  %s \r' % (
            '192.168.1.' + str(i), num_IP['IP']), False)
    sleep(1)  # Time in seconds.


```

### Results:

[![asciicast](https://asciinema.org/a/414011.svg)](https://asciinema.org/a/414011)

---

##Multiprocessing
**example3.py** - 2 Boxes with multiprocessing
```
import ebx_printbox
from multiprocessing import Process
from time import sleep
import os

lst_ObjBox = []
lst_Process = []

# Box(Line:30, Column: 10 to Line: 40, Column: 100 - No Border, Clear Screen)
lst_ObjBox.append(ebx_printbox.pyBox(30, 10, 40, 100, False, True))
lst_ObjBox[0].create_box()

# Box(Line:10, Column: 70 to  Line: 25, Column: 120 - With Border, No Clear Screen)
lst_ObjBox.append(ebx_printbox.pyBox(10, 70, 25, 120, True, False))
lst_ObjBox[1].create_box()


def multi_Box(int_Box):
    for i in range(50):
        lst_ObjBox[int_Box].box_print('Texto: ' + str(i) + ' - Process: ' + str(
            os.getpid()) + ' Lorem ipsum dolor sit amet, ad suas sale eam, falli suavitate corrumpit an sit. Latine '
                           'viderer ex vis. Ex maiorum fuisset aliquando vix, in cum dicant gloriatur. Ei elit '
                           'argumentum cum, quod blandit an eum.')
        sleep(1)  # Time in seconds.


for index in range(2):
    obj_Process = Process(target=multi_Box, args=(index,))
    lst_Process.append(obj_Process)
    obj_Process.start()

# Exit the completed processes
for obj_Process in lst_Process:
    obj_Process.join()

     
```

###Results:

[![asciicast](https://asciinema.org/a/414012.svg)](https://asciinema.org/a/414012)

---

## Versioning
```
=======================================================================================
== Log Changes:
== Date:            2021-05-13
== Author:          Fausto Branco
== Version:         1.0.0
== Description:     Initial Version
=======================================================================================
```

## License




