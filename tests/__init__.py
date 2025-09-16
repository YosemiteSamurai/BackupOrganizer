# Design Doc: File Organization Tool

> Please DON'T remove notes for AI

## Requirements

> Notes for AI: Keep it simple and clear.
> If the requirements are abstract, write concrete user stories

1. As a user, I want to categorize files from a source directory into a destination directory based on file type, so that I can easily find my files.
2. As a user, I want to sort files by creation date and last modified date, ensuring that my most recent files are easily accessible.
3. As a user, I want the system to handle name conflicts by renaming files appropriately, so that I do not lose any files.
4. As a user, I want to generate HTML and CSV reports of the organized files, so that I can keep track of my file organization.

## Flow Design

> Notes for AI:
> 1. Consider the design patterns of agent, map-reduce, rag, and workflow. Apply them if they fit.
> 2. Present a concise, high-level description of the workflow.

### Applicable Design Pattern:

1. **Map** the files from the source directory into categorized chunks based on file type, then **reduce** these chunks into the destination directory.
2. **Agentic file organizer**
   - *Context*: The entire set of files in the source directory
   - *Action*: Organize files into the destination directory

### Flow high-level Design:

1. **File Discovery Node**: This node scans the source directory and retrieves file metadata (type, creation date, last modified date).
2. **File Categorization Node**: This node categorizes files based on the retrieved metadata and prepares them for movement.
3. **File Movement Node**: This node moves files to the destination directory, handling name conflicts.
4. **Report Generation Node**: This node generates HTML and CSV reports of the organized files.