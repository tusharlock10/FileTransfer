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
 2) RECEIVE FILES
 3) QUIT
''' % logo

msg = 'Enter your choice from 1-3: '
while 1:
    os.system(clear)
    print(main_menu)
    choice = input(msg).upper()

    if choice == '1':
        print('\n * SENDING FILES *\n')
        import sender

        S = sender.Sender()
        D = S.get_files_to_send()
        S.send_files_metadata(D)
        S.send_files()
        S.close()
        break
    elif choice == '2':
        print('\n * RECEIVING FILES *\n')
        import receiver

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
        msg = 'Enter only numbers from 1-3: '
