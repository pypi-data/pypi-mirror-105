import linecache
import textwrap
import sys
from sys import exit

class LeavingProgram(Exception):
    pass

def parse(program):
    cmds = program.split(',')
    splitted_cmds = []
    for cmd in cmds:
        splitted = cmd.split()
        splitted_cmds.append(splitted)
    return splitted_cmds

def tokenize(s):
    return s.split()

def repl():
    while True:
        try:
            val = eval(parse(input('> ')))
            if val is not None:
                print(val)
        except LeavingProgram:
            break

text = None
line_number = 0
last_index = 0

def eval(cmds):
    global text
    global line_number
    global last_index
    global pattern

    for cmd in cmds:
        if cmd == []:
            line_number += 1
            last_index = 0

        elif cmd[0] == 'load':
            contents = open('input.txt').read()
            text = textwrap.wrap(contents, 60, break_long_words=True)
            print('\n'.join(text))
            line_number = 0
            last_index = 0

        elif cmd[0] == 'show':
            print(text[line_number])

        elif cmd[0] == 'under':
            current_line = text[line_number]
            char_number = int(cmd[1]) - 1
            char_list = list(current_line)

            x=range(last_index, char_number + last_index + 1)
            for time in x:
                if time < len(char_list):
                    char_list[time] = u'\u21e2'

            last_index += char_number + 1

            joined = ''.join(char_list)
            text[line_number] = joined

        elif cmd[0] == 'over':
            last_index += int(cmd[1])

        elif cmd[0] == 'pattern':

            pattern = text[0:line_number + 1]
            print('\n'.join(pattern))

        elif cmd[0] == 'save':
            pattern = text[0:line_number + 1]
            pattern_file = open('pattern.txt', 'w')
            pattern_file.write('\n'.join(pattern))
            pattern_file.close()
            print('Your pattern has been saved in the pattern.txt file.')

        elif cmd[0] == 'quit':
            print('Come back soon!')
            raise LeavingProgram()
        else:
            joined = ' '.join(cmd)
            print('Did not understand command {}'.format(joined))

if __name__ == '__main__':
    repl()
