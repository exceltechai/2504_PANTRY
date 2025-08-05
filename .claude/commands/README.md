# Claude Code Custom Commands

This directory contains custom commands for Claude Code. These commands can be invoked using slash notation (e.g., `/prime`, `/fix`, `/commit-and-push`).

## Available Commands

### Project Management
- **`/prime`** - Load project context by reading README, PLANNING.md, and TASK.md
- **`/build-planning`** - Create initial PLANNING.md and TASK.md files for project setup
- **`/commit-and-push`** - Add, commit, and push changes with semantic commit messages

### Development & Debugging
- **`/fix`** - Debug and fix terminal errors using available MCP tools
- **`/coverage`** - Analyze and improve code test coverage to 100%
- **`/nested-mvc`** - Structure code using nested Model-View-Controller architecture

### Code Review & Quality
- **`/review-diff`** - Comprehensive review of git diffs for bugs, tests, and alignment
- **`/review-pr`** - Structured pull request review process

### GitHub Integration
- **`/create-gh-issue`** - Create well-structured GitHub issues with study > planning > approval workflow
- **`/fix-gh-issue`** - Fix GitHub issues following structured analysis and implementation
- **`/open-pr`** - Open pull requests with proper formatting and documentation

### Utilities
- **`/domain-search`** - Generate and validate domain name ideas using whois lookup
- **`/add-claude-command`** - Bootstrap new custom commands (meta-command)

## Usage

1. Make sure `.claude/settings.json` has `"customCommands": true`
2. Use commands by typing `/command-name` in Claude Code
3. Commands will guide you through their specific workflows

## Adding New Commands

Use `/add-claude-command` to create new commands, or manually create `.md` files in this directory following the existing patterns.

## Command Structure

Each command file should:
- Have a clear, descriptive filename
- Include a title and brief description
- Provide step-by-step instructions
- Be specific and actionable
- Follow consistent formatting