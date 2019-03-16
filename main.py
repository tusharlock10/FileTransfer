import os
import sys

import tj

clear = "cls"
if 'win32' not in sys.platform.lower(): clear = 'clear'

logo = r'''
----------------------------------+
   ___                            |                _     
  / __|    ___    _ _     _ _      ___     __     | |_   
 | (__    / _ \  | ' \   | ' \    / -_)   / _|    |  _|  
  \___|   \___/  |_||_|  |_||_|   \___|   \__|_   _\__|  
_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
                                  |
        -TJ Productions (c) 2019  |
                                  |
  -- A FILE SHARING PLATFORM  --  |
----------------------------------+


'''

main_menu = '''
%s

 * MAIN MENU *

 1) SEND FILES 
        * Type 1h instead of 1, for help regarding sending files.
 2) RECEIVE FILES 
        * Type 2h instead of 2, for help regarding receiving files.
 3) QUIT
''' % logo

msg = 'Enter your choice from 1-3: '
while 1:
    os.system(clear)
    print(main_menu)
    choice = input(msg).upper()

    if choice.upper() in ['1', '1H', '1HELP', '1 H', '1 HELP']:
        print('\n * SENDING FILES *\n')
        import sender

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
        import receiver

        if choice != '2':
            receiver.help_receiving()

        R = receiver.Receiver()
        D = R.get_files_metadata()
        R.get_files(D)
        R.close()
        break

    elif choice in ['3', 'Q', 'QUIT', 'E']:
        print()
        bye = tj.color_text('  * GOOD BYE *  ', text_color='PURPLE', background_color='WHITE')
        print(bye)
        input('Enter to quit...')
        break
    else:
        msg = 'Enter only numbers from 1-3 (or 1h or 2h): '
