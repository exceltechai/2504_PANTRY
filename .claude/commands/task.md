# Add Task Command

Add a new task entry to the /specs/tasks.md file with structured format.

## Process

1. Check if `/specs/tasks.md` exists, create it if needed with proper header structure
2. Read the current tasks.md file to determine the next task number
3. Parse the user input string to extract task details
4. Add new task entry with the following format:
   - **Task Number**: Auto-incremented (T001, T002, etc.)
   - **Title**: Extracted from user input or prompt for clarification
   - **Progress**: Default to "Not Started"
   - **Description**: Main content from user input
   - **Notes**: Empty initially, can be updated later

## Task Entry Template
```markdown
### T### - [Title]
- **Progress**: Not Started
- **Description**: [User provided description]
- **Notes**: 
- **Created**: [Current date]

---
```

## Usage Examples
- `/task "Implement user authentication system"`
- `/task "Fix bug in payment processing - users getting duplicate charges"`
- `/task "Research AI integration options for chatbot"`

## Implementation Steps
1. Read existing tasks.md or create with template if missing
2. Count existing tasks to determine next number
3. Parse user input for title and description
4. Insert new task in "Active Tasks" section
5. Confirm task added with task number assigned