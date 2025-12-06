/*
Clap Subcommands Example

Demonstrates: Multi-command CLI with subcommands

Dependencies (Cargo.toml):
    [dependencies]
    clap = { version = "4.5", features = ["derive"] }

Usage:
    cargo run -- deploy --env prod
    cargo run -- logs --follow
*/

use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "myapp")]
#[command(about = "Application management CLI", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Deploy the application
    Deploy {
        /// Target environment
        #[arg(long)]
        env: String,

        /// Simulate deployment
        #[arg(long)]
        dry_run: bool,

        /// Version to deploy
        #[arg(long, default_value = "latest")]
        version: String,
    },
    /// View application logs
    Logs {
        /// Follow log output
        #[arg(short, long)]
        follow: bool,

        /// Number of lines to show
        #[arg(short = 'n', long, default_value_t = 10)]
        lines: u32,
    },
    /// Show application status
    Status,
}

fn main() {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Deploy { env, dry_run, version } => {
            if *dry_run {
                println!("[DRY RUN] Would deploy version {} to {}", version, env);
            } else {
                println!("Deploying version {} to {}...", version, env);
                println!("✓ Deployment successful!");
            }
        }
        Commands::Logs { follow, lines } => {
            println!("Showing last {} lines...", lines);
            for i in 1..=*lines {
                println!("[{:03}] Log line {}", i, i);
            }
            if *follow {
                println!("\nFollowing logs... (Press Ctrl+C to stop)");
            }
        }
        Commands::Status => {
            println!("Application Status:");
            println!("  Application: myapp");
            println!("  Status: Running");
            println!("  Uptime: 2 days");
            println!("  Version: v1.2.3");
        }
    }
}
