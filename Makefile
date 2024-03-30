FEATURE_NAME := hangman
TAG ?= latest

app:
	docker run --rm \
	-p 8501:8501 \
	-v $(HOME)/.config/gcloud/application_default_credentials.json/:/root/.config/gcloud/application_default_credentials.json/ \
	${FEATURE_NAME}:${TAG} 

build:
	docker build -t ${FEATURE_NAME}:${TAG} .

lint:
	isort ./src
	black ./src
	flake8 ./src
	mypy --ignore-missing-imports ./src