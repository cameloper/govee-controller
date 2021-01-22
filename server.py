from controller import GoveeBLController
from flask import Flask, request
import sys
import json

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
        color = tuple(int(args["value"][i:i+2], 16) for i in (0, 2, 4))
        controller.change_color(color)
    return f"Changed {args['char']} of {addr}."

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {format(sys.argv[0])} <config file path>")
        sys.exit(1)
    conf_path = sys.argv[1]

    conf_data = ""
    with open(conf_path, 'r') as conf_file:
        conf_data = conf_file.read()

    conf_dict = json.loads(conf_data)
    addr = conf_dict["device.bl_address"]
    host = conf_dict["server.address"]
    port = conf_dict["server.port"]

    controller = GoveeBLController(addr)
    print(f"Starting GoveeBLController with {addr}")
    app.run(host = host, port = port)