dht_peers = []
is_leader = False
my_name = None


def set_my_name(name):
    global my_name
    my_name = name


def handle_setup_reply(reply, leader_name):
    global dht_peers, is_leader

    lines = reply.strip().split("\n")

    if lines[0] != "SUCCESS":
        print("[DHT] Setup failed")
        return

    print("[DHT] Setup successful")
    dht_peers = []

    for line in lines[1:]:
        name, ip, port = line.split()
        dht_peers.append((name, ip, int(port)))

    if my_name == leader_name:
        is_leader = True
        print("[DHT] I am the leader")

    print("[DHT] DHT Peers:")
    for p in dht_peers:
        print("   ", p)