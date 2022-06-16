from flask import Flask, render_template, request, Request
from waitress import serve
from pysondb import PysonDB
import socket, html

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
s.close()

db = PysonDB("data.json")

app = Flask(__name__)

HOST = "0.0.0.0"
THREADS = 6
PORT = 8080

def getNames():
	data = db.get_all().items()
	for id, value in data:
		yield value["name"]+":"+str(id)
	
	idx = len(data)
	while True:
		data = db.get_all()
		if len(data) != idx:
			id, value = data[idx]
			yield value["name"]+":"+str(id)
			idx += 1

@app.route("/data", methods=['POST', 'GET'])
def names():
	if request.method == 'GET':
		return render_template("allData.html", names=getNames())
	else:
		id = html.escape(request.form["id"])
		data = db.get_by_id(id)

		return render_template("name.html", name=data["name"], id=id, pro=data["pro"], ssn=data["ssn"])

@app.route("/", methods=['POST', 'GET'])
def index():
	if request.method == 'GET':
		return render_template("index.html")
	else:
		name = html.escape(request.form["name"])
		pro = html.escape(request.form["pro"])
		ssn = html.escape(request.form["ssn"])
		db.add({"name": name, "pro": pro, "ssn": ssn})
		return render_template("greeting.html", name=name, pro=pro, ssn=ssn)

if __name__ == '__main__':
	print(f"starting\nip: {IP}\nport: {PORT}")
	serve(app, host=HOST, port=PORT, threads=THREADS)
