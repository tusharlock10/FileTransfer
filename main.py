import os
import sys

import tj

clear = "cls"
if 'win32' not in sys.platform.lower(): clear = 'clear'
c = tj.color_text

m1 = '     _  _             _  _ ___    '
m2 = '    /  / \ |\ | |\ | |_ /   |     '
m3 = '    \_ \_/ | \| | \| |_ \_  |     '
space = c('                                  ', background_color='WHITE')
border = c('                                      ', text_color='BLUE', background_color='PURPLE')
vbar = c('  ', text_color='BLUE', background_color='PURPLE')

logo = f'''
  {border}
  {vbar}{space}{vbar}
  {vbar}{c(m1, text_color='BLACK', background_color='WHITE')}{vbar}
  {vbar}{c(m2, text_color='BLACK', background_color='WHITE')}{vbar}
  {vbar}{c(m3, text_color='BLACK', background_color='WHITE')}{vbar}
  {vbar}{space}{vbar}
  {vbar}{c('        -TJ Productions (c) 2019  ', text_color='YELLOW',
           background_color='WHITE', bold=True)}{vbar}
  {vbar}{space}{vbar}
  {vbar}{c('  -- A FILE SHARING PLATFORM  --  ', text_color='YELLOW',
           background_color='WHITE', bold=True)}{vbar}
  {vbar}{space}{vbar}
  {border}

'''

main_menu = f'''
%s

 * MAIN MENU *

 1) {c('SEND FILES', text_color='GREEN', bold=True)} 
        {c('* Type 1h instead of 1, for help regarding sending files.',
           text_color='BLACK', background_color='WHITE', underline=True)}
 2) {c('RECEIVE FILES', text_color='GREEN', bold=True)} 
        {c('* Type 2h instead of 2, for help regarding receiving files.',
           text_color='BLACK', background_color='WHITE', underline=True)}
 3) {c('QUIT', text_color='RED', bold=True)}
''' % logo

msg = 'Enter your choice from 1-3: '
import sender, receiver

while 1:
    os.system(clear)
    print(main_menu)
    choice = input(msg).upper()

    if choice.upper() in ['1', '1H', '1HELP', '1 H', '1 HELP']:
        print('\n * SENDING FILES *\n')

        if choice != '1':
            sender.help_sending()

        S = sender.Sender()
        D = S.get_files_to_send()
        S.send_files_metadata(D)
        S.send_files()
        S.close()
        break

    elif choice.upper() in ['2', '2H', '2HELP', '2 H', '2 HELP']:
        print('\n * RECEIVING FILES *\n')
        if choice != '2':
            receiver.help_receiving()

        R = receiver.Receiver()
        D = R.get_files_metadata()
        R.get_files(D)
        R.close()
        break

    elif choice in ['3', 'Q', 'QUIT', 'E']:
        sender.full_exit()
    else:
        msg = 'Enter only numbers from 1-3 (or 1h or 2h): '
