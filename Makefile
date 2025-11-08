SHELL := /bin/bash

SERVICE_NAME := quasar-ai-agent
REGION := asia-northeast1
PROJECT_ID := $(shell gcloud config get-value project)
IMAGE := ${REGION}-docker.pkg.dev/${PROJECT_ID}/${SERVICE_NAME}/app
TAG := latest
QUASAR_MCP_ENDPOINT := http://127.0.0.1:3000/mcp

update:
	go get -u
	go mod tidy

run:
	QUASAR_MCP_ENDPOINT=${QUASAR_MCP_ENDPOINT} go run main.go

webui:
	QUASAR_MCP_ENDPOINT=${QUASAR_MCP_ENDPOINT} go run main.go web api webui

login:
	gcloud auth application-default login

proxy-mcp:
	gcloud run services proxy quasar-mcp-server --region ${REGION} --port=3000
