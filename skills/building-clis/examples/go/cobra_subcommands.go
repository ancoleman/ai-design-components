/*
Cobra Subcommands Example

Demonstrates: Multi-command CLI with subcommands

Dependencies:
    go get -u github.com/spf13/cobra@latest

Usage:
    go run cobra_subcommands.go deploy --env prod
    go run cobra_subcommands.go logs --follow
*/

package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "myapp",
	Short: "Application management CLI",
}

// Deploy command
var deployCmd = &cobra.Command{
	Use:   "deploy",
	Short: "Deploy the application",
	Run: func(cmd *cobra.Command, args []string) {
		env, _ := cmd.Flags().GetString("env")
		dryRun, _ := cmd.Flags().GetBool("dry-run")
		version, _ := cmd.Flags().GetString("version")

		if dryRun {
			fmt.Printf("[DRY RUN] Would deploy version %s to %s\n", version, env)
		} else {
			fmt.Printf("Deploying version %s to %s...\n", version, env)
			fmt.Println("✓ Deployment successful!")
		}
	},
}

// Logs command
var logsCmd = &cobra.Command{
	Use:   "logs",
	Short: "View application logs",
	Run: func(cmd *cobra.Command, args []string) {
		follow, _ := cmd.Flags().GetBool("follow")
		lines, _ := cmd.Flags().GetInt("lines")

		fmt.Printf("Showing last %d lines...\n", lines)

		for i := 1; i <= lines; i++ {
			fmt.Printf("[%03d] Log line %d\n", i, i)
		}

		if follow {
			fmt.Println("\nFollowing logs... (Press Ctrl+C to stop)")
		}
	},
}

// Status command
var statusCmd = &cobra.Command{
	Use:   "status",
	Short: "Show application status",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Application Status:")
		fmt.Println("  Application: myapp")
		fmt.Println("  Status: Running")
		fmt.Println("  Uptime: 2 days")
		fmt.Println("  Version: v1.2.3")
	},
}

func init() {
	// Deploy command flags
	deployCmd.Flags().String("env", "", "Target environment (dev/staging/prod)")
	deployCmd.Flags().Bool("dry-run", false, "Simulate deployment")
	deployCmd.Flags().String("version", "latest", "Version to deploy")
	deployCmd.MarkFlagRequired("env")

	// Logs command flags
	logsCmd.Flags().BoolP("follow", "f", false, "Follow log output")
	logsCmd.Flags().IntP("lines", "n", 10, "Number of lines to show")

	// Add commands to root
	rootCmd.AddCommand(deployCmd, logsCmd, statusCmd)
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
