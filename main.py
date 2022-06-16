#imports
from flask import Flask, render_template, request, Request
from waitress import serve
from pysondb import PysonDB
import socket, html

#get ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
s.close()

#init vars
db = PysonDB("data.json")
app = Flask(__name__)

#init constants
HOST = "0.0.0.0"
THREADS = 6
PORT = 8080

#gets all of the names
def getNames():
	for id, value in db.get_all().items():
		yield value["name"]+":"+str(id)

#sets up the data part of the website
@app.route("/data", methods=['POST', 'GET'])
def names():
	#if it is getting data, return all of the names
	if request.method == 'GET':
		return render_template("allData.html", names=getNames())
	#if it is sending data, give them the data
	else:
		id = html.escape(request.form["id"])
		data = db.get_by_id(id)

		return render_template("name.html", name=data["name"], id=id, pro=data["pro"], ssn=data["ssn"])

#sets up the index part of the website
@app.route("/", methods=['POST', 'GET'])
def index():
	#if it is getting data, return the normal part of the website
	if request.method == 'GET':
		return render_template("index.html")
	#if it is sending data, insult them
	else:
		name = html.escape(request.form["name"])
		pro = html.escape(request.form["pro"])
		ssn = html.escape(request.form["ssn"])
		db.add({"name": name, "pro": pro, "ssn": ssn})
		return render_template("greeting.html", name=name, pro=pro, ssn=ssn)

#if it is not being imported print the name and ip address and start up the website
if __name__ == '__main__':
	print(f"starting\nip: {IP}\nport: {PORT}")
	serve(app, host=HOST, port=PORT, threads=THREADS)