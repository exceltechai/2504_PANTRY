# Download Documentation (/dl)

Downloads comprehensive documentation for specified tools, agents, software, or repositories, with focus on API/SDK information useful for AI development.

## Usage
```
/dl <tool/agent/software/repo-name>
```

## Examples
```
/dl playwright
/dl langchain
/dl openai-api
/dl github.com/microsoft/playwright
```

## Process

1. **Identify Documentation Sources**
   - Official documentation websites
   - GitHub repositories (README, docs/, wiki)
   - API documentation and reference guides
   - SDK documentation and examples
   - Integration guides and tutorials

2. **Fetch Documentation**
   - Use WebFetch to retrieve official docs
   - Use GitHub API or web scraping for repo documentation
   - Download API references, SDK guides, and code examples
   - Collect integration patterns and best practices

3. **Process and Structure**
   - Extract key API/SDK information
   - Organize by topics (getting started, API reference, examples)
   - Format as markdown for AI consumption
   - Include code examples and usage patterns

4. **Save to ai_docs**
   - Create folder: `.claude/ai_docs/{tool_name}/`
   - Save main documentation as `overview.md`
   - Save API reference as `api_reference.md`
   - Save examples as `examples.md`
   - Save integration guides as `integration.md`

5. **Create Summary**
   - Generate AI-friendly summary of capabilities
   - List key APIs, methods, and use cases
   - Note compatibility and requirements
   - Add to main ai_docs index if needed

## Output Structure
```
.claude/ai_docs/{tool_name}/
├── overview.md          # Main documentation overview
├── api_reference.md     # API/SDK reference
├── examples.md          # Code examples and patterns
├── integration.md       # Integration guides
└── quick_reference.md   # AI-optimized quick reference
```

## Notes
- Prioritizes API/SDK documentation over general information
- Focuses on information useful for AI development and integration
- Automatically creates organized folder structure
- Generates AI-friendly summaries and quick references