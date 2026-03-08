# CSE 434 - Distributed Hash Table (DHT) Socket Project

This project implements a Distributed Hash Table (DHT) in a ring topology with "Hot Potato" query processing.

## Group Information
- **Group Number:** 61
- **Assigned Port Range:** 31500 - 31999

## Project Structure
- `manager/manager.py`: The central manager that handles peer registration and DHT initialization.
- `peer/peer.py`: The peer client that manages its portion of the DHT and processes messages.
- `peer/dht.py`: Core DHT logic, including ring management and data distribution.
- `common/utils.py`: Shared utility functions.
- `details-1950.csv`: transformed storm events data from 1950 (14-field format).
- `automated_test.py`: A local verification script configured for Group 61 ports.

## Port Assignments (Group 61)
| Component | Interaction Port | Logical Port (p-port) |
| :--- | :--- | :--- |
| Manager | 31500 | N/A |
| Peer 1 | 31501 | 31601 |
| Peer 2 | 31502 | 31602 |
| Peer 3 | 31503 | 31603 |

## Local Execution Instructions

### 1. Run Automated Test
The easiest way to verify the milestone locally:
```bash
python3 automated_test.py
```

### 2. Manual Execution (Milestone Steps)

**Terminal 1 (Manager):**
```bash
python3 manager/manager.py 31500
```

**Terminal 2 (Peer 1):**
```bash
python3 peer/peer.py 127.0.0.1 31500 127.0.0.1 31501
# Commands:
register peer1 127.0.0.1 31501 31601
setup-dht peer1 3 1950
```

**Terminal 3 (Peer 2):**
```bash
python3 peer/peer.py 127.0.0.1 31500 127.0.0.1 31502
# Commands:
register peer2 127.0.0.1 31502 31602
```

**Terminal 4 (Peer 3):**
```bash
python3 peer/peer.py 127.0.0.1 31500 127.0.0.1 31503
# Commands:
register peer3 127.0.0.1 31503 31603
```

## Data Preparation
For the final project or other years, download the `.csv.gz` files from the [NCEI Storm Events Database](https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/), unzip them, and use `transform_csv.py` to convert them to the required 14-field format:
```bash
python3 transform_csv.py <YEAR>
```