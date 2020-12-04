from controller import GoveeBLController
from flask import Flask, request
import sys

app = Flask(__name__)
addr = ""

@app.route("/connect", methods = ["POST"])
def connect():
    args = request.args.to_dict()
    if controller.connect(bool(args["keepAlive"])):
        return f"Connected to {addr}"
    else:
        return "Could not connect/ already connected"

@app.route("/disconnect", methods = ["POST"])
def disconnect():
    if controller.disconnect():
        return f"Disconnected from {addr}"
    else:
        return "Could not disconnect/ already disconnected"

@app.route("/set", methods = ["POST"])
def set_char():
    args = request.args.to_dict()
    if args["char"] == "brightness":
        controller.change_brightness(int(args["value"]))
    elif args["char"] == "color":
        r = int(args["red"])
        g = int(args["green"])
        b = int(args["blue"])
        controller.change_color((r, g, b))
    return f"Changed {args['char']} of {addr}."

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)
    addr = sys.argv[1]
    controller = GoveeBLController(addr)
    app.run(host = "192.168.1.124", port = 5000)