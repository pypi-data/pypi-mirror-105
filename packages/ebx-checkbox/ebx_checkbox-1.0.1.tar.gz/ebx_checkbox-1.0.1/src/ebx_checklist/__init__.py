#######################################################################################
## Script Info:		ebx_checklist.py - Class with functions to make Checkbox and ListBox
##
#######################################################################################
## Create Author:	Fausto Branco
## Create Date:		2021-05-13
## Actual Version:  1.0.1
## Description:		
#####################################################################

import sys
import signal
import tty

__version__ = '1.0.1'
int_InitialLine = 10
int_CurrentLine = 0
lst_Char_Check = [' ', 'X']  # Always on Order (unchecked, Checked)
lst_Char_Option = [' ', 'O']  # Always on Order (unchecked, Checked)
str_Title = ''
lst_Options = []
lst_Options_sets = []
int_LimitLine = 0
int_InitialColumn = 0
ind_Origem = 0
ind_ClearLine = True

call_int_Acao = 0
call_str_Title = ''
call_InitialLine = 0
call_InitialColumn = 0

int_SizeLimit = 10
int_LineStartPrint = 16

int_posTOP = 0
int_posDOWN = int_posTOP + int_SizeLimit


class Options:
    class _text_colors:
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

    class _Getch:
        """Gets a single character from standard input.  Does not echo to the screen."""

        def __init__(self):
            self.impl = Options()._GetchUnix()

        def __call__(self): return self.impl()

    class _GetchUnix:
        def __init__(self):
            pass

        def __call__(self):
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    def _handler(self, signum, frame):
        raise Exception('Timeout')

    def _get_Options(self):
        # global lst_Options_sets
        # lst_Options_sets = [0] * len(Options)
        getch = self._Getch()
        while True:
            char = getch()
            if char == '\x03':
                break
            elif char in '\r':
                break
            elif char in '\x01':
                if ind_Origem in [1]:
                    self._set_All(1)
            elif char in '\x0e':
                if ind_Origem in [1]:
                    self._set_All(0)
            elif char in ' ':
                self._set_Choice()
            elif char in '\x1b':
                signal.signal(signal.SIGALRM, self._handler)
                signal.setitimer(signal.ITIMER_REAL, 0.25)
                try:
                    next_char = getch()
                except:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    return -1
                else:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    if next_char == '[':
                        next_char = getch()
                        if next_char == 'A':
                            self._set_Navigate(-1)
                        elif next_char == 'B':
                            self._set_Navigate(1)

    def _print_Cursor(self, int_Position):
        # print int_Position
        # print lst_Options
        # print lst_Options_sets
        if ind_Origem in [1]:
            lst_Char_Print = lst_Char_Check[:]
        else:
            lst_Char_Print = lst_Char_Option[:]
        # for line, item in enumerate(lst_Options):
        for line, item in enumerate(range(int_posTOP, int_posDOWN)):
            if line == int_Position:
                sys.stdout.write(self._text_colors.fg_Bright_Black + self._text_colors.bg_Bright_Green)
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (
                    int_InitialLine + line, int_InitialColumn + 6, lst_Char_Print[lst_Options_sets[item]]))
            else:
                sys.stdout.write(self._text_colors.text_reset)
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (
                    int_InitialLine + line, int_InitialColumn + 6, lst_Char_Print[lst_Options_sets[item]]))
        sys.stdout.flush()
        sys.stdout.write(self._text_colors.text_reset)
        sys.stdout.flush()

    def _set_Navigate(self, Action):
        global int_CurrentLine
        global lst_Options
        int_CurrentLine = int_CurrentLine + Action
        if int_CurrentLine < 0:
            self._get_CheckList_Slice(-1, call_str_Title, call_InitialLine, call_InitialColumn,
                                      lst_Options, ClearLine=ind_ClearLine,
                                      Options_sets=lst_Options_sets)
            int_CurrentLine = 0
        if int_CurrentLine > int_SizeLimit - 1:
            lst_HostsCheck = self._get_CheckList_Slice(1, call_str_Title, call_InitialLine, call_InitialColumn,
                                                       lst_Options, ClearLine=ind_ClearLine,
                                                       Options_sets=lst_Options_sets)
            int_CurrentLine = int_SizeLimit - 1
        self._print_Cursor(int_CurrentLine)

    def _set_All(self, Action):
        global lst_Options_sets
        lst_Options_sets = [Action] * len(lst_Options_sets)
        self._set_Navigate(0)

    def _set_Choice(self):
        global int_CurrentLine
        global lst_Options_sets
        if ind_Origem in [2]:
            lst_Options_sets = [0] * len(lst_Options_sets)
        if lst_Options_sets[int_CurrentLine + int_posTOP] == 0:
            lst_Options_sets[int_CurrentLine + int_posTOP] = 1
        else:
            lst_Options_sets[int_CurrentLine + int_posTOP] = 0
        self._print_Cursor(int_CurrentLine)

    def _get_CheckList_Slice(self, int_Acao, str_Title, InitialLine, InitialColumn, Options, ClearLine=True,
                             Options_sets=[], pos_Lista=0):  # int_Acao, par_lst_Print, pos_Lista=0):
        global int_posTOP
        global int_posDOWN
        global int_CurrentLine
        global lst_Options_sets
        global int_LimitLine
        global lst_Options
        global int_InitialColumn
        global int_InitialLine
        global call_int_Acao
        global call_str_Title
        global call_InitialLine
        global call_InitialColumn

        call_int_Acao = int_Acao
        call_str_Title = str_Title
        call_InitialLine = InitialLine
        call_InitialColumn = InitialColumn

        int_InitialLine = InitialLine
        int_InitialColumn = InitialColumn
        lst_Options = Options
        if len(Options_sets) == 0:
            lst_Options_sets = [0] * len(Options)
        else:
            lst_Options_sets = Options_sets[:]
        int_LimitLine = len(lst_Options) - 1
        # Print list par_lst_Print on screen from int_LineStartPrint to int_SizeLimit
        int_posTOP += int_Acao
        int_posDOWN += int_Acao
        if int_posTOP < 0:
            int_posTOP = 0
            int_posDOWN = int_posTOP + int_SizeLimit
        if int_posTOP + int_SizeLimit >= len(Options):
            if len(Options) < int_SizeLimit:
                int_posTOP = 0
            else:
                int_posTOP = len(Options) - int_SizeLimit
            int_posDOWN = len(Options)
        if pos_Lista == -1:
            int_CurrentLine = 0
            int_posTOP = 0
            int_posDOWN = int_posTOP + int_SizeLimit
        elif pos_Lista == 1:
            if len(Options) < int_SizeLimit:
                int_posTOP = 0
            else:
                int_posTOP = len(Options) - int_SizeLimit
            int_posDOWN = int_posTOP + int_SizeLimit
        if int_posDOWN > len(Options):
            int_posDOWN = len(Options)
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (int_InitialLine, int_InitialColumn + 2, str_Title))
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (int_InitialLine + 1, int_InitialColumn + 2, ' '))
        int_InitialLine = int_InitialLine + 2
        # Get Max len of each item
        lst_Maxlength = [max([len(item) for item in Options])]
        str_fmt = ' '.join('{:<%d}' % (l + 9) for l in lst_Maxlength)
        for idx, i in enumerate(range(int_posTOP, int_posDOWN)):
            if ClearLine:
                sys.stdout.write("\033[" + str(int_InitialLine + idx) + ";1H\033[K")
            if ind_Origem == 1:
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (
                    int_InitialLine + idx, int_InitialColumn + 2, '   [ ] - ' + str_fmt.format(Options[i])))
            else:
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (
                    int_InitialLine + idx, int_InitialColumn + 2, '   ( ) - ' + str_fmt.format(Options[i])))
            sys.stdout.flush()

    def get_CheckList(self, str_Title, InitialLine, InitialColumn, SizeLimit, Options, ClearLine=True, Options_sets=[]):
        """
        Desc: get_CheckList: Create a list of checkBox and multiple choices, return a list of 1 (check) and 0 (uncheck) for all itens (on same order) of Options parameter
        Ctrl+A To check entire list
        Ctrl+N To uncheck entire list
        str_Title: Title of the list
        InitialLine: First line on screen where the list will br printed
        InitialColumn: Column on screen where the list will br printed 
        SizeLimit: Limit (quantity) in lines that will be shown on screen, navigation is by Up and Down arrows
        Options: List of itens to be printed
        ClearLine: (True or False) Clear entire line before print?
        Options_sets: (Optional) List of predefined choices (mark) of 1 (Checked) or 0 (Unchecked). The list must have same len of Options, and set 1 on index that you want show checked
        Return: List of 1 (check) and 0 (uncheck) for all itens (on same order) of Options parameter
        """
        global int_SizeLimit
        global int_posTOP
        global int_posDOWN
        global ind_Origem
        global ind_ClearLine

        ind_Origem = 1
        ind_ClearLine = ClearLine

        int_SizeLimit = SizeLimit
        if int_SizeLimit > len(Options):
            int_SizeLimit = len(Options)
        int_posTOP = 0
        int_posDOWN = int_posTOP + int_SizeLimit

        self._get_CheckList_Slice(0, str_Title, InitialLine, InitialColumn, Options, ClearLine,
                                  Options_sets=Options_sets, pos_Lista=-1)
        self._set_Navigate(0)
        retorno = self._get_Options()
        if retorno == -1:
            return -1
        else:
            return lst_Options_sets

    def get_OptionList(self, str_Title, InitialLine, InitialColumn, SizeLimit, Options, ClearLine=True,
                       Options_Index=-1):
        """
        Desc: get_OptionList: Create a list of OptionBox and only one choice, return a list of 1 (check) and 0 (uncheck) for all itens (on same order) of Options parameter
        str_Title: Title of the list
        InitialLine: First line on screen where the list will br printed
        InitialColumn: Column on screen where the list will br printed 
        SizeLimit: Limit (quantity) in lines that will be shown on screen, navigation is by Up and Down arrows
        Options: List of itens to be printed
        ClearLine: (True or False) Clear entire line before print?
        Options_Index: (Optional) Index of predefined choice (mark) of 1 (Checked) or 0 (Unchecked). 
        Return: List of 1 (check) and 0 (uncheck) for all itens (on same order) of Options parameter
        """

        global int_SizeLimit
        global int_posTOP
        global int_posDOWN
        global ind_Origem
        global ind_ClearLine

        ind_Origem = 2
        ind_ClearLine = ClearLine

        Options_sets = [0] * len(Options)
        if Options_Index >= 0:
            Options_sets[Options_Index] = 1

        int_SizeLimit = SizeLimit
        if int_SizeLimit > len(Options):
            int_SizeLimit = len(Options)
        int_posTOP = 0
        int_posDOWN = int_posTOP + int_SizeLimit

        self._get_CheckList_Slice(0, str_Title, InitialLine, InitialColumn, Options, ClearLine,
                                  Options_sets=Options_sets, pos_Lista=-1)
        self._set_Navigate(0)
        retorno = self._get_Options()
        if retorno == -1:
            return -1
        else:
            return lst_Options_sets
