FEATURE_NAME := hangman
TAG ?= latest

app:
	docker run --rm \
	-p 8501:8501 \
	-v $(HOME)/.config/gcloud/application_default_credentials.json/:/root/.config/gcloud/application_default_credentials.json/ \
	${FEATURE_NAME}:${TAG} streamlit run src/app.py --server.port 8501

app_os:
	docker run --rm \
	-p 8501:8501 \
	-v $(PWD)/.env/:/app/.env/ \
	-v $(HOME)/.cache/huggingface/:/root/.cache/huggingface/ \
	${FEATURE_NAME}:${TAG} streamlit run src/app_os.py --server.port 8501

build:
	docker build -t ${FEATURE_NAME}:${TAG} .

lint:
	isort ./src
	black ./src
	flake8 ./src
	mypy --ignore-missing-imports ./src