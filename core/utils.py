from colorama import Fore, Style
import os
from colorama import init



init()

def display_msg(msg, color="g"):
    if color == "g":
        print(Fore.GREEN + "\t\t[+] " + str(msg)+Style.RESET_ALL)
    else:
        print(Fore.RED + "\t\t[+] " + str(msg)+Style.RESET_ALL)
    

def banner():
    
    print(Fore.BLUE + "\t\t ---------------------------------------------------")
    print("\t\t +                 PONTUS SERVER                   +")
    
    print("\t\t ---------------------------------------------------")
    
    print("\n"+Style.RESET_ALL)




def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner()


