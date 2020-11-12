from flask import Flask, render_template, make_response, request, redirect
import docker
import threading

docker_client = docker.from_env()

app = Flask(__name__)

@app.route('/configure', methods=['GET'])
def configure():
	return render_template('configure.html')

def buildandrun(title):
	docker_client.images.build(path="./uploads", tag = title)
	docker_client.containers.run(title, 'echo HI')


@app.route('/create', methods=['POST', 'GET'])
def create_containers():
	if request.method == "POST":
		resp = make_response(redirect('/create'))
		container_title = request.form["containerTitle"]
		num_containers = request.form["numContainer"]
		print(num_containers)
		dockerfile = request.files["dockerfile"]
		dockerfile.save("uploads/" + dockerfile.filename)
		for datafile in request.files.getlist('datafiles'):
			if(datafile.filename != ''):
				datafile.save("uploads/" + datafile.filename)
		print("starting buildandrun")
		t = threading.Thread(target=buildandrun, args=(container_title))
		t.start()
		print("dispatched the task")
		
		return resp
	else:
		resp = make_response(render_template('configure.html'))
		return resp


if __name__ == "__main__":
	app.run(host='0.0.0.0')