from core.utils import *
from core.features.filetransfer import get_dir_from_remote

def execute_apps(server):
    display_msg("Executing apps")
    app_to_run = get_dir_from_remote(server)
    server.send_data(app_to_run + " all")

    command_rst = server.receive_data()
    print(command_rst)
