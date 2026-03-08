import socket
import time
import subprocess
import os
import threading

def read_output(name, proc):
    for line in iter(proc.stdout.readline, ''):
        print(f"[{name}] {line.strip()}")
    for line in iter(proc.stderr.readline, ''):
        print(f"[{name} ERR] {line.strip()}")

def test_milestone():
    # 1. Start Manager
    manager_proc = subprocess.Popen(["python3", "manager/manager.py", "31500"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    threading.Thread(target=read_output, args=("MANAGER", manager_proc), daemon=True).start()
    time.sleep(1)

    # 2. Start 3 Peers
    p1 = subprocess.Popen(["python3", "peer/peer.py", "127.0.0.1", "31500", "127.0.0.1", "31501"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p2 = subprocess.Popen(["python3", "peer/peer.py", "127.0.0.1", "31500", "127.0.0.1", "31502"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    p3 = subprocess.Popen(["python3", "peer/peer.py", "127.0.0.1", "31500", "127.0.0.1", "31503"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    threading.Thread(target=read_output, args=("P1", p1), daemon=True).start()
    threading.Thread(target=read_output, args=("P2", p2), daemon=True).start()
    threading.Thread(target=read_output, args=("P3", p3), daemon=True).start()
    
    time.sleep(1)

    try:
        # Register them
        print("Registering peers...")
        p1.stdin.write("register peerA 127.0.0.1 31501 31601\n")
        p1.stdin.flush()
        time.sleep(1)
        
        p2.stdin.write("register peerB 127.0.0.1 31502 31602\n")
        p2.stdin.flush()
        time.sleep(1)
        
        p3.stdin.write("register peerC 127.0.0.1 31503 31603\n")
        p3.stdin.flush()
        time.sleep(1)

        # Setup DHT
        print("Setting up DHT...")
        p1.stdin.write("setup-dht peerA 3 1950\n")
        p1.stdin.flush()
        
        # Give it some time to distribute data and signal completion
        time.sleep(5)

        print("Test sequence finished.")
        
    finally:
        manager_proc.terminate()
        p1.terminate()
        p2.terminate()
        p3.terminate()
        time.sleep(1)

if __name__ == "__main__":
    test_milestone()
