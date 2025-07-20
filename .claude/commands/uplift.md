# Uplift Idea to Project

Converts an existing idea from `0002_INCOMING/IDEAS.md` into a structured project folder with dedicated README.md file.

## Usage

```
/uplift [project_number]
```

Example: `/uplift 2549` (uplifts the Spike power line maintenance idea)

## What this command does

1. **Validates the project number** - Checks that the idea exists in IDEAS.md
2. **Creates project folder** - Creates a new folder named `[NUMBER]_[PROJECT_NAME]` in the root directory
3. **Extracts idea content** - Pulls the complete idea section from IDEAS.md
4. **Creates README.md** - Formats the idea content into a proper project README
5. **Updates idea status** - Marks the idea as "In Development" in IDEAS.md with reference to new folder

## Steps to execute

1. **Read and validate the project number**
   - Use the Read tool to examine `0002_INCOMING/IDEAS.md`
   - Find the specified project number and extract its complete section
   - Validate that the project exists and get its name for folder naming

2. **Create the project folder**
   - Generate folder name: `[NUMBER]_[UPPERCASE_PROJECT_NAME]` 
   - Example: `2549_SPIKE_POWER_LINE_MAINTENANCE` 
   - Use LS tool to verify the root directory location
   - Create the new folder using appropriate tools

3. **Extract and format the idea content**
   - Extract the complete idea section from IDEAS.md (from ### header to next --- separator)
   - Format it appropriately for a project README
   - Add project-specific sections like "Development Status", "Getting Started", etc.

4. **Create the README.md file**
   - Write the formatted content to `[PROJECT_FOLDER]/README.md`
   - Include the original idea content plus project structure sections
   - Add development status, next steps, and related files sections

5. **Update the IDEAS.md file**
   - Change the idea status from "New" to "In Development"
   - Add a reference to the new project folder location
   - Update the "Related Files" section to point to the new folder

## README.md Template Structure

```markdown
# [Project Name]

**Project ID**: [NUMBER]
**Status**: In Development
**Folder**: [FOLDER_NAME]

## Original Idea

[Complete original idea content from IDEAS.md]

## Development Status

- [x] Project folder created
- [ ] Initial planning and requirements
- [ ] Architecture design
- [ ] Implementation planning
- [ ] Development phase
- [ ] Testing and validation
- [ ] Documentation
- [ ] Deployment/Release

## Getting Started

[To be filled during development]

## Architecture

[To be filled during development]

## Related Files

- All project files in this folder: `[FOLDER_NAME]/`
- Original idea: [0002_INCOMING/IDEAS.md](0002_INCOMING/IDEAS.md#[project-id])

## Next Steps

[Extracted from original idea's Next Steps section]
```

## Success criteria

- [ ] New project folder created in root directory with proper naming convention
- [ ] README.md file created with formatted idea content and project structure
- [ ] IDEAS.md updated with "In Development" status and folder reference
- [ ] All content properly formatted and linked

## Error handling

- If project number doesn't exist, provide clear error message and list available project numbers
- If project folder already exists, ask user whether to overwrite or create versioned folder
- If IDEAS.md cannot be read or updated, provide fallback options

## Notes

- Follow existing project folder naming conventions (see other numbered project folders)
- Preserve all original idea content while adding project structure
- Maintain links between IDEAS.md and the new project folder for traceability