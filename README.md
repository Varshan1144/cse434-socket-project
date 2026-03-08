# CSE 434 — Distributed Hash Table (DHT) Socket Project

This project implements a Distributed Hash Table (DHT) using a logical ring topology and UDP socket communication. Peers form a distributed system where data is partitioned and stored across multiple machines.

## Group Information

- **Group Number:** 61
- **Assigned Port Range:** 31500 – 31999

## Project Structure
- **manager/**
    - `manager.py`        # Central coordinator (peer registration, DHT setup)
- **peer/**
    - `peer.py`           # Peer process & networking interface
    - `dht.py`            # Ring formation and data distribution logic
- **common/**
    - `utils.py`          # Shared helper functions
- `details-1950.csv`      # Storm dataset (1950, 14-field format)
- `automated_test.py`     # Local milestone verification script

## Port Assignments (Group 61)
| Component | Manager Communication Port | Peer Logical Port (p-port) |
| :--- | :--- | :--- |
| **Manager** | 31500 | N/A |
| **Peer A** | 31501 | 31601 |
| **Peer B** | 31502 | 31602 |
| **Peer C** | 31503 | 31603 |

## Milestone Features Implemented

✔ Peer registration  
✔ DHT setup via manager  
✔ Leader election  
✔ Logical ring formation (set-id)  
✔ Distributed data partitioning  
✔ Completion confirmation (dht-complete)

## 🖥️ Local Execution Instructions

### Option 1 — Automated Verification (Recommended)
Runs the full milestone automatically:
```bash
python3 automated_test.py
```

### Option 2 — Manual Execution
**Terminal 1 — Manager**
```bash
python3 manager/manager.py 31500
```
**Terminal 2 — Peer A (Leader)**
```bash
python3 peer/peer.py 127.0.0.1 31500 127.0.0.1 31501
```
*Commands:*
```text
register peerA 127.0.0.1 31501 31601
setup-dht peerA 3 1950
```
**Terminal 3 — Peer B**
```bash
python3 peer/peer.py 127.0.0.1 31500 127.0.0.1 31502
```
*Commands:*
```text
register peerB 127.0.0.1 31502 31602
```
**Terminal 4 — Peer C**
```bash
python3 peer/peer.py 127.0.0.1 31500 127.0.0.1 31503
```
*Commands:*
```text
register peerC 127.0.0.1 31503 31603
```

## ☁️ CloudLab Deployment (Distributed Demo)

This project supports full distributed execution across multiple machines.

### Node Roles
| Node | Role |
| :--- | :--- |
| **node0** | Manager |
| **node1** | Peer A (Leader) |
| **node2** | Peer B |
| **node3** | Peer C |

*Use each node’s private LAN IP (10.x.x.x).*

**Manager (node0)**
```bash
python3 manager/manager.py 31500
```
**Peer A (node1)**
```bash
python3 peer/peer.py <manager_ip> 31500 <peerA_ip> 31501
register peerA <peerA_ip> 31501 31601
setup-dht peerA 3 1950
```
**Peer B (node2)**
```bash
python3 peer/peer.py <manager_ip> 31500 <peerB_ip> 31502
register peerB <peerB_ip> 31502 31602
```
**Peer C (node3)**
```bash
python3 peer/peer.py <manager_ip> 31500 <peerC_ip> 31503
register peerC <peerC_ip> 31503 31603
```

## 🧠 DHT Operation Overview

1. **Peers register** with manager.
2. **Leader initiates** DHT creation.
3. **Manager selects** participating peers.
4. **Leader assigns IDs** and forms logical ring.
5. **Storm data is distributed** using hashing.
6. **Leader confirms completion** to manager.

## 📊 Hashing Logic

Data is distributed using:
```text
position = event_id % hash_table_size
node_id = position % number_of_peers
```
This ensures balanced distribution across the ring.

## 📁 Data Preparation

Storm datasets from other years can be processed as:
```bash
python3 transform_csv.py <YEAR>
```