def hashing(n):
    num = n * 387420489 % 4000000000
    return hex(num)[2:]


def unhashing(h):
    return int(h, 16) * 3513180409 % 4000000000
