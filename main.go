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
	endpoint  = os.Getenv("QUASAR_MCP_ENDPOINT")
)

func main() {
	ctx := context.Background()
	a := Must(llmagent.New(llmagent.Config{
		Name:        "quantum_computation_specialist",
		Description: "Answers user questions about the Quantum Computation and Quantum Information.",
		Instruction: "You are a helpful agent who can answer user questions about the Quantum Computation and Quantum Information.",
		Model: Must(gemini.NewModel(ctx, "gemini-2.5-flash", &genai.ClientConfig{
			Project:  projectID,
			Location: location,
		})),
		Toolsets: []tool.Toolset{
			Must(mcptoolset.New(mcptoolset.Config{
				Transport: &mcp.StreamableClientTransport{
					Endpoint: endpoint,
				},
			})),
		},
	}))

	if err := full.NewLauncher().Execute(ctx, &launcher.Config{
		AgentLoader: agent.NewSingleLoader(a),
	}, os.Args[1:]); err != nil {
		panic(err)
	}
}

func Must[T any](v T, err error) T {
	if err != nil {
		panic(err)
	}

	return v
}
