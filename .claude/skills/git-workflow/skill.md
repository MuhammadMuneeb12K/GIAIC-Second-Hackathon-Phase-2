# Git Workflow Skill

## Overview
You are an expert in Git version control and collaborative development workflows. You specialize in maintaining clean commit history, effective branching strategies, and professional collaboration practices for software development teams.

## Core Competencies

### 1. Git Fundamentals
- **Repository Management**: Initialize, clone, and manage repositories
- **Staging and Committing**: Stage changes and create meaningful commits
- **Branching**: Create, switch, and manage branches effectively
- **Merging**: Merge branches with appropriate strategies
- **Remote Operations**: Push, pull, and sync with remote repositories
- **History Navigation**: View and understand commit history
- **Conflict Resolution**: Resolve merge conflicts properly

### 2. Commit Best Practices
- **Atomic Commits**: Each commit should represent one logical change
- **Commit Messages**: Write clear, descriptive commit messages
- **Conventional Commits**: Follow conventional commit format
- **Commit Frequency**: Commit often but meaningfully
- **Commit Content**: Don't commit secrets, build artifacts, or unnecessary files
- **Co-authoring**: Credit collaborators appropriately

### 3. Branching Strategies
- **Feature Branches**: Create branches for new features
- **Branch Naming**: Use descriptive, consistent branch names
- **Main/Master Branch**: Keep main branch stable and deployable
- **Branch Lifecycle**: Create, develop, merge, and delete branches
- **Long-lived vs Short-lived**: Understand when to use each
- **Branch Protection**: Protect important branches with rules

### 4. Collaboration Workflows
- **Pull Requests**: Create clear, reviewable pull requests
- **Code Review**: Review code effectively and constructively
- **PR Descriptions**: Write comprehensive PR descriptions
- **Addressing Feedback**: Respond to review comments professionally
- **Merge Strategies**: Choose appropriate merge strategies
- **Conflict Resolution**: Handle merge conflicts collaboratively

### 5. Git Hygiene
- **Clean History**: Maintain readable commit history
- **Rebase vs Merge**: Know when to use each
- **Interactive Rebase**: Clean up commits before merging
- **Amending Commits**: Fix recent commits when appropriate
- **Stashing**: Temporarily save work in progress
- **Gitignore**: Properly configure ignored files

## Commit Message Format

### Conventional Commits
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring (no feature or bug fix)
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (dependencies, config)
- **ci**: CI/CD changes
- **build**: Build system changes

### Examples
```bash
# Feature commit
git commit -m "feat(auth): add JWT token refresh functionality

Implement automatic token refresh when access token expires.
Includes retry logic for failed API requests.

Closes #123"

# Bug fix commit
git commit -m "fix(tasks): prevent duplicate task creation

Add debouncing to task creation button to prevent
multiple submissions on rapid clicks.

Fixes #456"

# Documentation commit
git commit -m "docs(api): update authentication endpoint documentation

Add examples for token refresh flow and error responses."

# Refactoring commit
git commit -m "refactor(database): extract query logic into service layer

Move database queries from route handlers to dedicated
service classes for better separation of concerns."
```

## Branch Naming Conventions

### Format
```
<type>/<ticket-id>-<short-description>
```

### Examples
```bash
# Feature branches
feature/AUTH-123-jwt-authentication
feature/TASK-456-task-filtering

# Bug fix branches
fix/BUG-789-login-redirect
fix/TASK-101-duplicate-tasks

# Hotfix branches
hotfix/PROD-001-critical-security-patch

# Chore branches
chore/update-dependencies
chore/setup-ci-pipeline

# Documentation branches
docs/api-documentation
docs/setup-instructions
```

## Common Git Workflows

### Feature Development Workflow
```bash
# 1. Update main branch
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/TASK-123-new-feature

# 3. Make changes and commit
git add .
git commit -m "feat(feature): implement new feature"

# 4. Push to remote
git push -u origin feature/TASK-123-new-feature

# 5. Create pull request (via GitHub/GitLab UI)

# 6. After PR approval, merge and delete branch
git checkout main
git pull origin main
git branch -d feature/TASK-123-new-feature
```

### Keeping Feature Branch Updated
```bash
# Option 1: Merge main into feature branch
git checkout feature/TASK-123-new-feature
git merge main
git push origin feature/TASK-123-new-feature

# Option 2: Rebase feature branch on main (cleaner history)
git checkout feature/TASK-123-new-feature
git rebase main
git push --force-with-lease origin feature/TASK-123-new-feature
```

### Fixing Mistakes

#### Amend Last Commit
```bash
# Fix last commit message
git commit --amend -m "feat(auth): correct commit message"

# Add forgotten files to last commit
git add forgotten-file.ts
git commit --amend --no-edit

# IMPORTANT: Only amend commits that haven't been pushed
# If already pushed, you'll need to force push (use with caution)
git push --force-with-lease origin branch-name
```

#### Undo Changes
```bash
# Discard unstaged changes in a file
git checkout -- file.ts

# Unstage a file (keep changes)
git reset HEAD file.ts

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - DANGEROUS
git reset --hard HEAD~1

# Revert a commit (creates new commit)
git revert <commit-hash>
```

#### Interactive Rebase
```bash
# Clean up last 3 commits
git rebase -i HEAD~3

# In the editor:
# pick abc1234 First commit
# squash def5678 Second commit (will be squashed into first)
# reword ghi9012 Third commit (will edit message)

# After rebase, force push if already pushed
git push --force-with-lease origin branch-name
```

### Stashing Work in Progress
```bash
# Save current work
git stash save "WIP: working on authentication"

# List stashes
git stash list

# Apply most recent stash
git stash apply

# Apply and remove most recent stash
git stash pop

# Apply specific stash
git stash apply stash@{1}

# Delete a stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

## Pull Request Best Practices

### PR Title Format
```
<type>(<scope>): <description>

Examples:
feat(auth): Add JWT authentication
fix(tasks): Resolve duplicate task creation bug
docs(readme): Update installation instructions
```

### PR Description Template
```markdown
## Summary
Brief description of what this PR does and why.

## Changes
- List of specific changes made
- Another change
- One more change

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
Describe how you tested these changes:
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
- [ ] Dependent changes merged

## Related Issues
Closes #123
Relates to #456

## Additional Notes
Any additional context or notes for reviewers.
```

### Creating a Good PR
```bash
# 1. Ensure branch is up to date
git checkout feature/TASK-123-new-feature
git rebase main

# 2. Review your changes
git diff main

# 3. Ensure tests pass
npm test  # or pytest for backend

# 4. Push to remote
git push origin feature/TASK-123-new-feature

# 5. Create PR via GitHub CLI (optional)
gh pr create --title "feat(auth): Add JWT authentication" \
  --body "Implements JWT-based authentication with refresh tokens"

# 6. Or create via web interface
```

## Code Review Guidelines

### As a Reviewer
```markdown
## Review Checklist
- [ ] Code is readable and maintainable
- [ ] Logic is correct and handles edge cases
- [ ] Tests are comprehensive
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Documentation is updated
- [ ] Follows project conventions
- [ ] No unnecessary changes

## Providing Feedback
- Be constructive and specific
- Explain the "why" behind suggestions
- Distinguish between blocking issues and suggestions
- Acknowledge good work
- Ask questions instead of making demands

## Comment Examples

### Blocking Issue
❌ **Blocking**: This introduces a security vulnerability. User input is not sanitized before database query.

### Suggestion
💡 **Suggestion**: Consider extracting this logic into a separate function for better reusability.

### Question
❓ **Question**: What happens if the API returns a 500 error here?

### Praise
✅ **Nice**: Great use of TypeScript generics here!
```

### As a PR Author
```markdown
## Responding to Feedback
- Address all comments
- Mark resolved comments as resolved
- Push new commits for changes (don't force push during review)
- Thank reviewers for their time
- Ask for clarification if needed

## Example Responses
"Good catch! Fixed in commit abc1234"
"I've updated the tests to cover this case"
"That's a great suggestion. I've refactored it accordingly"
"Could you clarify what you mean by...?"
```

## Merge Strategies

### Merge Commit (Default)
```bash
git checkout main
git merge --no-ff feature/TASK-123-new-feature
```
- **Pros**: Preserves complete history, shows when feature was merged
- **Cons**: Creates merge commits, can clutter history
- **Use when**: You want to preserve feature branch history

### Squash and Merge
```bash
git checkout main
git merge --squash feature/TASK-123-new-feature
git commit -m "feat(auth): Add JWT authentication"
```
- **Pros**: Clean linear history, one commit per feature
- **Cons**: Loses individual commit history
- **Use when**: Feature branch has many small commits

### Rebase and Merge
```bash
git checkout feature/TASK-123-new-feature
git rebase main
git checkout main
git merge feature/TASK-123-new-feature
```
- **Pros**: Clean linear history, preserves individual commits
- **Cons**: Rewrites history, can be complex with conflicts
- **Use when**: You want linear history with detailed commits

## Conflict Resolution

### Resolving Merge Conflicts
```bash
# 1. Attempt merge
git merge main
# CONFLICT (content): Merge conflict in file.ts

# 2. View conflicted files
git status

# 3. Open conflicted file and resolve
# Look for conflict markers:
<<<<<<< HEAD
Your changes
=======
Their changes
>>>>>>> main

# 4. Edit file to resolve conflict, removing markers

# 5. Stage resolved files
git add file.ts

# 6. Complete merge
git commit -m "merge: resolve conflicts with main"

# 7. Push changes
git push origin feature/TASK-123-new-feature
```

### Conflict Resolution Tools
```bash
# Use merge tool
git mergetool

# Abort merge if needed
git merge --abort

# Abort rebase if needed
git rebase --abort
```

## Git Configuration

### Essential Configuration
```bash
# Set user information
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Set default editor
git config --global core.editor "code --wait"

# Enable color output
git config --global color.ui auto

# Set pull strategy
git config --global pull.rebase false

# Set push default
git config --global push.default current

# Enable credential caching
git config --global credential.helper cache
```

### Useful Aliases
```bash
# Status shortcut
git config --global alias.st status

# Commit shortcut
git config --global alias.ci commit

# Checkout shortcut
git config --global alias.co checkout

# Branch shortcut
git config --global alias.br branch

# Pretty log
git config --global alias.lg "log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# Undo last commit
git config --global alias.undo "reset --soft HEAD~1"

# Show last commit
git config --global alias.last "log -1 HEAD"
```

## Gitignore Best Practices

### Common Patterns
```gitignore
# Dependencies
node_modules/
venv/
__pycache__/

# Environment variables
.env
.env.local
.env.*.local

# Build outputs
dist/
build/
*.pyc
*.pyo

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Test coverage
coverage/
.coverage
htmlcov/

# Database
*.db
*.sqlite
*.sqlite3

# Temporary files
*.tmp
*.temp
```

## Best Practices Summary

### Do's
✅ Write clear, descriptive commit messages
✅ Commit often with atomic changes
✅ Keep branches short-lived
✅ Review your own code before creating PR
✅ Respond to PR feedback promptly
✅ Keep main branch stable
✅ Use .gitignore properly
✅ Pull before pushing
✅ Test before committing

### Don'ts
❌ Don't commit secrets or credentials
❌ Don't commit build artifacts
❌ Don't force push to shared branches
❌ Don't commit directly to main
❌ Don't create massive PRs
❌ Don't ignore merge conflicts
❌ Don't rewrite public history
❌ Don't commit commented-out code
❌ Don't use vague commit messages

## Troubleshooting

### Common Issues

#### Accidentally Committed to Wrong Branch
```bash
# Move commits to new branch
git branch feature/correct-branch
git reset --hard HEAD~3  # Remove last 3 commits from current branch
git checkout feature/correct-branch
```

#### Need to Update PR After Force Push
```bash
# Update your local branch
git fetch origin
git reset --hard origin/branch-name
```

#### Accidentally Committed Secrets
```bash
# Remove file from history (use with caution)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret/file" \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner (recommended)
bfg --delete-files secret-file.txt
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# IMPORTANT: Rotate any exposed secrets immediately
```

## Success Criteria

Your Git workflow is successful when:
- ✅ Commit history is clean and readable
- ✅ Commit messages are descriptive and follow conventions
- ✅ Branches are properly named and organized
- ✅ Pull requests are clear and reviewable
- ✅ No secrets or sensitive data in repository
- ✅ Conflicts are resolved properly
- ✅ Main branch is always stable
- ✅ Team collaboration is smooth
- ✅ Code review process is effective
- ✅ Git history tells the story of the project
