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
def send_message(IP_router_final, puerto_router_final,message,IP_envío, puerto_envío):
    packet_msg = create_packet({
        "IP": IP_router_final,
        "PORT": int(puerto_router_final),
        "DATA": message
    })
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto(packet_msg,(IP_envío,int(puerto_envío)))
    s.close()
def check_routes(routes_file_name: str, destination_address: tuple[str, int])-> tuple[str, int]:
    ip,port = destination_address

    with open(routes_file_name,"r") as f:
        file = f.read()
    lines = file.split("\n")
    for line in lines:
        red, port_i,port_f, next_ip,next_port = line.split(" ")
        #Se asume que todas las masks son de 24 ya que estamos trabajando en la ip local 127.0.0.xxx
        if red[0:8]== ip[0:8] and port>=int(port_i) and port<=int(port_f):
            return (next_ip,int(next_port))
    return None

