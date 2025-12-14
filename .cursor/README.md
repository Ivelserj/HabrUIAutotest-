# Cursor Configuration Documentation

Documentation for rules and commands configured for the project in Cursor IDE.

## рџ“‹ Table of Contents

- [Quick Overview](#quick-overview)
- [Rules](#rules)
  - [communication_style.mdc](#1-communication_stylemdc)
  - [context_management.mdc](#2-context_managementmdc)
  - [file_editing.mdc](#3-file_editingmdc)
  - [generate_mockups.mdc](#4-generate_mockupsmdc)
- [Commands](#commands)
  - [amend.md](#1-amendmd)
  - [commit.md](#2-commitmd)
- [File Structure](#file-structure)
- [Configuration and Usage](#configuration-and-usage)
- [Notes](#notes)

---

## Quick Overview

### Rules (`.cursor/rules/`)

All rules are automatically applied (`alwaysApply: true`).

| File | Brief Description |
|------|-------------------|
| `communication_style.mdc` | Communication style - be concise, provide concrete code, treat user as expert |
| `context_management.mdc` | Chat context management - reminder to create new chat when context exceeds 80% |
| `file_editing.mdc` | Handling uneditable files - create temporary files when direct editing is not possible |
| `generate_mockups.mdc` | SVG mockup generation and UI/UX design rules |

### Commands (`.cursor/commands/`)

All commands can be invoked through Command Palette in Cursor.

| File | Brief Description |
|------|-------------------|
| `amend.md` | Apply all changes and perform git amend |
| `commit.md` | Analyze changes and create commit with precise description (in English) |

---

## Rules

All rules are located in `.cursor/rules/` directory and are automatically applied (`alwaysApply: true`).

### 1. `communication_style.mdc`

**Description:** Communication and work style - be concise, provide concrete code, treat user as expert.

**Key Principles:**
- Provide concrete code/explanations, avoid generic phrases
- Be terse (brief and concise)
- Treat user as an expert
- Give answer immediately, details after
- Suggest non-obvious solutions, anticipate needs
- Don't repeat entire code when making edits - only show changed parts
- No moral lectures
- Respect prettier preferences when formatting code
- Split into multiple responses if one isn't enough

**When Applied:** Always (alwaysApply: true)

**Full Content:**
- Emphasizes direct, concrete responses over high-level explanations
- Requires immediate answers with details provided afterward
- Values good arguments over authorities
- Considers new technologies and contrarian ideas
- Allows high levels of speculation when flagged
- No unnecessary code repetition in edits

---

### 2. `context_management.mdc`

**Description:** Chat context management rule - reminder to create new chat when context usage exceeds 80%.

**Key Functions:**
- Automatic tracking of context usage
- At 80% threshold - create session summary
- Suggest creating new chat for continuing work

**Summary Structure:**
- Completed tasks
- Current project state
- Next steps
- Recommendation to create new chat

**When Applied:** Always (alwaysApply: true)

**Full Content:**
- Monitors context usage on every response
- Automatically provides session summary when context > 80%
- Summary should be brief (2-3 paragraphs) but contain key information
- Includes example summary template with:
  - Completed tasks list
  - Current state
  - Next steps
  - Recommendation message

---

### 3. `file_editing.mdc`

**Description:** Rules for handling uneditable files.

**Key Functions:**
- Create temporary files when editing is not possible
- Notify in chat about access problem
- Specify path to temporary file

**Temporary File Naming Convention:**
- Format: `[original-filename]-temp.[extension]`
- Name must reflect intended destination and placement
- For Cursor rules - file must fully comply with requirements (frontmatter, .mdc extension)

**Use Cases:**
- File is read-only or protected
- No access to directory
- Permission denied errors
- File locked by another process

**When Applied:** Always (alwaysApply: true)

**Full Content:**
- Defines 4-step process for handling uneditable files
- Specifies naming convention for temporary files
- Includes rules for creating Cursor Rules files as temporary files
- Provides example scenarios and chat notification templates
- Lists all situations when rule should be applied

---

### 4. `generate_mockups.mdc`

**Description:** Rules for SVG mockup generation and UI/UX design.

**Key Requirements:**

#### SVG File Creation Rules
- Use only ASCII characters in XML comments
- Proper SVG structure with `<defs>` section
- Semantic IDs for all major elements
- Colors in hex format (#RRGGBB)
- Layout guides for Figma with low opacity

#### Error Prevention
- XML syntax validation before saving
- Validate all tags (closing, quotes)
- Test file opens in browser

#### Complete Element Coverage
All page elements must be included:
- Navigation
- Buttons and interactive elements
- Icons (navigation, action, status, decorative)
- Images and logos
- All text (no placeholders)
- Forms and their elements
- Decorative elements

#### Documentation Requirements
- Create README.md for each mockup
- Color palette with hex codes
- Dimensions and spacing
- Typography (fonts, sizes, weights)
- Figma instructions
- Icon and image inventory

#### Quality Checklist
- Technical validation (XML, ASCII, structure)
- Content completeness (all elements included)
- Visual accuracy (colors, typography, spacing)
- Documentation (README, palettes, dimensions)

**When Applied:** Always (alwaysApply: true)

**Full Content:**
- Comprehensive SVG creation guidelines
- Error prevention checklist
- Prompt generation guidelines
- Example prompt template
- Advanced SVG features (gradients, filters, patterns)
- Figma integration details
- README documentation template
- Quality checklist (technical, content, visual, documentation)
- Troubleshooting section
- Browser integration workflow
- Comprehensive page analysis process
- Icons and images handling
- Text content capture requirements
- Mockup accuracy validation process

---

## Commands

All commands are located in `.cursor/commands/` directory and can be invoked through Command Palette in Cursor.

### 1. `amend.md`

**Description:** Applies all changes and performs git amend.

**Command:**
```
Take all the changes and make do git amend
```

**Usage:**
- Invoked through Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
- Automatically applies all changes
- Executes `git commit --amend`

**When to Use:**
- Need to add changes to last commit
- Fix last commit message

**Full Content:**
- Single line command that stages all changes and amends the last commit

---

### 2. `commit.md`

**Description:** Analyzes all changes in current branch and creates commit with precise description of performed actions (in English).

**Command:**
```
Analyze all changes in the current branch and make a commit with a precise description of what I did. (In english)
```

**Usage:**
- Invoked through Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
- Analyzes all changes in current branch
- Automatically generates commit description
- Creates commit with description in English

**When to Use:**
- Need to commit changes with automatic description
- Require precise description of performed actions

**Full Content:**
- Single line command that analyzes changes and creates descriptive commit

---

## File Structure

```
.cursor/
в”њв”Ђв”Ђ README.md (this file)
в”њв”Ђв”Ђ rules/
в”‚   в”њв”Ђв”Ђ communication_style.mdc
в”‚   в”њв”Ђв”Ђ context_management.mdc
в”‚   в”њв”Ђв”Ђ file_editing.mdc
в”‚   в””в”Ђв”Ђ generate_mockups.mdc
в””в”Ђв”Ђ commands/
    в”њв”Ђв”Ђ amend.md
    в””в”Ђв”Ђ commit.md
```

---

## Configuration and Usage

### Rules
- All rules are automatically applied
- Rule files have `.mdc` extension
- Each rule contains frontmatter with `alwaysApply: true`
- Rules can be temporarily disabled by changing `alwaysApply: false` in frontmatter

### Commands
- Commands are invoked through Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
- Command files have `.md` extension
- Commands are executed in context of current project

---

## Notes

- All rules are applied globally for the project
- Rules can be temporarily disabled by changing `alwaysApply: false` in frontmatter
- Commands can be invoked at any time during project work
- To add new rules or commands, create files in corresponding directories
- Temporary files created by `file_editing.mdc` rule follow naming convention: `[original-filename]-temp.[extension]`

---

**Last Updated:** 2024