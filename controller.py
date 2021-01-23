import pexpect
import time
import sys
import threading
from random import randint

from message import GoveeBLMessageType, build_message, get_handle

class GoveeBLController(object):
    #constructor
    def __init__(self, addr):
        self.addr = addr
        self.gatt = pexpect.spawn(f"gatttool -b {addr} -I")
        self.should_keep_alive = False

    def send_keep_alive(self):
        while(self.should_keep_alive):
            msg = build_message(GoveeBLMessageType.KEEPALIVE, None)
            self.gatt.sendline(f"char-write-req {get_handle()} {msg}")
            try:
                self.gatt.expect("Characteristic value was written successfully", timeout=1)
            except pexpect.exceptions.TIMEOUT:
                print("Lost connection to device. Trying to reconnect")
                self.disconnect()
                self.connect(True) # TODO: This is a bad implementation and needs to be fixed asap
            time.sleep(2)

    def connect(self, keep_alive):
        self.gatt.sendline("connect")
        try:
            self.gatt.expect("Connection successful", timeout=5)
            print(f"Successfuly connected to {self.addr}")
            self.should_keep_alive = keep_alive
            if keep_alive:
                print("Will try to keep the connection alive")
                self.keep_alive_thread = threading.Thread(target=self.send_keep_alive, name="alive_keeper")
                self.keep_alive_thread.start()
            return True
        except pexpect.exceptions.TIMEOUT:
            print(f"Failed to connect to {self.addr}")
            return False
    
    def disconnect(self):
        self.should_keep_alive = False
        self.gatt.sendline("disconnect")
        return True

    def change_color(self, color):
        if not self.should_keep_alive:
            self.connect(False)
        
        msg = build_message(GoveeBLMessageType.SETCOLOR, color)
        self.gatt.sendline(f"char-write-req {get_handle()} {msg}")

    def change_brightness(self, brightness):
        if not self.should_keep_alive:
            self.connect(False)
        
        msg = build_message(GoveeBLMessageType.SETBRIGHTNESS, brightness)
        self.gatt.sendline(f"char-write-req {get_handle()} {msg}")
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    controller = GoveeBLController(sys.argv[1])
    controller.connect(True)
