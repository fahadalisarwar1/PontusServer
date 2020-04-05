from core.utils import display_msg
from glob import glob
import os
import time
import json
import tqdm

BUFFER_SIZE =  2 * 4096
SEPARATOR = "<SEPARATOR>"


class FileTransfer:
    def __init__(self, server):
        self.server = server

    def upload_file(self, filename):
        if filename == "quit":
            self.server.send_data("quit")
            return
        display_msg("Upload Files to client")
        file_data = b''
        with open(filename, "rb") as file:
            file_data = file.read()
        only_filename = os.path.basename(filename)
        self.server.send_data(only_filename)
        data_with_delimeter = file_data + self.server.DELIMETER.encode()
        self.server.conn.send(data_with_delimeter)
        display_msg("File "+ only_filename + " Uploaded successfully")
        time.sleep(4)


    def download_files(self, filename):
        display_msg("Downloading Files")
        if filename == "quit":
            self.server.send_data("quit")
            return
        self.server.send_data(filename)

        zipped_name = self.server.receive_data()
        file_data = b''
        while True:
            chunk = self.server.conn.recv(self.server.CHUNK_SIZE)

            if chunk.endswith(self.server.DELIMETER.encode()):
                chunk  = chunk[:-len(self.server.DELIMETER)]
                file_data += chunk
                break
            file_data += chunk

        with open(zipped_name, "wb") as file:
            file.write(file_data)
        display_msg("File/Folder " + filename + " downloaded successfully")
        time.sleep(2)

    def download_fancy(self, filename):
        display_msg("Downloading Files")
        if filename == "quit":
            self.server.send_data("quit")
            return
        self.server.send_data(filename)
        received = self.server.conn.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)
        count = 0
        with open(filename, "wb") as file:
            
            while True:
                data_buffer = self.server.conn.recv(BUFFER_SIZE)
                count += 1
                data_received = count * BUFFER_SIZE
                prog = (data_received / filesize) * 100
                print(" \t\tProgress: "+str(int(prog)) +"\t"+str(data_received)+ "\r", end="")             
                if "DONE_SENDING".encode() in data_buffer:
                    break
                file.write(data_buffer)
        display_msg("File Downloaded successfully")
        time.sleep(10)


def upload(server):
    
    files_list = glob("UploadFolder/*")
    files_list = list(filter(os.path.isfile, files_list))
    if not files_list:
        display_msg("No files present in Upload folder", "r")
        check_existence = True
        while check_existence: 
            filename = input("[+] Write filename to send : ")
            if os.path.exists(filename):
                break
            if filename == "quit":
                break
            else:
                display_msg("[+] File doesn't exist, try again", "r")
    else:
        for i, file in enumerate(files_list):
            print(i, "\t", os.path.basename(file))
        while True:
            try:    
                file_index = int(input("[+] Select the file index you want to upload  "))
                filename = files_list[file_index]
                break

            except Exception:
                display_msg("Invalid index selected", "r")
                filename = "quit"
                break

    ft = FileTransfer(server)
    ft.upload_file(filename)

def download(server):

    full_list_of_files = b''
    while True:
        chunk = server.conn.recv(server.CHUNK_SIZE)
        if chunk.endswith(server.DELIMETER.encode()):
            chunk = chunk[:-len(server.DELIMETER)]
            full_list_of_files += chunk
            break
        full_list_of_files += chunk

    files = json.loads(full_list_of_files)
    # print(files)
    for index in files:
        print("\t\t", index, "\t", files[index])

    try:
        file_index = input("[+] Enter the file / folder you want to download ")
        file_2_download = files[file_index]
        # print(file_2_download)
    except Exception as err:
        file_2_download = "quit"
        print(err)
        display_msg(str(err), "r")
        time.sleep(10)
    
    ft = FileTransfer(server)
    # ft.download_files(file_2_download)
    ft.download_fancy(file_2_download)

