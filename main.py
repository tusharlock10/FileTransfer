import os,sys, tj
os.chdir(os.path.dirname(sys.argv[0]))

logo=r'''
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

main_menu=f'''
{logo}


 * MAIN MENU *

 1) SEND FILES
 2) RECEIVE FILES
 3) QUIT
'''

msg='Enter your choice from 1-3: '
while 1:
    choice=input(msg).upper()

    if choice =='1':
        import sender
        break
    elif choice == '2':
        import receiver
        break
    elif choice in ['3','Q','QUIT','E']:
        bye=tj.color_text('\n * GOOD BYE *', text_color='PURPLE', background_color='WHITE')
        input(bye+', Enter to quit...')
        break
    else:
        msg='Enter only numbers from 1-3: '