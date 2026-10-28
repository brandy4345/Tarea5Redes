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
