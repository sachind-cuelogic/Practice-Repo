Comment_Service is one of microservice of Audetemi project

it is used to handle user's public comments

To run this microservice in container we need docker to be installed on machine.

Install docker as follows:
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
	sudo apt-get update
	apt-cache policy docker-ce
	sudo apt-get install -y docker-ce
	sudo systemctl status docker

Steps To Install Comment_Service:
	1. create Dockerfile and docker-compose.yaml file
	2. run command : docker-compose build for building docker image 
	3. run command : docker-compose run for running images in different containers.