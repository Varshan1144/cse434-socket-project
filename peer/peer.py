import socket
import sys
from dht import handle_setup_reply, set_my_name


def start_peer(manager_ip, manager_port, peer_ip, m_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((peer_ip, m_port))
    print(f"[PEER] Bound to {peer_ip}:{m_port}")

    while True:
        print("\nEnter command:")
        print("register <peer_name> <peer_ip> <m_port> <p_port>")
        print("setup-dht <leader_name> <n> <year>")
        cmd = input("> ").strip()

        if not cmd:
            continue

        parts = cmd.split()

        if parts[0] == "register":
            set_my_name(parts[1])

        sock.sendto(cmd.encode(), (manager_ip, manager_port))

        data, _ = sock.recvfrom(4096)
        reply = data.decode()

        if parts[0] == "setup-dht":
            handle_setup_reply(reply, parts[1])
        else:
            print(f"[MANAGER REPLY] {reply}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python peer.py <manager_ip> <manager_port> <peer_ip> <m_port>")
        sys.exit(1)

    manager_ip = sys.argv[1]
    manager_port = int(sys.argv[2])
    peer_ip = sys.argv[3]
    m_port = int(sys.argv[4])

    start_peer(manager_ip, manager_port, peer_ip, m_port)