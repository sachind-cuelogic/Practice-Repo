This is private message service of audetei SnapHelp project.

It's motive is user and agent can chat with each other privately.
No one can see private message, only user and agent can see.

To run this microservice in container we need docker to be installed on machine.

Install docker as follows:
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
	sudo apt-get update
	apt-cache policy docker-ce
	sudo apt-get install -y docker-ce
	sudo systemctl status docker

Steps To Install Private message service:
	1. create Dockerfile and docker-compose.yaml file
	2. run command : docker-compose build for building docker image 
	3. run command : docker-compose run for running images in different containers.