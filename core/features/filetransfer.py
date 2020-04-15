from core.utils import display_msg
from glob import glob
import os
import time
import json
import tqdm

BUFFER_SIZE =  1 * 4096
SEPARATOR = "<SEPARATOR>"


class FileTransfer:
    def __init__(self, server):
        self.server = server
    
    def upload_with_tqdm(self, filename):
        if filename == "quit":
            self.server.send_data(filename)
            return
        else:
            self.server.send_data("pass")

        filesize = os.path.getsize(filename)

        self.server.conn.send(f"{filename}{SEPARATOR}{filesize}".encode())
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            for _ in progress:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                self.server.conn.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
            self.server.conn.send(SEPARATOR.encode())
        display_msg("Successfully uploaded")

    
    def download_with_tqdm(self, filename):
        display_msg("Downloading Files")
        if filename == "quit":
            self.server.send_data("quit")
            return
        self.server.send_data(filename)
        # print(filename)
        received = self.server.conn.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)
        download_folder = "Downloads_folder"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
                
        file_name_to_save = download_folder + "/"+filename
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(file_name_to_save, "wb") as f:
            for _ in progress:
                # read 1024 bytes from the socket (receive)
                bytes_read = self.server.conn.recv(BUFFER_SIZE)
                if SEPARATOR.encode() in bytes_read:
                    bytes_read = bytes_read[:-len(SEPARATOR)]    
                    f.write(bytes_read)
                    # nothing is received
                    # file transmitting is done
                    break
                
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))




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
    ft.upload_with_tqdm(filename)

def get_dir_from_remote(server):
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
        file_index = input("[+] select the file ")
        file_2_download = files[file_index]
        # print(file_2_download)
    except Exception as err:
        file_2_download = "quit"
        print(err)
        display_msg(str(err), "r")
        time.sleep(3)
    return file_2_download

def download(server):

    file_2_download = get_dir_from_remote(server)

    ft = FileTransfer(server)
    # ft.download_files(file_2_download)

    # ft.download_fancy(file_2_download)
    ft.download_with_tqdm(file_2_download)

