from core.utils import display_msg, clear_screen
import time
class ReverseShell:

    def help(self):
        clear_screen()
        display_msg("cd\t\t\tChange directory")
        display_msg("clear\t\tclear screen")
        display_msg("stop\t\tStop")
        print()

    def run_commands(self, server):
        self.help()
        run_shell = True
        pwd = server.receive_data()

        while run_shell:
            command = input(pwd+" >> ")
            server.send_data(command)
            if command == "exit" or command == "stop" or command == "quit" or command == "q":
                clear_screen()
                run_shell = False
                
                break        
            elif command == "clear" or command == "cls":
                self.help()
            elif command.startswith("cd"):
                display_msg("changing path")
            elif command == "":
                display_msg("No command entered", "r")
            else:
                cmd_result = server.receive_data()
                print(cmd_result)
            time.sleep(0.1)    
            pwd = server.receive_data()



def run_reverse_shell(server):
    rs = ReverseShell()
    rs.run_commands(server)


