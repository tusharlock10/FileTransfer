import os
import sys
import tj

dirname=os.path.dirname(sys.argv[0])
if dirname!="":os.chdir(dirname)

clear="cls"
if 'win32' not in sys.platform.lower():clear='clear'

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
        break
    elif choice == '2':
        break
    elif choice in ['3', 'Q', 'QUIT', 'E']:
        print()
        bye = tj.color_text('  * GOOD BYE *  ', text_color='PURPLE', background_color='WHITE')
        print()
        input(bye + ', Enter to quit...')
        break
    else:
        msg = 'Enter only numbers from 1-3: '
