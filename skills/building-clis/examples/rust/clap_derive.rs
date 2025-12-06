/*
Clap Derive API Example

Demonstrates: Type-safe CLI with derive macros

Dependencies (Cargo.toml):
    [dependencies]
    clap = { version = "4.5", features = ["derive"] }

Usage:
    cargo run -- Alice
    cargo run -- Bob --formal
*/

use clap::Parser;

#[derive(Parser)]
#[command(name = "greet")]
#[command(about = "Greet someone with a friendly message", long_about = None)]
struct Cli {
    /// Name of the person to greet
    name: String,

    /// Use formal greeting
    #[arg(long)]
    formal: bool,

    /// Number of times to greet
    #[arg(short, long, default_value_t = 1)]
    count: u32,
}

fn main() {
    let cli = Cli::parse();

    let greeting = if cli.formal { "Good day" } else { "Hello" };

    for _ in 0..cli.count {
        println!("{}, {}!", greeting, cli.name);
    }
}
