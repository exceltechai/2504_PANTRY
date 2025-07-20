# Compact Command

Pause, take a breath, document current progress in README.md, commit changes to git, sync everything, and compact AI memory for optimal performance.

## Process Overview

This command performs a comprehensive checkpoint operation to:
- Document current project state and progress
- Plan and record next steps
- Commit all changes to version control
- Sync with remote repository
- Build fresh optimized HTML with all changes
- Prepare for memory optimization

## Implementation Steps

### 1. Pause and Reflect (1 minute)
```
- Take a moment to assess current session progress
- Review what has been accomplished
- Identify any incomplete tasks or pending work
- Gather thoughts on project direction
```

### 2. Document Progress in README.md
```
- Locate appropriate section in /root/README.md for progress updates
- Add current session progress under relevant project section
- Document completed tasks, features, or fixes
- Note any important discoveries or decisions made
```

### 3. Plan and Record Next Steps
```
- Identify logical next steps for project continuation
- Document planned approach for upcoming work
- Note any dependencies or blockers to address
- Record technical decisions or architecture choices
```

### 4. Archive Current Version
```bash
# Check if spike-latest.html exists
if [ -f "build/spike-latest.html" ]; then
    # Find the next version number
    NEXT_VERSION=$(ls legacy/html-versions/spike-v*.html 2>/dev/null | sed 's/.*spike-v\([0-9.]*\)\.html/\1/' | sort -V | tail -1 | awk -F. '{print $1"."($2+1)}')
    if [ -z "$NEXT_VERSION" ]; then
        NEXT_VERSION="1.0"
    fi
    
    # Archive current latest
    cp build/spike-latest.html legacy/html-versions/spike-v${NEXT_VERSION}.html
    echo "Archived current version as spike-v${NEXT_VERSION}.html"
fi
```

### 5. Git Operations
```bash
# Check current git status
git status

# Add all changes to staging
git add .

# Create descriptive commit message
git commit -m "Progress checkpoint: [brief summary of work completed]

- [List major accomplishments]
- [Note important changes]
- Next: [Planned next steps]

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Sync with remote repository
git push origin main
```

### 6. Build Fresh HTML
```bash
# Build the latest optimized version with all recent changes
node tools/build-optimized.js

# Verify build succeeded and show token count
if [ -f "build/spike-latest.html" ]; then
    echo "✅ Fresh build completed successfully"
    # Show file size and estimated token count
    ls -lh build/spike-latest.html | awk '{print "File size: " $5}'
else
    echo "❌ Build failed - spike-latest.html not found"
fi
```

### 7. Memory Compact Preparation
```
- Summarize key information for memory retention
- Document important context for future sessions
- Note any critical decisions or patterns established
- Prepare clean slate for continued work
- Run the Compaction process
```

## Progress Documentation Format

Add to README.md under appropriate section:

```markdown
### Recent Progress ([Date])

**Completed:**
- [Major accomplishment 1]
- [Major accomplishment 2]
- [Bug fixes or improvements]

**Current Status:**
- [Overall project state]
- [Any blocking issues]

**Next Steps:**
- [ ] [Planned next action 1]
- [ ] [Planned next action 2]
- [ ] [Future considerations]

**Technical Notes:**
- [Important decisions made]
- [Architecture or design choices]
- [Dependencies or requirements identified]
```

## Success Criteria
- ✅ Progress documented in README.md
- ✅ Next steps clearly planned and recorded  
- ✅ All changes committed to git
- ✅ Repository synced with remote
- ✅ Fresh HTML build completed with all changes
- ✅ Session state properly preserved
- ✅ Ready for memory optimization

## Usage Notes
- Run this command before ending major work sessions
- Helps maintain project continuity across AI sessions
- Ensures no progress is lost during memory management
- Creates clear checkpoint for resuming work later
- Maintains clean git history with meaningful commits