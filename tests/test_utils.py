# Design Doc: File Organization Tool

> Please DON'T remove notes for AI

## Requirements

> Notes for AI: Keep it simple and clear.
> If the requirements are abstract, write concrete user stories

1. **User Story 1**: As a user, I want to categorize files from a source directory into a destination directory based on file type, so that I can easily find my files.
2. **User Story 2**: As a user, I want to organize files based on their creation date and last modified date, so that I can prioritize my recent files.
3. **User Story 3**: As a user, I want to handle name conflicts by renaming files, so that I do not lose any files during the organization process.
4. **User Story 4**: As a user, I want to generate HTML and CSV reports of the organized files, so that I can keep track of my file organization.

## Flow Design

> Notes for AI:
> 1. Consider the design patterns of agent, map-reduce, rag, and workflow. Apply them if they fit.
> 2. Present a concise, high-level description of the workflow.

### Applicable Design Pattern:

1. **Map-Reduce**: Map files into categories based on type, creation date, and last modified date, then reduce them into organized folders.
2. **Agentic File Organizer**:
   - *Context*: The entire set of files in the source directory.
   - *Action*: Organize files into the destination directory.

### Flow High-level Design:

1. **File Discovery Node**: Scans the source directory and retrieves file metadata.
2. **File Categorization Node**: Categorizes files based on type, creation date, and last modified date.
3. **Conflict Resolution Node**: Handles name conflicts by renaming files.
4. **File Movement Node**: Moves files to the destination directory.
5. **Report Generation Node**: Generates HTML and CSV reports of the organized files.