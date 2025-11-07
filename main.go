package main

import (
	"context"
	"os"

	"github.com/modelcontextprotocol/go-sdk/mcp"
	"google.golang.org/adk/agent/llmagent"
	"google.golang.org/adk/cmd/launcher/adk"
	"google.golang.org/adk/cmd/launcher/full"
	"google.golang.org/adk/model/gemini"
	"google.golang.org/adk/server/restapi/services"
	"google.golang.org/adk/tool"
	"google.golang.org/adk/tool/mcptoolset"
	"google.golang.org/genai"
)

func main() {
	ctx := context.Background()
	model, err := gemini.NewModel(ctx, "gemini-2.5-flash", &genai.ClientConfig{
		Project:  os.Getenv("GOOGLE_CLOUD_PROJECT"),
		Location: os.Getenv("GOOGLE_CLOUD_LOCATION"),
	})
	if err != nil {
		panic(err)
	}

	toolset, err := mcptoolset.New(mcptoolset.Config{
		Transport: &mcp.StreamableClientTransport{
			Endpoint: "http://127.0.0.1:3000/mcp",
		},
	})
	if err != nil {
		panic(err)
	}

	agent, err := llmagent.New(llmagent.Config{
		Model:       model,
		Name:        "quantum_computation_specialist",
		Description: "Answers user questions about the Quantum Computation and Quantum Information.",
		Instruction: "You are a helpful agent who can answer user questions about the Quantum Computation and Quantum Information.",
		Toolsets: []tool.Toolset{
			toolset,
		},
	})
	if err != nil {
		panic(err)
	}

	if err = full.NewLauncher().Execute(ctx, &adk.Config{
		AgentLoader: services.NewSingleAgentLoader(agent),
	}, os.Args[1:]); err != nil {
		panic(err)
	}
}
