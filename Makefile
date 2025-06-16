SHELL := /bin/bash

SERVICE_NAME := quasar-ai-agent
REGION := asia-northeast1
PROJECT_ID := $(shell gcloud config get-value project)
IMAGE := ${REGION}-docker.pkg.dev/${PROJECT_ID}/${SERVICE_NAME}/app
TAG := latest

install:
	python3 -m venv .venv
	source .venv/bin/activate
	pip install google-adk

update:
	pip install --upgrade google-adk

web:
	adk web

deploy:
	adk deploy cloud_run --project=${PROJECT_ID} --region=${REGION} --service_name=${SERVICE_NAME} --with_ui ./quasar

proxy:
	gcloud run services proxy ${SERVICE_NAME} --region ${REGION} --port=3001

proxy-mcp:
	gcloud run services proxy quasar-mcp-server --region ${REGION} --port=3000
