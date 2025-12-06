#!/bin/bash

# Automated Git Hooks Setup
# Installs Husky, lint-staged, and commitlint with recommended configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Git Hooks Setup${NC}"
echo "=================="
echo ""

# Check if package.json exists
if [ ! -f "package.json" ]; then
  echo -e "${RED}❌ package.json not found${NC}"
  echo "This script must be run from the project root"
  exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
  echo -e "${RED}❌ npm is not installed${NC}"
  exit 1
fi

echo -e "${BLUE}📦 Installing dependencies...${NC}"
echo ""

# Install Husky
echo "Installing Husky..."
npm install --save-dev husky

# Install lint-staged
echo "Installing lint-staged..."
npm install --save-dev lint-staged

# Install commitlint
echo "Installing commitlint..."
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# Install ESLint and Prettier (if not already installed)
if ! npm list eslint &> /dev/null; then
  echo "Installing ESLint..."
  npm install --save-dev eslint
fi

if ! npm list prettier &> /dev/null; then
  echo "Installing Prettier..."
  npm install --save-dev prettier
fi

echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Initialize Husky
echo -e "${BLUE}🎣 Initializing Husky...${NC}"
npx husky init

# Create commitlint configuration
echo -e "${BLUE}📝 Creating commitlint configuration...${NC}"
cat > commitlint.config.js << 'EOF'
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'build',
        'ci',
        'chore',
        'revert'
      ]
    ],
    'subject-case': [2, 'never', ['upper-case', 'pascal-case', 'start-case']],
    'header-max-length': [2, 'always', 100],
    'body-max-line-length': [2, 'always', 72],
    'scope-case': [2, 'always', 'lower-case']
  }
};
EOF

echo -e "${GREEN}✅ commitlint.config.js created${NC}"
echo ""

# Create lint-staged configuration
echo -e "${BLUE}📝 Creating lint-staged configuration...${NC}"

# Add lint-staged to package.json
node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
pkg['lint-staged'] = {
  '*.{js,jsx,ts,tsx}': [
    'eslint --fix',
    'prettier --write'
  ],
  '*.{json,md,yml,yaml}': [
    'prettier --write'
  ]
};
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2) + '\n');
"

echo -e "${GREEN}✅ lint-staged configuration added to package.json${NC}"
echo ""

# Create pre-commit hook
echo -e "${BLUE}🎣 Creating pre-commit hook...${NC}"
cat > .husky/pre-commit << 'EOF'
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run lint-staged
npx lint-staged

# Check for console.log in staged files
if git diff --cached | grep -E "^\+.*console\.log"; then
  echo "⚠️  Warning: console.log found in staged files"
  echo "Remove console.log or use --no-verify to skip this check"
  exit 1
fi
EOF

chmod +x .husky/pre-commit
echo -e "${GREEN}✅ pre-commit hook created${NC}"
echo ""

# Create commit-msg hook
echo -e "${BLUE}🎣 Creating commit-msg hook...${NC}"
cat > .husky/commit-msg << 'EOF'
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Validate commit message format
npx --no -- commitlint --edit $1
EOF

chmod +x .husky/commit-msg
echo -e "${GREEN}✅ commit-msg hook created${NC}"
echo ""

# Create pre-push hook
echo -e "${BLUE}🎣 Creating pre-push hook...${NC}"
cat > .husky/pre-push << 'EOF'
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Get current branch
branch=$(git rev-parse --abbrev-ref HEAD)

# Prevent direct push to main
if [ "$branch" = "main" ]; then
  echo "⛔ Cannot push directly to main branch"
  echo "Please create a pull request instead"
  exit 1
fi

# Run tests (if test script exists)
if grep -q '"test"' package.json; then
  echo "🧪 Running tests..."
  npm test
fi
EOF

chmod +x .husky/pre-push
echo -e "${GREEN}✅ pre-push hook created${NC}"
echo ""

# Update package.json scripts
echo -e "${BLUE}📝 Updating package.json scripts...${NC}"

node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));

// Add prepare script for Husky
if (!pkg.scripts) pkg.scripts = {};
pkg.scripts.prepare = 'husky install';

// Add lint and format scripts if they don't exist
if (!pkg.scripts.lint) {
  pkg.scripts.lint = 'eslint . --ext .js,.jsx,.ts,.tsx';
}
if (!pkg.scripts['lint:fix']) {
  pkg.scripts['lint:fix'] = 'eslint . --ext .js,.jsx,.ts,.tsx --fix';
}
if (!pkg.scripts.format) {
  pkg.scripts.format = 'prettier --write .';
}
if (!pkg.scripts['format:check']) {
  pkg.scripts['format:check'] = 'prettier --check .';
}

fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2) + '\n');
"

echo -e "${GREEN}✅ package.json scripts updated${NC}"
echo ""

# Create .prettierrc if it doesn't exist
if [ ! -f ".prettierrc" ]; then
  echo -e "${BLUE}📝 Creating .prettierrc...${NC}"
  cat > .prettierrc << 'EOF'
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false
}
EOF
  echo -e "${GREEN}✅ .prettierrc created${NC}"
  echo ""
fi

# Create .eslintrc.js if it doesn't exist
if [ ! -f ".eslintrc.js" ] && [ ! -f ".eslintrc.json" ]; then
  echo -e "${BLUE}📝 Creating .eslintrc.js...${NC}"
  cat > .eslintrc.js << 'EOF'
module.exports = {
  extends: ['eslint:recommended'],
  env: {
    node: true,
    es2021: true,
  },
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  rules: {
    'no-console': 'warn',
  },
};
EOF
  echo -e "${GREEN}✅ .eslintrc.js created${NC}"
  echo ""
fi

# Summary
echo -e "${GREEN}✅ Git hooks setup complete!${NC}"
echo ""
echo "Installed hooks:"
echo "  • pre-commit  - Runs linting and formatting on staged files"
echo "  • commit-msg  - Validates commit message format"
echo "  • pre-push    - Prevents direct push to main, runs tests"
echo ""
echo "Configuration files created:"
echo "  • commitlint.config.js"
echo "  • .prettierrc"
echo "  • .eslintrc.js"
echo ""
echo "Package.json updated with:"
echo "  • lint-staged configuration"
echo "  • npm scripts (lint, format, prepare)"
echo ""
echo "Usage:"
echo "  npm run lint        - Run ESLint"
echo "  npm run lint:fix    - Fix ESLint issues"
echo "  npm run format      - Format code with Prettier"
echo "  npm test            - Run tests (if configured)"
echo ""
echo "Commit format:"
echo "  <type>[optional scope]: <description>"
echo ""
echo "  Examples:"
echo "    feat: add user authentication"
echo "    fix(api): resolve timeout issue"
echo "    docs: update README"
echo ""
echo "To skip hooks (emergency only):"
echo "  git commit --no-verify"
echo "  git push --no-verify"
echo ""
echo -e "${YELLOW}💡 Test the setup by making a commit!${NC}"
