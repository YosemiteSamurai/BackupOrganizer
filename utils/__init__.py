# Design Doc: File Organization Tool

# Please DON'T remove notes for AI

## Requirements

# Notes for AI: Keep it simple and clear.
# If the requirements are abstract, write concrete user stories

# 1. **User Story 1**: As a user, I want to categorize files from a source directory into a destination directory based on file type, so that I can easily find files of a specific type.
# 2. **User Story 2**: As a user, I want to organize files by creation date and last modified date, so that I can manage my files chronologically.
# 3. **User Story 3**: As a user, I want the system to handle name conflicts by renaming files, so that I do not lose any files during the organization process.
# 4. **User Story 4**: As a user, I want to generate HTML and CSV reports of the organized files, so that I can have a record of my file organization.

## Flow Design

# Notes for AI:
# 1. Consider the design patterns of agent, map-reduce, rag, and workflow. Apply them if they fit.
# 2. Present a concise, high-level description of the workflow.

### Applicable Design Pattern:

# 1. **Map-Reduce**: Map files into categories based on type, creation date, and last modified date, then reduce them into organized directories.
# 2. **Agentic File Organizer**:
   # - *Context*: The source directory containing files.
   # - *Action*: Organize files into the destination directory.

### Flow High-level Design:

# 1. **File Discovery Node**: This node scans the source directory and retrieves file metadata.
# 2. **Categorization Node**: This node categorizes files based on type, creation date, and last modified date.
# 3. **Conflict Resolution Node**: This node handles name conflicts by renaming files if necessary.
# 4. **Report Generation Node**: This node generates HTML and CSV reports of the organized files.