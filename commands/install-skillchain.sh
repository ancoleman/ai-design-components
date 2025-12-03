#!/bin/bash
#
# AI Design Components - Skillchain Command Installer (v2.1)
#
# This script installs the /skillchain slash command into Claude Code.
# The skillchain command provides a guided workflow for building UI components.
#
# Usage:
#   ./install-skillchain.sh                    # Install to current project
#   ./install-skillchain.sh --global           # Install globally (all projects)
#   ./install-skillchain.sh ~/my-project       # Install to specific project
#   ./install-skillchain.sh -g                 # Short form for global
#
# After installation, use: /skillchain [goal]
# Example: /skillchain dashboard with charts
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Source directory (where this script lives)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLCHAIN_SOURCE="$SCRIPT_DIR/skillchain"

# Parse arguments
GLOBAL_INSTALL=false
TARGET_DIR=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -g|--global)
            GLOBAL_INSTALL=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS] [TARGET_DIR]"
            echo ""
            echo "Options:"
            echo "  -g, --global    Install to ~/.claude/commands (available in all projects)"
            echo "  -h, --help      Show this help message"
            echo ""
            echo "Arguments:"
            echo "  TARGET_DIR      Project directory to install to (default: current directory)"
            echo ""
            echo "Examples:"
            echo "  $0                      # Install to current project"
            echo "  $0 --global             # Install globally for all projects"
            echo "  $0 ~/my-project         # Install to specific project"
            exit 0
            ;;
        *)
            TARGET_DIR="$1"
            shift
            ;;
    esac
done

# Determine installation directory
if [ "$GLOBAL_INSTALL" = true ]; then
    CLAUDE_COMMANDS_DIR="$HOME/.claude/commands"
    INSTALL_TYPE="global"
    INSTALL_SCOPE="all your projects"
else
    if [ -z "$TARGET_DIR" ]; then
        TARGET_DIR="."
    fi
    TARGET_DIR=$(cd "$TARGET_DIR" && pwd)
    CLAUDE_COMMANDS_DIR="$TARGET_DIR/.claude/commands"
    INSTALL_TYPE="project"
    INSTALL_SCOPE="this project only"
fi

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   AI Design Components - Skillchain Command Installer v2.1   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if source directory exists
if [ ! -d "$SKILLCHAIN_SOURCE" ]; then
    echo -e "${RED}Error: skillchain directory not found at $SKILLCHAIN_SOURCE${NC}"
    echo "Make sure you're running this script from the ai-design-components repository."
    exit 1
fi

# Verify critical files exist
REQUIRED_FILES=(
    "$SKILLCHAIN_SOURCE/skillchain.md"
    "$SKILLCHAIN_SOURCE/_registry.yaml"
    "$SKILLCHAIN_SOURCE/_help.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}Error: Required file missing: $file${NC}"
        echo "The skillchain directory appears to be incomplete."
        exit 1
    fi
done

# Show installation type
echo -e "${CYAN}Installation type:${NC} $INSTALL_TYPE"
echo -e "${CYAN}Available in:${NC} $INSTALL_SCOPE"
echo -e "${CYAN}Target:${NC} $CLAUDE_COMMANDS_DIR"
echo ""

# Create commands directory if it doesn't exist
if [ ! -d "$CLAUDE_COMMANDS_DIR" ]; then
    echo -e "${YELLOW}Creating $CLAUDE_COMMANDS_DIR...${NC}"
    mkdir -p "$CLAUDE_COMMANDS_DIR"
fi

# Check if skillchain already exists
if [ -d "$CLAUDE_COMMANDS_DIR/skillchain" ]; then
    echo -e "${YELLOW}Existing skillchain directory found. Updating...${NC}"
    rm -rf "$CLAUDE_COMMANDS_DIR/skillchain"
fi

# Copy entire skillchain directory
echo -e "${YELLOW}Installing skillchain v2.1 command structure...${NC}"
cp -r "$SKILLCHAIN_SOURCE" "$CLAUDE_COMMANDS_DIR/"

# Count installed files
FILE_COUNT=$(find "$CLAUDE_COMMANDS_DIR/skillchain" -type f | wc -l | tr -d ' ')

# Verify installation
if [ -f "$CLAUDE_COMMANDS_DIR/skillchain/skillchain.md" ]; then
    echo ""
    echo -e "${GREEN}✅ Skillchain v2.1 command installed successfully!${NC}"
    echo ""
    echo -e "Location: ${BLUE}$CLAUDE_COMMANDS_DIR/skillchain/${NC}"
    echo -e "Files installed: ${CYAN}$FILE_COUNT${NC}"
    echo ""

    # Show structure
    echo -e "${CYAN}Installed structure:${NC}"
    echo "  skillchain/"
    echo "  ├── skillchain.md         (Router)"
    echo "  ├── _registry.yaml        (Skill registry)"
    echo "  ├── _help.md             (Help content)"
    echo "  ├── _shared/             (Shared rules)"
    echo "  ├── categories/          (Category skills)"
    echo "  └── blueprints/          (Project templates)"
    echo ""

    if [ "$GLOBAL_INSTALL" = true ]; then
        echo -e "${CYAN}Global Installation:${NC}"
        echo "  The /skillchain command is now available in ALL your projects."
        echo "  No additional setup needed per project."
        echo ""
    else
        echo -e "${CYAN}Project Installation:${NC}"
        echo "  The /skillchain command is available in: $TARGET_DIR"
        echo "  Commit .claude/commands/ to share with your team."
        echo ""
    fi

    echo -e "${YELLOW}Usage:${NC}"
    echo "  /skillchain help                    # Show available skills"
    echo "  /skillchain dashboard with charts   # Build a dashboard"
    echo "  /skillchain login form              # Build a login form"
    echo "  /skillchain AI chat interface       # Build a chat UI"
    echo "  /skillchain import CSV to postgres  # Build ETL pipeline"
    echo ""
    echo -e "${YELLOW}The skillchain command will:${NC}"
    echo "  1. Parse your goal and identify required skills"
    echo "  2. Guide you through each skill in the correct order"
    echo "  3. Ask configuration questions for each component"
    echo "  4. Generate themed, accessible code"
    echo ""
    echo -e "${CYAN}v2.1 Features:${NC}"
    echo "  • User preferences saved to ~/.claude/skillchain-prefs.yaml"
    echo "  • Parallel skill loading for faster workflows"
    echo "  • Skill versioning with compatibility tracking"
    echo "  • 29 skills: 15 frontend + 14 backend"
    echo ""
    echo -e "${GREEN}Start Claude Code and try: /skillchain help${NC}"
else
    echo -e "${RED}❌ Installation failed. Please check permissions.${NC}"
    exit 1
fi
