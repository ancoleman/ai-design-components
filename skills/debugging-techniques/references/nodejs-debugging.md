# Node.js Debugging Reference

## Table of Contents

1. [Built-in Debugger: node --inspect](#built-in-debugger-node---inspect)
2. [VS Code Integration](#vs-code-integration)
3. [Debugging in Docker](#debugging-in-docker)
4. [Debugging TypeScript](#debugging-typescript)
5. [Debugging Common Frameworks](#debugging-common-frameworks)
6. [Advanced Techniques](#advanced-techniques)
7. [Best Practices](#best-practices)

## Built-in Debugger: node --inspect

### Basic Usage

```bash
# Start with debugger, pause immediately
node --inspect-brk app.js

# Start with debugger, run until breakpoint
node --inspect app.js

# Specify host and port (default: 127.0.0.1:9229)
node --inspect=0.0.0.0:9229 app.js

# Legacy debugger (deprecated)
node --debug app.js  # Don't use
```

### Chrome DevTools Integration

1. Start Node.js with `--inspect` or `--inspect-brk`
2. Open Chrome browser
3. Navigate to `chrome://inspect`
4. Click "Open dedicated DevTools for Node"
5. Set breakpoints, inspect variables, step through code

### Debugging Commands (Chrome DevTools)

- **F8** - Continue execution
- **F10** - Step over
- **F11** - Step into
- **Shift+F11** - Step out
- **Click line number** - Set/remove breakpoint
- **Right-click line** - Conditional breakpoint
- **Watch expressions** - Add in Watch panel
- **Console** - Evaluate expressions

## VS Code Integration

### launch.json Configurations

**Launch current file:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch Program",
      "skipFiles": ["<node_internals>/**"],
      "program": "${workspaceFolder}/app.js"
    }
  ]
}
```

**Launch with arguments:**
```json
{
  "type": "node",
  "request": "launch",
  "name": "Launch with Args",
  "program": "${workspaceFolder}/app.js",
  "args": ["--port", "3000", "--verbose"],
  "skipFiles": ["<node_internals>/**"]
}
```

**Attach to running process:**
```json
{
  "type": "node",
  "request": "attach",
  "name": "Attach to Process",
  "port": 9229,
  "skipFiles": ["<node_internals>/**"]
}
```

**Debug npm script:**
```json
{
  "type": "node",
  "request": "launch",
  "name": "npm start",
  "runtimeExecutable": "npm",
  "runtimeArgs": ["run-script", "start"],
  "skipFiles": ["<node_internals>/**"]
}
```

**Debug tests (Jest):**
```json
{
  "type": "node",
  "request": "launch",
  "name": "Jest Tests",
  "program": "${workspaceFolder}/node_modules/.bin/jest",
  "args": ["--runInBand", "--no-cache"],
  "console": "integratedTerminal",
  "internalConsoleOptions": "neverOpen"
}
```

## Debugging in Docker

### Dockerfile Configuration

```dockerfile
FROM node:18

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Expose app port and debug port
EXPOSE 3000
EXPOSE 9229

# Start with inspector
CMD ["node", "--inspect=0.0.0.0:9229", "app.js"]
```

### docker-compose.yml

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"   # Application port
      - "9229:9229"   # Debug port
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
```

### VS Code Remote Debugging in Docker

**launch.json:**
```json
{
  "type": "node",
  "request": "attach",
  "name": "Attach to Docker",
  "address": "localhost",
  "port": 9229,
  "localRoot": "${workspaceFolder}",
  "remoteRoot": "/app",
  "skipFiles": ["<node_internals>/**"]
}
```

**Steps:**
1. Start Docker container: `docker-compose up`
2. In VS Code: F5 → "Attach to Docker"
3. Set breakpoints in code
4. Trigger code execution (HTTP request, etc.)

## Debugging TypeScript

### Configuration

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "sourceMap": true,  // Generate source maps
    "outDir": "./dist"
  }
}
```

**launch.json:**
```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug TypeScript",
  "preLaunchTask": "tsc: build - tsconfig.json",
  "program": "${workspaceFolder}/src/app.ts",
  "outFiles": ["${workspaceFolder}/dist/**/*.js"],
  "sourceMaps": true
}
```

### Using ts-node

**Direct debugging without compilation:**
```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug TypeScript (ts-node)",
  "runtimeArgs": ["-r", "ts-node/register"],
  "args": ["${workspaceFolder}/src/app.ts"],
  "cwd": "${workspaceFolder}",
  "protocol": "inspector"
}
```

## Debugging Common Frameworks

### Express.js

```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug Express",
  "program": "${workspaceFolder}/server.js",
  "env": {
    "NODE_ENV": "development",
    "PORT": "3000"
  }
}
```

### NestJS

```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug NestJS",
  "runtimeArgs": ["--nolazy", "-r", "ts-node/register", "-r", "tsconfig-paths/register"],
  "args": ["${workspaceFolder}/src/main.ts"],
  "cwd": "${workspaceFolder}",
  "protocol": "inspector"
}
```

### Next.js

```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug Next.js",
  "runtimeExecutable": "npm",
  "runtimeArgs": ["run", "dev"],
  "port": 9229,
  "serverReadyAction": {
    "pattern": "started server on .+, url: (https?://.+)",
    "uriFormat": "%s",
    "action": "debugWithChrome"
  }
}
```

## Advanced Techniques

### Remote Debugging Over SSH

**SSH tunnel:**
```bash
# Forward remote port 9229 to local
ssh -L 9229:localhost:9229 user@remote-server

# On remote server
node --inspect=127.0.0.1:9229 app.js

# In VS Code, connect to localhost:9229
```

### Debugging Worker Threads

```javascript
const { Worker } = require('worker_threads');

const worker = new Worker('./worker.js', {
  execArgv: ['--inspect-brk=9230']  // Different port
});
```

**Connect to worker:**
- Chrome DevTools will show multiple targets
- Or connect VS Code to port 9230

### Debugging Child Processes

```javascript
const { spawn } = require('child_process');

const child = spawn('node', [
  '--inspect-brk=9230',
  'child-script.js'
]);
```

### Conditional Breakpoints in Code

```javascript
function processItem(item) {
  if (item.id === 'problematic-id') {
    debugger;  // Programmatic breakpoint
  }
  // Process item
}
```

### Logging Debug Information

```javascript
// Use debug module
const debug = require('debug')('app:server');

debug('Starting server on port %d', port);
```

**Enable debug logs:**
```bash
DEBUG=app:* node app.js
```

## Best Practices

### 1. Use --inspect-brk for Immediate Pause

```bash
# Good for debugging startup issues
node --inspect-brk app.js
```

### 2. Skip Node Internals

```json
{
  "skipFiles": [
    "<node_internals>/**",
    "node_modules/**"
  ]
}
```

### 3. Use Source Maps for TypeScript

**Always enable in tsconfig.json:**
```json
{
  "compilerOptions": {
    "sourceMap": true
  }
}
```

### 4. Expose Debug Port in Docker

```yaml
ports:
  - "9229:9229"
```

### 5. Use Environment Variables

```json
{
  "env": {
    "NODE_ENV": "development",
    "DEBUG": "*"
  }
}
```

### 6. Chrome DevTools for Quick Debugging

**When:**
- Quick debugging session
- No need for IDE features
- Remote debugging

### 7. VS Code for Project Debugging

**When:**
- Full project debugging
- Multiple debug configurations
- Integrated workflow

### 8. Use debugger; Statement Sparingly

**Only for:**
- Conditional breakpoints in code
- Dynamic debugging points
- One-off investigations

### 9. Clean Up Debug Ports

```bash
# Find process using port 9229
lsof -i :9229

# Kill process
kill <pid>
```

### 10. Security: Don't Expose Debug Port in Production

**Bad:**
```bash
# NEVER in production
node --inspect=0.0.0.0:9229 app.js
```

**Good:**
```bash
# Production
node app.js

# Or bind to localhost only if needed
node --inspect=127.0.0.1:9229 app.js
```
