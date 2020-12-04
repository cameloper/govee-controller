import pexpect
import time
import sys
import threading
from random import randint

from govee_bl_message import GoveeBLMessageType, build_message, get_handle

class GoveeBLHandler(object):
    #constructor
    def __init__(self, addr):
        self.addr = addr
        self.gatt = pexpect.spawn(f"gatttool -b {addr} -I")

    def send_keep_alive(self):
        while(True):
            msg = build_message(GoveeBLMessageType.KEEPALIVE, None)
            self.gatt.sendline(f"char-write-req {get_handle()} {msg}")
            try:
                self.gatt.expect("Characteristic value was written successfully", timeout=1)
            except pexpect.exceptions.TIMEOUT:
                print("Lost connection to device.")
                sys.exit()
            time.sleep(2)

    def connect(self, keep_alive):
        self.gatt.sendline("connect")
        try:
            self.gatt.expect("Connection successful", timeout=5)
            print(f"Successfuly connected to {self.addr}")
            if keep_alive:
                print("Will try to keep the connection alive")
                self.keep_alive_thread = threading.Thread(target=self.send_keep_alive, name="alive_keeper")
                self.keep_alive_thread.start()
        except pexpect.exceptions.TIMEOUT:
            print(f"Failed to connect to {self.addr}")
            sys.exit()

    def change_color(self, color):
        if self.keep_alive_thread.is_alive() == False:
            self.connect(False)
        
        msg = build_message(GoveeBLMessageType.SETCOLOR, color)
        self.gatt.sendline(f"char-write-req {get_handle()} {msg}")

    def change_brightness(self, brightness):
        if self.keep_alive_thread.is_alive() == False:
            self.connect(False)
        
        msg = build_message(GoveeBLMessageType.SETBRIGHTNESS, brightness)
        self.gatt.sendline(f"char-write-req {get_handle()} {msg}")
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    handler = GoveeBLHandler(sys.argv[1])
    handler.connect(True)