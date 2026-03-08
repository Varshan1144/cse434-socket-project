import math

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def get_next_prime(n):
    if n <= 1:
        return 2
    prime = n
    # Start looking from n or n+1
    if prime % 2 == 0:
        prime += 1
    else:
        prime += 2
    
    while True:
        if is_prime(prime):
            return prime
        prime += 2
