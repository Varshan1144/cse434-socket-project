import socket
import sys
import random

peers = {}

dht_exists = False
dht_peers = []
dht_leader = None
dht_status = "IDLE"


def handle_register(parts, addr, sock):
    if len(parts) != 5:
        sock.sendto("FAILURE: Invalid arguments".encode(), addr)
        return

    _, name, ip, m_port, p_port = parts
    
    if not name.isalpha() or len(name) > 15:
        sock.sendto("FAILURE: peer-name must be alphabetic and max 15 chars".encode(), addr)
        return

    m_port = int(m_port)
    p_port = int(p_port)

    if name in peers:
        sock.sendto("FAILURE: Peer name already exists".encode(), addr)
        return

    for peer in peers.values():
        if peer["ip"] == ip and (peer["m_port"] == m_port or peer["p_port"] == p_port):
            sock.sendto("FAILURE: Port already in use on this IP".encode(), addr)
            return

    peers[name] = {
        "ip": ip,
        "m_port": m_port,
        "p_port": p_port,
        "state": "Free"
    }

    print(f"[MANAGER] Registered peer: {name}")
    print(f"[MANAGER] Sending SUCCESS to {name} at {addr}")
    sock.sendto("SUCCESS: Registered".encode(), addr)


def handle_setup_dht(parts, addr, sock):
    global dht_exists, dht_peers, dht_leader

    if len(parts) != 4:
        sock.sendto("FAILURE: Invalid arguments".encode(), addr)
        return

    _, leader_name, n_str, year = parts
    n = int(n_str)

    if leader_name not in peers:
        sock.sendto("FAILURE: Leader not registered".encode(), addr)
        return

    if n < 3:
        sock.sendto("FAILURE: n must be at least 3".encode(), addr)
        return

    if len(peers) < n:
        sock.sendto("FAILURE: Not enough peers registered".encode(), addr)
        return

    if dht_exists:
        sock.sendto("FAILURE: DHT already exists".encode(), addr)
        return

    free_peers = list(peers.keys())
    free_peers.remove(leader_name)
    selected = random.sample(free_peers, n - 1)

    dht_peers = [leader_name] + selected
    dht_leader = leader_name
    dht_exists = True
    dht_status = "SETTING_UP"

    peers[leader_name]["state"] = "Leader"
    for p in selected:
        peers[p]["state"] = "InDHT"

    print(f"[MANAGER] DHT setup initiated by leader {leader_name}")
    print(f"[MANAGER] DHT Peers: {dht_peers}")

    response = "SUCCESS\n"
    for name in dht_peers:
        info = peers[name]
        response += f"{name} {info['ip']} {info['p_port']}\n"

    sock.sendto(response.encode(), addr)


def handle_dht_complete(parts, addr, sock):
    global dht_status
    if len(parts) != 2:
        sock.sendto("FAILURE: Invalid arguments".encode(), addr)
        return

    name = parts[1]
    if name != dht_leader:
        sock.sendto("FAILURE: Only leader can call dht-complete".encode(), addr)
        return

    dht_status = "READY"
    print(f"[MANAGER] DHT setup complete. Ready for queries.")
    print(f"[MANAGER] Sending SUCCESS to leader {name} at {addr}")
    sock.sendto("SUCCESS: DHT is ready".encode(), addr)


def start_manager(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    print(f"[MANAGER] Listening on port {port}...")

    while True:
        data, addr = sock.recvfrom(4096)
        message = data.decode().strip()
        print(f"[MANAGER] Received from {addr}: {message}")

        parts = message.split()
        if not parts:
            sock.sendto("FAILURE: Empty command".encode(), addr)
            continue

        command = parts[0]

        if dht_status == "SETTING_UP":
            if command == "dht-complete":
                handle_dht_complete(parts, addr, sock)
            else:
                sock.sendto("FAILURE: Manager waiting for dht-complete".encode(), addr)
            continue

        if command == "register":
            handle_register(parts, addr, sock)
        elif command == "setup-dht":
            handle_setup_dht(parts, addr, sock)
        elif command == "dht-complete":
            handle_dht_complete(parts, addr, sock)
        else:
            sock.sendto("FAILURE: Unknown command".encode(), addr)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python manager.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_manager(port)