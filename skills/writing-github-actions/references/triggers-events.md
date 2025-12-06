# GitHub Actions Triggers and Events

Complete reference for workflow triggers, event types, and activity filters.

## Event Categories

### Code Events
- `push` - Code pushed to repository
- `pull_request` - Pull request activity
- `pull_request_target` - Pull request targeting base branch (safe for secrets)
- `create` - Branch or tag created
- `delete` - Branch or tag deleted

### Repository Events
- `release` - Release published, created, edited
- `watch` - Repository starred
- `fork` - Repository forked
- `issues` - Issue activity
- `issue_comment` - Issue/PR comment activity
- `discussion` - Discussion activity

### Workflow Events
- `workflow_dispatch` - Manual trigger
- `workflow_call` - Reusable workflow
- `workflow_run` - Triggered by another workflow
- `repository_dispatch` - Webhook trigger

### Scheduled Events
- `schedule` - Cron-based trigger

### Deployment Events
- `deployment` - Deployment created
- `deployment_status` - Deployment status changed

For complete syntax examples, see `workflow-syntax.md`.
