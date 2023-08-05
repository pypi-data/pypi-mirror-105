#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOT IN USE, IS IN GENERAL!!! Igual hay que separarla
from __future__ import unicode_literals
from __future__ import print_function
from collections import deque
import os
import io


class Reader:
    def __init__(self, filename):
        basename = os.path.basename(filename)
        self.caseName = os.path.splitext(basename)[0]
        self.f = io.open(filename, 'r', encoding="utf-8")
        self._iline = 0
        self.stackOut = deque()
        self.lastLine = " "

    def __call__(self, endText):
        # Una llamada para agregar el texto y que después llame al iterador
        self.stackOut.append(endText)
        return self

    def __iter__(self):
        return self

    def __next__(self):
        try:
            line = self.f.readline()
            if not line:
                raise StopIteration
            self._iline += 1
            # print(str(self._iline) + ": " + line.strip())
            line = line.strip()

            # Para saltarse los comentarios
            if line.startswith('$'):
                return self.__next__()
            line = line.split('!')[0].strip()

            # Para las continuaciones de linea
            if line.endswith('\\'):
                secondLine = self.__next__()
                line = line[:-1] + " " + secondLine
            self.lastLine = line
            # Comprueba si se cierra el sector
            if self.stackOut[-1] in line:
                self.stackOut.pop()
                raise StopIteration
        except StopIteration:
            raise
        except Exception:
            print("Error in line: " + str(self._iline))
            raise
        return line
    next = __next__

    def lineNum(self):
        return self._iline
