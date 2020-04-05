import socket
from core.utils import clear_screen
from core.utils import display_msg
import os


clear_screen()


class Server:
    """
    usage:
        # create a server object
        server = Server() #  by default system's local Ip address will be used, default port = 8080

        server.wait_to_connect()  # tries to listen for incoming connections

    """
    def __init__(self, ip="", port=8080):
        """[summary]
        
        Keyword Arguments:
            ip {str} -- IP address to be used for server (default: {""})
            port {int} -- Server listening port (default: {8080})
        """     

        self.DELIMETER = "<END_OF_BYTES>"
        self.CHUNK_SIZE = 64 * 1024
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.addr = (ip, port)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(self.addr)
        except Exception as err:
            self.sock.close()
            display_msg(err, "r")

    def wait_to_connect(self):
        display_msg("Waiting for incoming connection on port "+ str(self.addr[1]))
        
        try:
            self.sock.listen()
            self.conn, self.client_addr = self.sock.accept()
            display_msg("Connection established with "+self.client_addr[0])
        except KeyboardInterrupt as err:
            display_msg("Exiting ...", "r")
            exit(0)
            
        except Exception as err:
            display_msg(err, "r")
            


    def send_data(self, data=""):
        data_to_send = data + self.DELIMETER
        data_bin = data_to_send.encode()
        self.conn.send(data_bin)


    def receive_data(self):
        data = b''
        while True:
            chunk = self.conn.recv(self.CHUNK_SIZE)

            if self.DELIMETER.encode() in chunk:
                # print("")
                
                chunk = chunk[:-len(self.DELIMETER)]
                # print(chunk.decode())
                # print()
                data += chunk
                break
            data += chunk
        # display_msg("Received Results completely")
        return data.decode()

    def send(self, msg=""):
        """send a simple 1024 bytes message
        
        Keyword Arguments:
            msg {str} -- Message you want to send (default: {""})
        """        
        msg_bin = msg.encode()
        self.conn.send(msg_bin)
    
    def recv(self):
        """Receive simple message in 1024 bytes
        
        Returns:
            msg -->> [type str] Message you want to receive 
        """        
        msg_bin = self.conn.recv(self.CHUNK_SIZE)
        msg = msg_bin.decode()
        return msg


    def close(self):
        try:
            self.conn.close()
            self.sock.close()
        except AttributeError:
            pass



