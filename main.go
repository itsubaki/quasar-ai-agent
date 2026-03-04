package main

import (
	"context"
	"os"

	"github.com/modelcontextprotocol/go-sdk/mcp"
	"google.golang.org/adk/agent"
	"google.golang.org/adk/agent/llmagent"
	"google.golang.org/adk/cmd/launcher"
	"google.golang.org/adk/cmd/launcher/full"
	"google.golang.org/adk/model/gemini"
	"google.golang.org/adk/tool"
	"google.golang.org/adk/tool/mcptoolset"
	"google.golang.org/genai"
)

var (
	projectID = os.Getenv("GOOGLE_CLOUD_PROJECT")
	location  = os.Getenv("GOOGLE_CLOUD_LOCATION")
	model     = os.Getenv("GOOGLE_CLOUD_AI_MODEL")
	endpoint  = os.Getenv("QUASAR_MCP_ENDPOINT")
)

func main() {
	ctx := context.Background()
	m, err := gemini.NewModel(ctx, model, &genai.ClientConfig{
		Project:  projectID,
		Location: location,
	})
	if err != nil {
		panic(err)
	}

	toolset, err := mcptoolset.New(mcptoolset.Config{
		Transport: &mcp.StreamableClientTransport{
			Endpoint: endpoint,
		},
	})
	if err != nil {
		panic(err)
	}

	a, err := llmagent.New(llmagent.Config{
		Name:        "quantum_computation_specialist",
		Description: "Answers user questions about the Quantum Computation and Quantum Information.",
		Instruction: "You are a helpful agent who can answer user questions about the Quantum Computation and Quantum Information.",
		Model:       m,
		Toolsets: []tool.Toolset{
			toolset,
		},
	})
	if err != nil {
		panic(err)
	}

	if err := full.NewLauncher().Execute(ctx, &launcher.Config{
		AgentLoader: agent.NewSingleLoader(a),
	}, os.Args[1:]); err != nil {
		panic(err)
	}
}
