# quasar-ai-agent

- A quasar AI agent using [google/adk-go](https://github.com/google/adk-go).
- A professional in quantum computing and quantum information, able to run OpenQASM 3.x code.

## Examples

```shell
$ go run main.go 
User  -> Please list tools
Agent -> I can run a quantum circuit using OpenQASM 3.0. This tool is called `openqasm3p0_run`.
User  -> 
```

## Installation and Environments

 1. Install the [gcloud CLI](https://docs.cloud.google.com/sdk/docs/install)
 1. Deploy [quasar](https://github.com/itsubaki/quasar) to Cloud Run.
 1. Deploy [quasar-mcp-server](https://github.com/itsubaki/quasar-mcp-server) to Cloud Run.

```shell
# .env
export GOOGLE_GENAI_USE_VERTEXAI=TRUE
export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT
export GOOGLE_CLOUD_LOCATION=asia-northeast1
export QUASAR_MCP_ENDPOINT=http://127.0.0.1:3000/mcp
```

```shell
make proxy-mcp
```
