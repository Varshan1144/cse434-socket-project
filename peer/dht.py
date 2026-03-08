import socket
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from common.utils import get_next_prime

dht_peers = []
is_leader = False
my_name = None
my_id = None
ring_size = None
right_neighbor = None

manager_ip = None
manager_port = None
main_sock = None

local_dht = {}

def set_my_name(name):
    global my_name
    my_name = name

def set_manager_info(ip, port, sock):
    global manager_ip, manager_port, main_sock
    manager_ip = ip
    manager_port = port
    main_sock = sock

def handle_setup_reply(reply, leader_name, year):
    global dht_peers, is_leader
    print(f"[DHT DEBUG] Handling setup reply for leader {leader_name}, year {year}")
    sys.stdout.flush()
    lines = reply.strip().split("\n")
    if lines[0] != "SUCCESS":
        print("[DHT] Setup failed")
        return

    print("[DHT] Setup successful. Parsing peers...")
    dht_peers = []
    for line in lines[1:]:
        name, ip, port = line.split()
        dht_peers.append((name, ip, int(port)))

    if my_name == leader_name:
        is_leader = True
        print("[DHT] I am the leader. Building ring...")
        build_ring()
        global ring_size, my_id, right_neighbor
        n = len(dht_peers)
        ring_size = n
        my_id = 0
        if n > 1:
            neigh = dht_peers[1]
            right_neighbor = (neigh[1], neigh[2])
        else:
            right_neighbor = None 
        
        distribute_data(year)

def build_ring():
    global dht_peers
    print("[DHT] Building logical ring...")
    n = len(dht_peers)
    for i in range(n):
        name, ip, port = dht_peers[i]
        neigh = dht_peers[(i + 1) % n]
        neigh_ip, neigh_port = neigh[1], neigh[2]
        msg = f"set-id {i} {n} {neigh_ip} {neigh_port}"
        print(f"[DHT DEBUG] Sending set-id to {name} at {ip}:{port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg.encode(), (ip, port))
        sock.close()
    sys.stdout.flush()

def handle_set_id(parts):
    global my_id, ring_size, right_neighbor
    _, id_str, size_str, neigh_ip, neigh_port = parts
    my_id = int(id_str)
    ring_size = int(size_str)
    right_neighbor = (neigh_ip, int(neigh_port))
    print(f"[RING] My ID: {my_id}, Right Neighbor: {right_neighbor}")

def load_dataset(year):
    filename = f"details-{year}.csv"
    if not os.path.exists(filename):
        print(f"[ERROR] Dataset {filename} not found.")
        return []
    
    records = []
    with open(filename, 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            if line.strip():
                records.append(line.strip())
    return records

def distribute_data(year):
    print(f"[DHT DEBUG] distribute_data called for year {year}")
    records = load_dataset(year)
    l = len(records)
    print(f"[DHT DEBUG] Loaded {l} records.")
    if l == 0:
        print("[DHT] No data to distribute.")
        send_dht_complete()
        return

    s = get_next_prime(2 * l)
    n = ring_size
    print(f"[DHT] Distributing {l} records. Hash table size s={s}, ring size n={n}")
    sys.stdout.flush()

    for record in records:
        event_id = int(record.split(',')[0])
        pos = event_id % s
        target_id = pos % n
        
        if target_id == my_id:
            local_dht[pos] = record
        else:
            msg = f"store {pos} {record}"
            main_sock.sendto(msg.encode(), right_neighbor)
    
    print(f"[DHT] Data distribution initiated.")
    send_dht_complete()

def handle_peer_message(message, addr, sock):
    parts = message.split(maxsplit=2)
    if not parts: return
    
    cmd = parts[0]
    if cmd == "store":
        pos = int(parts[1])
        record = parts[2]
        target_id = pos % ring_size
        
        if target_id == my_id:
            local_dht[pos] = record
        else:
            sock.sendto(message.encode(), right_neighbor)
    elif cmd == "teardown":
        local_dht.clear()
        if is_leader:
             pass
        else:
            sock.sendto(message.encode(), right_neighbor)

def send_dht_complete():
    print(f"[DHT] Sending dht-complete to manager...")
    msg = f"dht-complete {my_name}"
    main_sock.sendto(msg.encode(), (manager_ip, manager_port))