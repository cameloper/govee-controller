from enum import Enum

class GoveeBLMessageType(Enum):
    KEEPALIVE = 1
    SETCOLOR = 2
    SETBRIGHTNESS = 3

def int_to_hex(intv):
    h = hex(intv).replace("0x", "")
    while len(h) < 2:
        h = "0" + h
    return h

def get_handle():
    handle = 21
    return "0x{:04x}".format(handle)


def build_message(type, val):
    bins = []

    if type is GoveeBLMessageType.KEEPALIVE:
        bins = [170, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 171]
    elif type is GoveeBLMessageType.SETCOLOR:
        r, g, b = val
        sig = (3*16 + 1) ^ r ^ g ^ b
        bins = [51, 5, 2, r, g, b, 0, 255, 174, 84, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    elif type is GoveeBLMessageType.SETBRIGHTNESS:
        bright = int(val / 100 * 255)
        sig = (3*16 + 3) ^ (4) ^ bright
        bins = [51, 4, bright, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, sig]
    
    return "".join(map(int_to_hex, bins))