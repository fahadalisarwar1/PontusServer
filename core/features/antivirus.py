from core.utils import display_msg
def show_exception_options():
    display_msg("1 Add current dir")
    display_msg("2 Add Temp dir")

def add_exception(server):
    show_exception_options()
    display_msg("")
    exception_options = input("Select options: ")
    server.send_data(exception_options)
    output = server.receive_data()
    display_msg(output)