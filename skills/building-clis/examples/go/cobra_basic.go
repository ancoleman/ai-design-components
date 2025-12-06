/*
Basic Cobra CLI Example

Demonstrates: Simple single-command CLI with flags

Dependencies:
    go get -u github.com/spf13/cobra@latest

Usage:
    go run cobra_basic.go Alice
    go run cobra_basic.go Bob --formal
*/

package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var formal bool
var count int

var rootCmd = &cobra.Command{
	Use:   "greet [name]",
	Short: "Greet someone with a friendly message",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		name := args[0]
		greeting := "Hello"
		if formal {
			greeting = "Good day"
		}

		for i := 0; i < count; i++ {
			fmt.Printf("%s, %s!\n", greeting, name)
		}
	},
}

func init() {
	rootCmd.Flags().BoolVar(&formal, "formal", false, "Use formal greeting")
	rootCmd.Flags().IntVarP(&count, "count", "c", 1, "Number of times to greet")
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
