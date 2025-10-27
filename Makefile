run-api-server:
	poetry run python api_server.py


run-worker:
	poetry run taskiq worker worker:tiq_broker --use-process-pool --workers 4 -fsd --tasks-pattern "tiq_tasks/*.py" --log-level INFO

IMAGE_NAME=loadtestem
API_CONTAINER_NAME=loadtestem-api
WORKER_CONTAINER_NAME=loadtestem-worker

docker-build:
	sudo docker build -t ${IMAGE_NAME} .

docker-api-up:
	sudo docker run -d -p 9001:9001 --name ${API_CONTAINER_NAME} ${IMAGE_NAME} make run-api-server

docker-api-down:
	sudo docker rm -f ${API_CONTAINER_NAME}

docker-api-logs:
	sudo docker logs -f ${API_CONTAINER_NAME}


docker-api-restart:
	make docker-build
	make -i docker-api-down
	make docker-api-up
	make docker-api-logs

# Docker Worker container
docker-worker-up:
	sudo docker run -d --name ${WORKER_CONTAINER_NAME} ${IMAGE_NAME} make run-worker

docker-worker-down:
	sudo docker rm -f ${WORKER_CONTAINER_NAME}

docker-worker-logs:
	sudo docker logs -f ${WORKER_CONTAINER_NAME}

docker-worker-restart:
	make docker-build
	make -i docker-worker-down
	make docker-worker-up
	make docker-worker-logs

