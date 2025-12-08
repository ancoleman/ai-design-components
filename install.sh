#!/bin/bash
#
# AI Design Components - Installer v3.0
#
# Comprehensive installer for managing marketplace and plugins.
#
# Usage:
#   ./install.sh                        # Interactive mode
#   ./install.sh marketplace add        # Add marketplace from GitHub
#   ./install.sh marketplace add-local  # Add marketplace from local path
#   ./install.sh marketplace remove     # Remove marketplace
#   ./install.sh plugins install-all    # Install all 19 plugins
#   ./install.sh plugins install NAME   # Install single plugin
#   ./install.sh plugins uninstall NAME # Uninstall single plugin
#   ./install.sh plugins uninstall-all  # Uninstall all plugins
#   ./install.sh validate               # Validate marketplace
#   ./install.sh commands               # Install /skillchain globally
#   ./install.sh --help                 # Show help
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
NC='\033[0m'

# Script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Version
VERSION="3.0.0"

# GitHub repo info
GITHUB_REPO="ancoleman/ai-design-components"
MARKETPLACE_NAME="ai-design-components"

# All available plugins (19 total)
ALL_PLUGINS=(
    "ui-foundation-skills"
    "ui-data-skills"
    "ui-input-skills"
    "ui-interaction-skills"
    "ui-structure-skills"
    "ui-content-skills"
    "ui-assembly-skills"
    "backend-data-skills"
    "backend-api-skills"
    "backend-platform-skills"
    "backend-ai-skills"
    "devops-skills"
    "infrastructure-skills"
    "security-skills"
    "developer-productivity-skills"
    "data-engineering-skills"
    "ai-ml-skills"
    "cloud-provider-skills"
    "finops-skills"
)

#######################################
# Print banner
#######################################
print_banner() {
    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}     ${BOLD}AI Design Components${NC} - Installer v${VERSION}                      ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}                                                                   ${BLUE}║${NC}"
    echo -e "${BLUE}║${NC}     ${CYAN}76 Skills${NC} across ${CYAN}19 Plugins${NC} for Claude Code                 ${BLUE}║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

#######################################
# Print usage
#######################################
print_usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo ""
    echo -e "  ${BOLD}Marketplace Management:${NC}"
    echo "    marketplace add         Add marketplace from GitHub"
    echo "    marketplace add-local   Add marketplace from local directory"
    echo "    marketplace remove      Remove marketplace"
    echo "    marketplace list        List configured marketplaces"
    echo "    marketplace update      Update marketplace"
    echo ""
    echo -e "  ${BOLD}Plugin Management:${NC}"
    echo "    plugins install-all     Install all 19 plugins"
    echo "    plugins install NAME    Install single plugin"
    echo "    plugins uninstall NAME  Uninstall single plugin"
    echo "    plugins uninstall-all   Uninstall all plugins"
    echo "    plugins list            List available plugins"
    echo ""
    echo -e "  ${BOLD}Other:${NC}"
    echo "    validate                Validate marketplace manifest"
    echo "    commands                Install /skillchain command globally"
    echo "    help                    Show this help message"
    echo ""
    echo "Interactive mode (no arguments) provides guided setup."
    echo ""
}

#######################################
# Check if Claude CLI is available
#######################################
check_claude_cli() {
    if command -v claude &> /dev/null; then
        return 0
    else
        echo -e "${RED}Error: Claude Code CLI not found${NC}"
        echo ""
        echo "The 'claude' command must be available in your PATH."
        echo "Make sure Claude Code is installed and the CLI is accessible."
        echo ""
        echo "Alternative: Run these commands from within Claude Code:"
        return 1
    fi
}

#######################################
# Marketplace: Add from GitHub
#######################################
marketplace_add() {
    echo -e "${CYAN}Adding marketplace from GitHub...${NC}"
    echo ""

    if check_claude_cli; then
        echo -e "Running: ${GREEN}claude plugin marketplace add ${GITHUB_REPO}${NC}"

        # Try to add, handle "already installed" case
        if ! claude plugin marketplace add "${GITHUB_REPO}" 2>&1; then
            echo ""
            echo -e "${YELLOW}Marketplace may already be installed.${NC}"
            echo -e "To update: ${GREEN}claude plugin marketplace update ${MARKETPLACE_NAME}${NC}"
            echo -e "To reinstall: ${GREEN}claude plugin marketplace rm ${MARKETPLACE_NAME}${NC} first"
            echo ""
            return 0  # Don't fail - marketplace exists
        fi
        echo ""
        echo -e "${GREEN}✓ Marketplace added successfully${NC}"
    else
        echo "  claude plugin marketplace add ${GITHUB_REPO}"
    fi
}

#######################################
# Marketplace: Add from local
#######################################
marketplace_add_local() {
    echo -e "${CYAN}Adding marketplace from local directory...${NC}"
    echo ""

    # Verify marketplace.json exists
    if [[ ! -f "$SCRIPT_DIR/.claude-plugin/marketplace.json" ]]; then
        echo -e "${RED}Error: .claude-plugin/marketplace.json not found${NC}"
        exit 1
    fi

    if check_claude_cli; then
        echo -e "Running: ${GREEN}claude plugin marketplace add ${SCRIPT_DIR}${NC}"
        claude plugin marketplace add "${SCRIPT_DIR}"
        echo ""
        echo -e "${GREEN}✓ Marketplace added successfully${NC}"
    else
        echo "  claude plugin marketplace add ${SCRIPT_DIR}"
    fi
}

#######################################
# Marketplace: Remove
#######################################
marketplace_remove() {
    echo -e "${CYAN}Removing marketplace...${NC}"
    echo ""

    if check_claude_cli; then
        echo -e "Running: ${GREEN}claude plugin marketplace rm ${MARKETPLACE_NAME}${NC}"
        claude plugin marketplace rm "${MARKETPLACE_NAME}" || true
        echo ""
        echo -e "${GREEN}✓ Marketplace removed${NC}"
    else
        echo "  claude plugin marketplace rm ${MARKETPLACE_NAME}"
    fi
}

#######################################
# Marketplace: List
#######################################
marketplace_list() {
    echo -e "${CYAN}Listing configured marketplaces...${NC}"
    echo ""

    if check_claude_cli; then
        claude plugin marketplace list
    else
        echo "  claude plugin marketplace list"
    fi
}

#######################################
# Marketplace: Update
#######################################
marketplace_update() {
    echo -e "${CYAN}Updating marketplace...${NC}"
    echo ""

    if check_claude_cli; then
        echo -e "Running: ${GREEN}claude plugin marketplace update ${MARKETPLACE_NAME}${NC}"
        claude plugin marketplace update "${MARKETPLACE_NAME}"
        echo ""
        echo -e "${GREEN}✓ Marketplace updated${NC}"
    else
        echo "  claude plugin marketplace update ${MARKETPLACE_NAME}"
    fi
}

#######################################
# Plugins: Install all
#######################################
plugins_install_all() {
    echo -e "${CYAN}Installing all ${#ALL_PLUGINS[@]} plugins...${NC}"
    echo ""

    local installed=0
    local failed=0

    if check_claude_cli; then
        for plugin in "${ALL_PLUGINS[@]}"; do
            echo -e "Installing: ${GREEN}${plugin}${NC}"
            if claude plugin install "${plugin}@${MARKETPLACE_NAME}" 2>/dev/null; then
                ((installed++))
            else
                echo -e "  ${YELLOW}(already installed or error)${NC}"
                ((installed++))  # Count as installed if already present
            fi
        done

        echo ""
        echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}  Installation Complete!${NC}"
        echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "  Installed: ${installed}/${#ALL_PLUGINS[@]} plugins"
        echo ""
        echo -e "  ${YELLOW}Restart Claude Code to load new plugins.${NC}"
    else
        echo "Run these commands:"
        echo ""
        for plugin in "${ALL_PLUGINS[@]}"; do
            echo "  claude plugin install ${plugin}@${MARKETPLACE_NAME}"
        done
    fi
}

#######################################
# Plugins: Install single
#######################################
plugins_install() {
    local plugin_name="$1"

    if [[ -z "$plugin_name" ]]; then
        echo -e "${RED}Error: Plugin name required${NC}"
        echo ""
        echo "Usage: $0 plugins install PLUGIN_NAME"
        echo ""
        echo "Available plugins:"
        for plugin in "${ALL_PLUGINS[@]}"; do
            echo "  - ${plugin}"
        done
        exit 1
    fi

    echo -e "${CYAN}Installing plugin: ${plugin_name}${NC}"
    echo ""

    if check_claude_cli; then
        echo -e "Running: ${GREEN}claude plugin install ${plugin_name}@${MARKETPLACE_NAME}${NC}"
        claude plugin install "${plugin_name}@${MARKETPLACE_NAME}"
        echo ""
        echo -e "${GREEN}✓ Plugin installed. Restart Claude Code to load.${NC}"
    else
        echo "  claude plugin install ${plugin_name}@${MARKETPLACE_NAME}"
    fi
}

#######################################
# Plugins: Uninstall single
#######################################
plugins_uninstall() {
    local plugin_name="$1"

    if [[ -z "$plugin_name" ]]; then
        echo -e "${RED}Error: Plugin name required${NC}"
        echo ""
        echo "Usage: $0 plugins uninstall PLUGIN_NAME"
        exit 1
    fi

    echo -e "${CYAN}Uninstalling plugin: ${plugin_name}${NC}"
    echo ""

    if check_claude_cli; then
        echo -e "Running: ${GREEN}claude plugin uninstall ${plugin_name}${NC}"
        claude plugin uninstall "${plugin_name}"
        echo ""
        echo -e "${GREEN}✓ Plugin uninstalled${NC}"
    else
        echo "  claude plugin uninstall ${plugin_name}"
    fi
}

#######################################
# Plugins: Uninstall all
#######################################
plugins_uninstall_all() {
    echo -e "${CYAN}Uninstalling all plugins...${NC}"
    echo ""

    if check_claude_cli; then
        for plugin in "${ALL_PLUGINS[@]}"; do
            echo -e "Uninstalling: ${plugin}"
            claude plugin uninstall "${plugin}" 2>/dev/null || true
        done

        echo ""
        echo -e "${GREEN}✓ All plugins uninstalled${NC}"
    else
        echo "Run these commands:"
        echo ""
        for plugin in "${ALL_PLUGINS[@]}"; do
            echo "  claude plugin uninstall ${plugin}"
        done
    fi
}

#######################################
# Plugins: List available
#######################################
plugins_list() {
    echo -e "${CYAN}Available plugins (${#ALL_PLUGINS[@]} total):${NC}"
    echo ""

    echo -e "  ${BOLD}Frontend:${NC}"
    echo "    ui-foundation-skills     - Design tokens and theming (1 skill)"
    echo "    ui-data-skills           - Data viz, tables, dashboards (3 skills)"
    echo "    ui-input-skills          - Forms, search/filter (2 skills)"
    echo "    ui-interaction-skills    - AI chat, drag-drop, feedback (3 skills)"
    echo "    ui-structure-skills      - Navigation, layouts, timelines (3 skills)"
    echo "    ui-content-skills        - Media, onboarding (2 skills)"
    echo "    ui-assembly-skills       - Component assembly (1 skill)"
    echo ""
    echo -e "  ${BOLD}Backend:${NC}"
    echo "    backend-data-skills      - All database types (6 skills)"
    echo "    backend-api-skills       - API patterns, queues, realtime (3 skills)"
    echo "    backend-platform-skills  - Observability, auth, deployment (3 skills)"
    echo "    backend-ai-skills        - AI data engineering, model serving (2 skills)"
    echo ""
    echo -e "  ${BOLD}DevOps & Infrastructure:${NC}"
    echo "    devops-skills            - CI/CD, GitOps, testing (6 skills)"
    echo "    infrastructure-skills    - Kubernetes, IaC, networking (12 skills)"
    echo ""
    echo -e "  ${BOLD}Security:${NC}"
    echo "    security-skills          - Security architecture, compliance (7 skills)"
    echo ""
    echo -e "  ${BOLD}Developer Productivity:${NC}"
    echo "    developer-productivity-skills - API design, CLI, SDK (7 skills)"
    echo ""
    echo -e "  ${BOLD}Data Engineering:${NC}"
    echo "    data-engineering-skills  - Data pipelines, SQL (6 skills)"
    echo ""
    echo -e "  ${BOLD}AI/ML:${NC}"
    echo "    ai-ml-skills             - MLOps, prompt engineering (4 skills)"
    echo ""
    echo -e "  ${BOLD}Cloud Providers:${NC}"
    echo "    cloud-provider-skills    - AWS, GCP, Azure (3 skills)"
    echo ""
    echo -e "  ${BOLD}FinOps:${NC}"
    echo "    finops-skills            - Cost optimization, tagging (2 skills)"
    echo ""
    echo -e "  ${BOLD}Total: 76 skills across 19 plugins${NC}"
}

#######################################
# Validate marketplace
#######################################
do_validate() {
    echo -e "${CYAN}Validating marketplace...${NC}"
    echo ""

    local manifest="$SCRIPT_DIR/.claude-plugin/marketplace.json"

    if [[ ! -f "$manifest" ]]; then
        echo -e "${RED}Error: marketplace.json not found${NC}"
        exit 1
    fi

    if check_claude_cli; then
        echo -e "Running: ${GREEN}claude plugin validate ${manifest}${NC}"
        claude plugin validate "${manifest}"
        echo ""
        echo -e "${GREEN}✓ Validation complete${NC}"
    else
        echo "  claude plugin validate ${manifest}"
    fi
}

#######################################
# Install /skillchain command globally
#######################################
install_commands() {
    local claude_dir="$HOME/.claude"
    local commands_dir="$claude_dir/commands"

    echo -e "${CYAN}Installing /skillchain command globally...${NC}"
    echo ""

    # Create commands directory
    mkdir -p "$commands_dir"

    # Copy skillchain.md (the router)
    if [[ -f "$SCRIPT_DIR/.claude-commands/skillchain.md" ]]; then
        cp "$SCRIPT_DIR/.claude-commands/skillchain.md" "$commands_dir/skillchain.md"
        echo -e "${GREEN}✓${NC} Installed skillchain.md"
    else
        echo -e "${RED}Error: .claude-commands/skillchain.md not found${NC}"
        exit 1
    fi

    # Copy skillchain resources directory
    if [[ -d "$SCRIPT_DIR/.claude-commands/skillchain" ]]; then
        rm -rf "$commands_dir/skillchain" 2>/dev/null || true
        cp -r "$SCRIPT_DIR/.claude-commands/skillchain" "$commands_dir/skillchain"
        echo -e "${GREEN}✓${NC} Installed skillchain resources"
    fi

    echo ""
    echo -e "${GREEN}✓ /skillchain command installed to ${commands_dir}${NC}"
    echo ""
    echo "Usage:"
    echo "  /skillchain help"
    echo "  /skillchain dashboard with charts"
    echo "  /skillchain kubernetes with monitoring"
}

#######################################
# Interactive mode
#######################################
interactive_mode() {
    echo -e "${CYAN}What would you like to do?${NC}"
    echo ""
    echo -e "  ${BOLD}1)${NC} ${GREEN}Quick Install${NC} - Add marketplace + install all plugins"
    echo -e "  ${BOLD}2)${NC} ${YELLOW}Marketplace Only${NC} - Just add the marketplace"
    echo -e "  ${BOLD}3)${NC} ${MAGENTA}Select Plugins${NC} - Choose which plugins to install"
    echo -e "  ${BOLD}4)${NC} ${CYAN}Uninstall${NC} - Remove marketplace and plugins"
    echo -e "  ${BOLD}5)${NC} ${BLUE}List Plugins${NC} - Show available plugins"
    echo -e "  ${BOLD}6)${NC} Help - Show all commands"
    echo ""
    read -p "Enter choice [1-6]: " choice

    case $choice in
        1)
            marketplace_add
            echo ""
            plugins_install_all
            ;;
        2)
            marketplace_add
            echo ""
            echo -e "${CYAN}Next steps:${NC}"
            echo "  ./install.sh plugins install-all    # Install all plugins"
            echo "  ./install.sh plugins install NAME   # Install specific plugin"
            ;;
        3)
            plugins_list
            echo ""
            echo -e "${CYAN}To install specific plugins:${NC}"
            echo "  ./install.sh plugins install PLUGIN_NAME"
            ;;
        4)
            echo -e "${YELLOW}This will remove all plugins and the marketplace.${NC}"
            read -p "Continue? [y/N]: " confirm
            if [[ "$confirm" =~ ^[Yy]$ ]]; then
                plugins_uninstall_all
                echo ""
                marketplace_remove
            fi
            ;;
        5)
            plugins_list
            ;;
        6)
            print_usage
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            exit 1
            ;;
    esac
}

#######################################
# Main
#######################################
main() {
    print_banner

    # No arguments - interactive mode
    if [[ $# -eq 0 ]]; then
        interactive_mode
        exit 0
    fi

    # Parse command
    local command="$1"
    shift

    case "$command" in
        marketplace)
            local subcommand="${1:-}"
            shift || true
            case "$subcommand" in
                add)
                    marketplace_add
                    ;;
                add-local)
                    marketplace_add_local
                    ;;
                remove|rm)
                    marketplace_remove
                    ;;
                list)
                    marketplace_list
                    ;;
                update)
                    marketplace_update
                    ;;
                *)
                    echo -e "${RED}Unknown marketplace command: ${subcommand}${NC}"
                    echo "Available: add, add-local, remove, list, update"
                    exit 1
                    ;;
            esac
            ;;
        plugins)
            local subcommand="${1:-}"
            shift || true
            case "$subcommand" in
                install-all)
                    plugins_install_all
                    ;;
                install)
                    plugins_install "$1"
                    ;;
                uninstall)
                    plugins_uninstall "$1"
                    ;;
                uninstall-all)
                    plugins_uninstall_all
                    ;;
                list)
                    plugins_list
                    ;;
                *)
                    echo -e "${RED}Unknown plugins command: ${subcommand}${NC}"
                    echo "Available: install-all, install, uninstall, uninstall-all, list"
                    exit 1
                    ;;
            esac
            ;;
        validate)
            do_validate
            ;;
        commands)
            install_commands
            ;;
        help|--help|-h)
            print_usage
            ;;
        *)
            echo -e "${RED}Unknown command: ${command}${NC}"
            print_usage
            exit 1
            ;;
    esac
}

main "$@"
