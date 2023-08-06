#######################################################################################
## Script Info:		ebx_printbox.py - Class with functions to create a virtual ebx_printbox on screen and print on then
##
#######################################################################################
## Create Author:	Fausto Branco
## Create Date:		2021-05-14
## Actual Version:  1.0.2
## Description:		
#######################################################################################


import sys
import os
import collections

__version__ = '1.0.1'


class pyBox:
    def __init__(self, x, y, x2, y2, border=False, clear_screen=False):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.border = border
        self.clear_screen = clear_screen
        self.lst_printedLines = collections.deque(
            maxlen=self.x2 - self.x + 1 if self.border == False else (self.x2 - self.x) - 1)

    def get_limits(self):
        rows, columns = os.popen('stty size', 'r').read().split()
        # self.max_rows = int(rows)
        # self.max_columns = int(columns)
        pyBox.__dict__['get_limits'].max_rows = int(rows)
        pyBox.__dict__['get_limits'].max_columns = int(columns)
        return self.get_limits

    def print_there(x, y, text):
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
        sys.stdout.flush()

    def create_box(self):
        obj_Limits = self.get_limits()
        if self.x <= 0 or self.x2 <= 0 or self.y <= 0 or self.y2 <= 0:
            return 'Err: Box size must be in screen limits: (' + str(obj_Limits.max_rows) + ' rows x ' + str(
                obj_Limits.max_columns) + ' columns).'
        if self.x2 < self.x:
            return 'Err: Start Line must by lower than finish line.'
        if self.y2 < self.y:
            return 'Err: Start Column must by lower than finish Column.'
        if self.x > obj_Limits.max_rows:
            return 'Err: Start line must by lower than screen limits: (' + str(obj_Limits.max_rows) + ' rows x ' + str(
                obj_Limits.max_columns) + ' columns).'
        if self.x2 > obj_Limits.max_rows:
            return 'Err: Finish line must by lower than screen limits: (' + str(obj_Limits.max_rows) + ' rows x ' + str(
                obj_Limits.max_columns) + ' columns).'
        if self.y > obj_Limits.max_columns:
            return 'Err: Start Column must by lower than screen limits: (' + str(
                obj_Limits.max_rows) + ' rows x ' + str(obj_Limits.max_columns) + ' columns).'
        if self.y2 > obj_Limits.max_columns:
            return 'Err: Finish Column must by lower than screen limits: (' + str(
                obj_Limits.max_rows) + ' rows x ' + str(obj_Limits.max_columns) + ' columns).'
        if self.clear_screen:
            print(chr(27) + "[2J")
        else:
            for int_Line in range(self.x, self.x2 + 1):
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (int_Line, self.y, ' ' * (self.y2 - self.y)))
                sys.stdout.flush()
        if self.border:
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (self.x, self.y, '-' * (self.y2 - self.y)))
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (self.x2, self.y, '-' * (self.y2 - self.y)))
            for int_Line in range(self.x + 1, self.x2):
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (int_Line, self.y, '|'))
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (int_Line, self.y2, '|'))
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (self.x, self.y, '+'))
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (self.x, self.y2, '+'))
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (self.x2, self.y, '+'))
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (self.x2, self.y2, '+'))
            sys.stdout.flush()

    def box_clear(self):
        self.lst_printedLines = collections.deque(
            maxlen=self.x2 - self.x + 1 if self.border == False else (self.x2 - self.x) - 1)

    def box_print(self, txt_String, new_Line=True):
        if new_Line:
            self.lst_printedLines.append(txt_String)
        else:
            self.lst_printedLines[-1] = txt_String
        for int_Linha in range(len(self.lst_printedLines)):
            sys.stdout.write("\x1b7\x1b[%d;%df%s" % (
                self.x + int_Linha if self.border == False else (self.x + int_Linha) + 1,
                self.y if self.border == False else self.y + 1,
                (self.lst_printedLines[int_Linha][:self.y2 - self.y]) if self.border == False else (
                    self.lst_printedLines[int_Linha][:(self.y2 - self.y) - 2])))
            sys.stdout.flush()
