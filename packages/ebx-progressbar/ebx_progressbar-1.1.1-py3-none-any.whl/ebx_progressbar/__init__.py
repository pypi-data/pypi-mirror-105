#######################################################################################
## Script Info:		ebx_progressbar.py - Class with functions to show progress Bar
##
#######################################################################################
## Create Author:	Fausto Branco
## Create Date:		2021-05-13
## Actual Version:  1.1.1
## Description:		
##############################################################################

import time
import sys
import os
from datetime import timedelta

__version__ = '1.0.0'


class progressBar:
    def __init__(self, fixed_width=0, pos_Line=0, pos_Column=0, ind_NewLine=False):
        """
        Desc: Init class with max Size(fixed_width) Line (pos_Line) and Column (pos_Column) to show progress bar, 
              and ind_NewLine that show all status update in same line (False) or in new line (True)
        """
        self.fixed_width = fixed_width
        self.pos_Line = pos_Line
        self.pos_Column = pos_Column
        self.ind_NewLine = ind_NewLine
        self.const_infSize = 34
        self.dht_Inicio = 0
        self.last_Char = ''

    def print_Running(self, int_Progress=0, str_AdditionalText='', pre_Text='', ind_Simple=False):
        """
        Desc: Progress with running format [|], [/], [-], [\], [|], [/], [-], [-], [|]
              with ind_Simple = True shows a time elapsed
              pre_Text: [-] AdditionalText
              Call this function addind the value of int_Progress to progress
        """
        if self.last_Char == '|':
            self.last_Char = '/'
        elif self.last_Char == '/':
            self.last_Char = '-'
        elif self.last_Char == '-':
            self.last_Char = '\\'
        elif self.last_Char == '\\':
            self.last_Char = '|'
        elif self.last_Char == '|':
            self.last_Char = '/'
        else:
            self.last_Char = '|'

        self.dht_Inicio = (time.time() if self.dht_Inicio == 0 else self.dht_Inicio)
        dht_Now = time.time()
        if not ind_Simple:
            if str_AdditionalText == '':
                str_Text = pre_Text + '[' + self.last_Char + '] ' + str(int_Progress) + ' [Elapsed Time: ' + ':'.join(
                    str(str(timedelta(seconds=dht_Now - self.dht_Inicio))).split('.')[:1]) + '] '
            else:
                str_Text = pre_Text + '[' + self.last_Char + '] ' + str(
                    int_Progress) + ' ' + str_AdditionalText + ' [Elapsed Time: ' + ':'.join(
                    str(str(timedelta(seconds=dht_Now - self.dht_Inicio))).split('.')[:1]) + '] '
        else:
            if str_AdditionalText == '':
                str_Text = pre_Text + '[' + self.last_Char + '] '
            else:
                str_Text = pre_Text + '[' + self.last_Char + '] ' + str_AdditionalText

        str_Text = str_Text + ('\r' if self.ind_NewLine == False else '\n')
        if self.pos_Line > 0:
            sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (self.pos_Line, self.pos_Column, str_Text))
        else:
            sys.stdout.write(str_Text)
        sys.stdout.flush()

    def print_Bar(self, int_Progress=0, pre_Text=''):
        """
        Desc: Progress with commom format: pre_Text [Elapsed Time: 0:00:04] [####################################                                                        ] (40%)
              Call this function addind the value of int_Progress to progress
        """
        max_Rows, max_Columns = os.popen('stty size', 'r').read().split()
        max_Columns = int(max_Columns) - self.pos_Column - len(pre_Text)
        if self.fixed_width > max_Columns:
            self.fixed_width = max_Columns - 1
        self.dht_Inicio = (time.time() if self.dht_Inicio == 0 else self.dht_Inicio)
        dht_Now = time.time()
        if self.fixed_width > 0:
            int_Step = round((self.fixed_width - self.const_infSize)) / float(100)
        else:
            int_Step = round((int(max_Columns) - self.fixed_width - self.const_infSize)) / float(100)

        if int(max_Columns) - self.fixed_width >= 0:
            if int_Step * int_Progress > (int(max_Columns) - self.const_infSize) or int_Progress >= 100:
                int_Progress = 100
                if self.fixed_width > 0:
                    int_StepProgress = self.fixed_width - self.const_infSize
                    str_Text = pre_Text + ' [Elapsed Time: ' + ':'.join(
                        str(str(timedelta(seconds=dht_Now - self.dht_Inicio))).split('.')[:1]) + '] [' + '#' * int(
                        int_StepProgress) + ' ' * (int(self.fixed_width - self.const_infSize) - int(
                        int_StepProgress)) + '] (' + str(int_Progress) + '%)'
                else:
                    int_StepProgress = int(max_Columns) - self.const_infSize - self.fixed_width
                    str_Text = pre_Text + ' [Elapsed Time: ' + ':'.join(
                        str(str(timedelta(seconds=dht_Now - self.dht_Inicio))).split('.')[:1]) + '] [' + '#' * int(
                        int_StepProgress) + ' ' * int(round(
                        (int(max_Columns) - self.fixed_width - self.const_infSize) - int(
                            int_StepProgress))) + '] (' + str(int_Progress) + '%)'
            else:
                if self.fixed_width > 0:
                    int_StepProgress = int_Step * int_Progress
                    str_Text = pre_Text + ' [Elapsed Time: ' + ':'.join(
                        str(str(timedelta(seconds=dht_Now - self.dht_Inicio))).split('.')[:1]) + '] [' + '#' * int(
                        int_StepProgress) + ' ' * (int(self.fixed_width - self.const_infSize) - int(
                        int_StepProgress)) + '] (' + str(int_Progress) + '%)'
                else:
                    int_StepProgress = int_Step * int_Progress
                    str_Text = pre_Text + ' [Elapsed Time: ' + ':'.join(
                        str(str(timedelta(seconds=dht_Now - self.dht_Inicio))).split('.')[:1]) + '] [' + '#' * int(
                        int_StepProgress) + ' ' * int(round(
                        (int(max_Columns) - self.fixed_width - self.const_infSize) - int(
                            int_StepProgress))) + '] (' + str(int_Progress) + '%)'
            str_Text = str_Text + ('\r' if self.ind_NewLine == False else '\n')
            if self.pos_Line > 0:
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (self.pos_Line, self.pos_Column, str_Text))
            else:
                sys.stdout.write(str_Text)
        else:
            str_Text = pre_Text + ' [Elapsed Time: ' + ':'.join(
                str(str(timedelta(seconds=dht_Now - self.dht_Inicio))).split('.')[:1]) + '] (' + str(
                int_Progress) + '%)'
            str_Text = str_Text + ('\r' if not self.ind_NewLine else '\n')
            if self.pos_Line > 0:
                sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (self.pos_Line, self.pos_Column, str_Text))
            else:
                sys.stdout.write(str_Text)
        sys.stdout.flush()

    def reset(self):
        self.dht_Inicio = 0
