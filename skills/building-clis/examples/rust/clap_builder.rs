/*
Clap Builder API Example

Demonstrates: Programmatic CLI construction with builder API

Dependencies (Cargo.toml):
    [dependencies]
    clap = "4.5"

Usage:
    cargo run -- Alice
    cargo run -- Bob --formal
*/

use clap::{Arg, Command};

fn main() {
    let matches = Command::new("greet")
        .about("Greet someone with a friendly message")
        .arg(
            Arg::new("name")
                .help("Name of the person to greet")
                .required(true)
                .index(1),
        )
        .arg(
            Arg::new("formal")
                .long("formal")
                .help("Use formal greeting")
                .action(clap::ArgAction::SetTrue),
        )
        .arg(
            Arg::new("count")
                .short('c')
                .long("count")
                .help("Number of times to greet")
                .value_parser(clap::value_parser!(u32))
                .default_value("1"),
        )
        .get_matches();

    let name = matches.get_one::<String>("name").unwrap();
    let formal = matches.get_flag("formal");
    let count = matches.get_one::<u32>("count").unwrap();

    let greeting = if formal { "Good day" } else { "Hello" };

    for _ in 0..*count {
        println!("{}, {}!", greeting, name);
    }
}
