from flask import Flask, render_template, make_response, request, redirect
import docker
import threading
from requests import get

ip_addr = get('https://api.ipify.org').text

docker_client = docker.from_env()

app = Flask(__name__)


def buildandrun(title, runforever):
	docker_client.images.build(path="./uploads", tag=title)
	nproc_limit = docker.types.Ulimit(name='nproc', hard=100)
	cpu_limit = docker.types.Ulimit(name='cpu', hard=2)
	if runforever:
		docker_client.containers.run(image=title, command='tail -f /dev/null', detach=True, name=title+"container", remove=True)  # , ulimits=[nproc_limit, cpu_limit])
	else:
		docker_client.containers.run(image=title, detach=True, name=title+"container", remove=True)#, ulimits=[nproc_limit, cpu_limit])


@app.route('/', methods=['POST', 'GET'])
def create_containers():
	if request.method == "POST":
		resp = make_response(redirect('/'))
		container_title = request.form["containerTitle"]
		num_containers = int(request.form["numContainer"])
		runforever = request.form.get('runforever')
		dockerfile = request.files["dockerfile"]

		dockerfile.save("uploads/" + dockerfile.filename)
		for datafile in request.files.getlist('datafiles'):
			if(datafile.filename != ''):
				datafile.save("uploads/" + datafile.filename)
		for i in range(num_containers):
			print("starting buildandrun")
			t = threading.Thread(target=buildandrun, args=(container_title + str(i), runforever,))
			t.start()
			print("dispatched the task")
		
		return resp
	else:
		resp = make_response(render_template('configure.html'))
		return resp

@app.route('/containers', methods=['GET'])
def list_results():
	rows = []
	for cnt in docker_client.containers.list():
		if cnt.name != "cadvisor":
			rows.append(cnt.name)
	resp = make_response(render_template('containerlist.html', rows=rows, ip=ip_addr))
	return resp

if __name__ == "__main__":
	app.run(host='0.0.0.0')
