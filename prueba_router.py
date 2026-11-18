import socket
import sys


def create_packet(parsed_IP_packet):
    temp = parsed_IP_packet["IP"].split(".")
    a = int(temp[0])
    b = int(temp[1])
    c = int(temp[2])
    d = int(temp[3])
    ip = bytes([a,b,c,d])
    temp2 = parsed_IP_packet["PORT"]
    port = temp2.to_bytes(2,byteorder="big")
    ttl = parsed_IP_packet["TTL"].to_bytes(1,byteorder="big")
    data = parsed_IP_packet["DATA"].encode()
    return ip+port+ttl+data



def main():
    if len(sys.argv) < 4:
        print("error: No hay suficientes argumentos")
        sys.exit(1)

    dest_ip, dest_port, ttl = sys.argv[1].split(";")
    dest_port = int(dest_port)
    ttl = int(ttl)

    router_addr = (sys.argv[2], int(sys.argv[3]))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for line in sys.stdin:
        line = line.rstrip("\n")
        pack_dict= {
            "IP": dest_ip,
            "PORT": dest_port,
            "TTL": ttl,
            "DATA": line,
        }
        packet = create_packet(pack_dict)
        sock.sendto(packet, router_addr)


if __name__ == "__main__":
    main()
