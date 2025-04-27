# quasar-agent

 * quasar Agent using the Agent Development Kit

[Factoring](factoring.png)

```shell
adk web
```

## Installation

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install google-adk
gcloud auth application-default login
```

## Environment

```
# agent/.env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_CLOUD_LOCATION=us-central1
COMMAND=/go/bin/quasar-mcp-server
BASE_URL=https://CLOUD_RUN_URL.a.run.app
GCLOUD_PATH=/google-cloud-sdk/bin/gcloud
```

## Links

 * [Agent Development Kit](https://google.github.io/adk-docs/)
