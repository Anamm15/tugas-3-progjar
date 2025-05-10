import socket
import json
import base64
import logging
import sys

server_address = ('0.0.0.0', 7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")

        encoded_command = command_str.encode()
        length_str = str(len(encoded_command)).zfill(10).encode() 
        sock.sendall(length_str + encoded_command)

        length_data = b''
        while len(length_data) < 10:
            more = sock.recv(10 - len(length_data))
            if not more:
                raise Exception("Connection closed while reading length header")
            length_data += more
        total_length = int(length_data.decode())

        data_received = b''
        while len(data_received) < total_length:
            chunk = sock.recv(min(4096, total_length - len(data_received)))
            if not chunk:
                break
            data_received += chunk

        hasil = json.loads(data_received.decode())
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {e}")
        return False

def remote_list():
    command_str = "LIST"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb') as fp:
            fp.write(isifile)
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename=""):
    try:
        with open(filename, 'rb') as fp:
            isifile = base64.b64encode(fp.read()).decode()
        command_str = f"UPLOAD {filename} {isifile}"
        hasil = send_command(command_str)
        if hasil and hasil['status'] == 'OK':
            print(hasil['data'])
            return True
        else:
            print("Gagal")
            return False
    except Exception as e:
        print(f"Upload error: {e}")
        return False

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        print(hasil['data'])
        return True
    else:
        print("Gagal")
        return False

if __name__ == '__main__':
    server_address = ('172.16.16.101', 6667)
    # remote_list()
    # remote_get('donalbebek.jpg')
    # remote_upload('donalbebek.jpg')
