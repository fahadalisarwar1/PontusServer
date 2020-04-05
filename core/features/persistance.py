from core.utils import display_msg
import time

def become_persistant(server):
    status = server.receive_data()
    display_msg(status)
    time.sleep(5)

    