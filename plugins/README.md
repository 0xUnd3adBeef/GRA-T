# **GRA-T Editor**

*A purpose-built plugin editor for `.grataddin` plugins for GRA-T*

---

# Take a look !
![gif](./screen1_recording.gif)


## Overview

**GRA-T Editor** is a modular, dark-themed integrated development environment designed for creating, editing, and validating `.grataddin` plugins used in [GRA-T](https://github.com/0xUnd3adBeef/GRA-T).


---

## Key Features

* **Dark-themed interface** for comfortable extended use in lab or red team settings.
* **Metadata sidebar** with live display of plugin fields (`name`, `description`, `lang`, `ositworkswith`, `commands`, `args`).
* **Metadata editor** via structured dialog for clean updates.
* **Language-agnostic script editing**  supports Python, PowerShell, Bash, and Batch.
* **Plugin validation** to check completeness before saving or testing.
* **Embedded terminal** (PowerShell, CMD, Bash) with show/hide toggle.
* **Tabbed editing** for multiple plugins in one session.
* **Plugin testing** from within the IDE (planned enhancements for live colored output).

---

## Plugin Development Workflow

| Action              | Purpose                                                           |
| ------------------- | ----------------------------------------------------------------- |
| **New Plugin**      | Create a new `.grataddin` template with empty metadata and logic. |
| **Open Plugin**     | Load an existing plugin file for review or changes.               |
| **Edit Metadata**   | Structured interface to modify metadata fields.                   |
| **Save / Save As**  | Write validated plugin files to disk.                             |
| **Validate Plugin** | Check for missing or incomplete metadata and empty body.          |
| **Test Plugin**     | Execute in selected shell for local testing (lab use only).       |
| **Toggle Terminal** | Show/hide embedded shell to focus on editing.                     |

---

## Technical Overview

| Field                  | Detail                                     |
| ---------------------- | ------------------------------------------ |
| Type                   | `.grataddin` Plugin IDE                    |
| Language               | Python 3                                   |
| GUI Framework          | `tkinter`, `ttk`                           |
| Terminal Integration   | `subprocess` + `threading`                 |
| Supported Platforms    | Windows ✅ / Linux ✅                        |
| Supported Plugin Types | Python, PowerShell, Bash, Batch            |
| Supported Shells       | PowerShell, CMD, Bash                      |
| Developer              | [@0xUnd3adBeef](https://github.com/0xUnd3adBeef) |

---

## Quick Start

1. **Clone or download**:

```bash
wget "https://raw.github.com/MohaCHarr/GRA-T/plugins/GRA-T Editor.py"
```

2. **Run**:

```bash
python3 "GRA-T Editor.py"
```

3. Start creating or editing plugins in a structured, metadata-driven environment.

---

## Keyboard Shortcuts

| Keybind        | Action          |
| -------------- | --------------- |
| `Ctrl+N`       | New Plugin      |
| `Ctrl+O`       | Open Plugin     |
| `Ctrl+S`       | Save            |
| `Ctrl+Shift+S` | Save As         |
| `Ctrl+W`       | Close Tab       |
| `Ctrl+Q`       | Quit            |
| `Ctrl+E`       | Edit Metadata   |
| `Ctrl+V`       | Validate Plugin |
| `Ctrl+T`       | Test Plugin     |
| `F1`           | Help/About      |

---

## Use Case

Making plugins for GRA-T and feel cool doing it.

---

## License

Licensed under a “Responsible Use” policy. You are solely responsible for compliance with applicable laws and agreements.

---

## Contact

[GitHub](https://github.com/0xUnd3adBeef) | Discord : @mohacharr

---

### Happy scripting.
