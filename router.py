import socket
import sys

IP = "localhost"
PORT = 8000
BUFFER_SIZE= 1024

def parse_packet(IP_packet: bytes):
    a = IP_packet[0]
    b = IP_packet[1]
    c = IP_packet[2] 
    d = IP_packet[3]
    ip = f"{a}.{b}.{c}.{d}"
    port = int.from_bytes(IP_packet[4:6], byteorder="big")
    data = IP_packet[6:].decode()
    dict = {}
    dict = {
        "IP": ip,
        "PORT": port,
        "DATA": data

    }
    return dict
def create_packet(parsed_IP_packet):
    temp = parsed_IP_packet["IP"].split(".")
    a = int(temp[0])
    b = int(temp[1])
    c = int(temp[2])
    d = int(temp[3])
    ip = bytes([a,b,c,d])
    temp2 = parsed_IP_packet["PORT"]
    port = temp2.to_bytes(2,byteorder="big")
    data = parsed_IP_packet["DATA"].encode()
    return ip+port+data
