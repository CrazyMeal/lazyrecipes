# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LazyRecipes is a newly initialized project. This document will be updated as the project structure and architecture are established.

## Current Status

This is an empty repository that has just been initialized. Project structure, technology stack, and development workflows will be defined as development begins.

## Commit Message Convention

This project follows the Conventional Commits specification. All commit messages must adhere to the following format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files

### Examples
```
feat(auth): add user login functionality
fix(api): resolve null pointer exception in user service
docs(readme): update installation instructions
chore: initialize project with CLAUDE.md
```

### Rules
- Use lowercase for type and scope
- Keep subject line under 50 characters
- Use imperative mood in the subject line ("add" not "added")
- Separate subject from body with a blank line
- Wrap body at 72 characters
- Use body to explain what and why, not how

## Notes for Future Development

When the project structure is established, update this file with:
- Build, test, and development commands
- High-level architecture and design patterns
- Key technical decisions and their rationale
- Integration points and external dependencies
