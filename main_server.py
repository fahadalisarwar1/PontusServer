from core.connection.conn import Server
from core.connection.handler import connection_handler



if __name__ == "__main__":
    server = Server()
    server.wait_to_connect()
    connection_handler(server)
    server.close()
