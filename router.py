import socket
import sys

BUFFER_SIZE= 1024

rutas ={}

def parse_packet(IP_packet: bytes):
    a = IP_packet[0]
    b = IP_packet[1]
    c = IP_packet[2] 
    d = IP_packet[3]
    ip = f"{a}.{b}.{c}.{d}"
    port = int.from_bytes(IP_packet[4:6], byteorder="big")
    ttl = IP_packet[6]
    data = IP_packet[7:].decode()
    dict = {}
    dict = {
        "IP": ip,
        "PORT": port,
        "TTL": ttl,
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
    ttl = parsed_IP_packet["TTL"].to_bytes(1,byteorder="big")
    data = parsed_IP_packet["DATA"].encode()
    return ip+port+ttl+data

def send_message(IP_router_final, puerto_router_final,ttl,message,IP_envío, puerto_envío):
    packet_msg = create_packet({
        "IP": IP_router_final,
        "PORT": puerto_router_final,
        "TTL": ttl,
        "DATA": message
    })
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto(packet_msg,(IP_envío,puerto_envío))
    s.close()
def check_routes(routes_file_name: str, destination_address: tuple[str, int])-> tuple[str, int]:
    ip,port = destination_address

    with open(routes_file_name,"r") as f:
        file = f.read()
    lines = file.split("\n")
    candidates = []
    for line in lines:
        red, port_i,port_f, next_ip,next_port = line.split(" ")
        #Se asume que todas las masks son de 24 ya que estamos trabajando en la ip local 127.0.0.xxx
        if red[0:8]== ip[0:8] and port>=int(port_i) and port<=int(port_f):
            candidates.append((red, int(port_i), int(port_f), next_ip, int(next_port)))
    if not candidates:        
        return None
    next_ip,next_port = round_robin(candidates)
    return (next_ip, next_port)

def round_robin(candidates):
    temp = tuple(candidates)
    key = rutas.get(temp)
    if key is None:
        rutas[temp] = 0
        key = 0
    rout = temp[key]
    _,_,_,next_ip,next_port = rout
    actual = rutas[temp]
    rutas[temp] =(actual+1)%len(temp)
    return next_ip,next_port

def is_for_me(paq,ip,port):
    paq_ip = paq["IP"]
    paq_port = paq["PORT"]
    return paq_ip == ip and paq_port == port
        

def main():
    if len(sys.argv)<4:
        print("error: No hay suficientes argumentos")
        sys.exit(1)
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    route = sys.argv[3]
    address = (IP,PORT)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(address)
    while True:
        data, _ = sock.recvfrom(BUFFER_SIZE)
        pars_data = parse_packet(data)
        if pars_data["TTL"]>0:
            a = is_for_me(pars_data,IP,PORT)
            if a:
                print(pars_data["DATA"])
            else:
                next_hop = check_routes(route,(pars_data["IP"],pars_data["PORT"]))
                if next_hop:
                    print(f"redirigiendo paquete {pars_data} con destino final {pars_data['IP']}:{pars_data['PORT']} desde {IP}:{PORT} hacia {next_hop[0]}:{next_hop[1]}")
                    send_message(pars_data["IP"],pars_data["PORT"],pars_data["TTL"]-1,pars_data["DATA"],next_hop[0],next_hop[1])
                else:
                    print(f"No hay rutas hacia {pars_data['IP']}:{pars_data['PORT']} para paquete {pars_data}")
        else:
            print(f"Se recibio paquete {pars_data} con TTL 0")

if __name__=="__main__":
    main()
