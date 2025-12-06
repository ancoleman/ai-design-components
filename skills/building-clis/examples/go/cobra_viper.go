/*
Cobra + Viper Configuration Example

Demonstrates: Configuration management with Viper

Dependencies:
    go get -u github.com/spf13/cobra@latest
    go get -u github.com/spf13/viper@latest

Usage:
    go run cobra_viper.go serve
    MYAPP_PORT=9000 go run cobra_viper.go serve
*/

package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var cfgFile string

var rootCmd = &cobra.Command{
	Use:   "myapp",
	Short: "Application with configuration",
}

var serveCmd = &cobra.Command{
	Use:   "serve",
	Short: "Start server",
	Run: func(cmd *cobra.Command, args []string) {
		host := viper.GetString("host")
		port := viper.GetInt("port")

		fmt.Printf("Starting server at %s:%d\n", host, port)
		fmt.Println("\nEffective configuration:")
		fmt.Printf("  Host: %s\n", host)
		fmt.Printf("  Port: %d\n", port)
	},
}

func initConfig() {
	if cfgFile != "" {
		viper.SetConfigFile(cfgFile)
	} else {
		viper.SetConfigName("config")
		viper.SetConfigType("yaml")

		// Config search paths (precedence: local > user > system)
		viper.AddConfigPath(".")
		viper.AddConfigPath("$HOME/.config/myapp")
		viper.AddConfigPath("/etc/myapp")
	}

	// Environment variables (MYAPP_HOST, MYAPP_PORT)
	viper.SetEnvPrefix("MYAPP")
	viper.AutomaticEnv()

	// Read config file
	if err := viper.ReadInConfig(); err == nil {
		fmt.Println("Using config file:", viper.ConfigFileUsed())
	}

	// Set defaults
	viper.SetDefault("host", "localhost")
	viper.SetDefault("port", 8080)
}

func init() {
	cobra.OnInitialize(initConfig)

	// Global config flag
	rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file path")

	// Serve command flags
	serveCmd.Flags().String("host", "", "Server host")
	serveCmd.Flags().Int("port", 0, "Server port")

	// Bind flags to viper
	viper.BindPFlag("host", serveCmd.Flags().Lookup("host"))
	viper.BindPFlag("port", serveCmd.Flags().Lookup("port"))

	rootCmd.AddCommand(serveCmd)
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
