#######################################################################################
## Script Info:		ebx_keypress.py - Class with functions to capture pressed keys
##
#######################################################################################
## Create Author:	Fausto Branco
## Create Date:		2021-05-12
## Actual Version:  1.1.0
## Description:
#######################################################################################

import signal
import sys
import tty
import termios

__version__ = '1.1.0'


class Get_Key:
    def _getch(self, keylen=1):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(keylen)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def _handler(self, signum, frame):
        raise Exception('Timeout')

    def keypress(self):
        """
        Desc: ebx_keypress: Return a string with description os pressed key; Ex: Up, Down, Ctrl+ Up, etc
        """
        ret_keypress = ''
        # while True:
        char = self._getch()
        if char == '\x11':
            ret_keypress = 'Ctrl+ Q'
        elif char == '\x17':
            ret_keypress = 'Ctrl+ W'
        elif char == '\x05':
            ret_keypress = 'Ctrl+ E'
        elif char == '\x12':
            ret_keypress = 'Ctrl+ R'
        elif char == '\x14':
            ret_keypress = 'Ctrl+ T'
        elif char == '\x19':
            ret_keypress = 'Ctrl+ Y'
        elif char == '\x15':
            ret_keypress = 'Ctrl+ U'
        elif char == '\x0f':
            ret_keypress = 'Ctrl+ O'
        elif char == '\x10':
            ret_keypress = 'Ctrl+ P'
        elif char == '\x01':
            ret_keypress = 'Ctrl+ A'
        elif char == '\x13':
            ret_keypress = 'Ctrl+ S'
        elif char == '\x04':
            ret_keypress = 'Ctrl+ D'
        elif char == '\x06':
            ret_keypress = 'Ctrl+ F'
        elif char == '\x07':
            ret_keypress = 'Ctrl+ G'
        elif char == '\x08':
            ret_keypress = 'Ctrl+ H'
        elif char == '\x0a':
            ret_keypress = 'Ctrl+ J'
        elif char == '\x0b':
            ret_keypress = 'Ctrl+ K'
        elif char == '\x0c':
            ret_keypress = 'Ctrl+ L'
        elif char == '\x1a':
            ret_keypress = 'Ctrl+ Z'
        elif char == '\x18':
            ret_keypress = 'Ctrl+ X'
        elif char == '\x03':
            ret_keypress = 'Ctrl+ C'
        elif char == '\x16':
            ret_keypress = 'Ctrl+ V'
        elif char == '\x02':
            ret_keypress = 'Ctrl+ B'
        elif char == '\x0e':
            ret_keypress = 'Ctrl+ N'
        elif char == '\x20':
            ret_keypress = 'Space'
        elif char == '\r':
            ret_keypress = 'Enter'
        elif char == '\t':
            ret_keypress = 'Tab'
        elif char in '\x1b':
            signal.signal(signal.SIGALRM, self._handler)
            signal.setitimer(signal.ITIMER_REAL, 0.25)
            try:
                next_char = self._getch()
            except:
                signal.setitimer(signal.ITIMER_REAL, 0)
                ret_keypress = 'Esc'
            else:
                signal.setitimer(signal.ITIMER_REAL, 0)
                if next_char in '[O' or next_char in '\x1b':
                    if next_char == 'O':
                        next_char = self._getch()
                        if next_char == 'P':
                            ret_keypress = ret_keypress + 'F1'
                            return ret_keypress
                        elif next_char == 'Q':
                            ret_keypress = ret_keypress + 'F2'
                            return ret_keypress
                        elif next_char == 'R':
                            ret_keypress = ret_keypress + 'F3'
                            return ret_keypress
                        elif next_char == 'S':
                            ret_keypress = ret_keypress + 'F4'
                            return ret_keypress
                        else:
                            ret_keypress = 'Ctrl+ '
                    elif next_char == '[':
                        next_char = self._getch()
                        if next_char == 'F':
                            ret_keypress = ret_keypress + 'End'
                        elif next_char == '5' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'Page Up'
                        elif next_char == '6' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'Page Down'
                        elif next_char == 'H':
                            ret_keypress = ret_keypress + 'Home'
                        elif next_char == '3' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'Delete'
                        elif next_char == '1':
                            next_char = self._getch()
                            if next_char == '~':
                                ret_keypress = ret_keypress + 'Home'
                            elif next_char == '1' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F1'
                            elif next_char == '2' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F2'
                            elif next_char == '3' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F3'
                            elif next_char == '4' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F4'
                            elif next_char == '5' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F5'
                            elif next_char == '7' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F6'
                            elif next_char == '8' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F7'
                            elif next_char == '9' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F8'
                        elif next_char == '2':
                            next_char = self._getch()
                            if next_char == '~':
                                ret_keypress = ret_keypress + 'Insert'
                            elif next_char == '0' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F9'
                            elif next_char == '1' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F10'
                            elif next_char == '3' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F11'
                            elif next_char == '4' and self._getch() == '~':
                                ret_keypress = ret_keypress + 'F12'
                        elif next_char == 'A':
                            ret_keypress = ret_keypress + 'Up'
                        elif next_char == 'B':
                            ret_keypress = ret_keypress + 'Down'
                        elif next_char == 'D':
                            ret_keypress = ret_keypress + 'Left'
                        elif next_char == 'C':
                            ret_keypress = ret_keypress + 'Right'
                        return ret_keypress
                    elif next_char == '\x1b':
                        next_char = self._getch()
                        if next_char == 'O':
                            ret_keypress = 'Ctrl+ '
                        ret_keypress = ret_keypress + 'Alt+ '
                    next_char = self._getch()
                    if next_char == 'A':
                        ret_keypress = ret_keypress + 'Up'
                    elif next_char == 'B':
                        ret_keypress = ret_keypress + 'Down'
                    elif next_char == 'D':
                        ret_keypress = ret_keypress + 'Left'
                    elif next_char == 'C':
                        ret_keypress = ret_keypress + 'Right'
                    elif next_char == '1':
                        next_char = self._getch()
                        if next_char == '~':
                            ret_keypress = ret_keypress + 'Home'
                        elif next_char == '1' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F1'
                        elif next_char == '2' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F2'
                        elif next_char == '3' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F3'
                        elif next_char == '4' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F4'
                        elif next_char == '5' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F5'
                        elif next_char == '7' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F6'
                        elif next_char == '8' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F7'
                        elif next_char == '9' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F8'
                    elif next_char == '2':
                        next_char = self._getch()
                        if next_char == '~':
                            ret_keypress = ret_keypress + 'Insert'
                        elif next_char == '0' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F9'
                        elif next_char == '1' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F10'
                        elif next_char == '3' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F11'
                        elif next_char == '4' and self._getch() == '~':
                            ret_keypress = ret_keypress + 'F12'
                    elif next_char == '3':
                        next_char = self._getch()
                        if next_char == '~':
                            ret_keypress = ret_keypress + 'Delete'
                    elif next_char == '4':
                        next_char = self._getch()
                        if next_char == '~':
                            ret_keypress = ret_keypress + 'End'
                    elif next_char == '6':
                        next_char = self._getch()
                        if next_char == '~':
                            ret_keypress = ret_keypress + 'Page Down'
                    elif next_char == '5':
                        next_char = self._getch()
                        if next_char == '~':
                            ret_keypress = ret_keypress + 'Page Up'
        else:
            ret_keypress = ret_keypress + char
        return ret_keypress
