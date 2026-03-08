import socket
import sys
import os
import threading
sys.path.append(os.path.dirname(__file__))
from dht import handle_setup_reply, set_my_name, handle_set_id, handle_peer_message, set_manager_info


current_year = None

def listen_loop(sock):
    global current_year
    while True:
        try:
            data, addr = sock.recvfrom(4096)
            message = data.decode()
            parts = message.split()
            
            if not parts:
                continue

            if message.startswith("set-id"):
                handle_set_id(parts)
            elif message.startswith("SUCCESS") and len(message.splitlines()) > 1:
                handle_setup_reply(message, my_name_for_setup_ref, current_year)
            elif message.startswith("SUCCESS") or message.startswith("FAILURE"):
                print(f"\n[MANAGER] {message}\n> ", end="")
                sys.stdout.flush()
            else:
                handle_peer_message(message, addr, sock)
        except Exception as e:
            break

my_name_for_setup_ref = None

def start_peer(manager_ip, manager_port, peer_ip, m_port):
    global current_year, my_name_for_setup_ref
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((peer_ip, m_port))
    print(f"[PEER] Bound to {peer_ip}:{m_port}")
    
    set_manager_info(manager_ip, manager_port, sock)

    listener = threading.Thread(target=listen_loop, args=(sock,), daemon=True)
    listener.start()

    while True:
        cmd = input("> ").strip()

        if not cmd:
            continue

        parts = cmd.split()
        if not parts:
            continue

        if parts[0] == "register":
            set_my_name(parts[1])
            my_name_for_setup_ref = parts[1]
        elif parts[0] == "setup-dht":
            my_name_for_setup_ref = parts[1]
            current_year = parts[3]

        sock.sendto(cmd.encode(), (manager_ip, manager_port))


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python peer.py <manager_ip> <manager_port> <peer_ip> <m_port>")
        sys.exit(1)

    manager_ip = sys.argv[1]
    manager_port = int(sys.argv[2])
    peer_ip = sys.argv[3]
    m_port = int(sys.argv[4])

    start_peer(manager_ip, manager_port, peer_ip, m_port)