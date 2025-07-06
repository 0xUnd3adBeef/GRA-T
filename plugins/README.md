# 🐐 GRA-T Editor

**GRA-T Editor** is a modular, dark-themed IDE built specifically for developing, editing, and testing `.grataddin` plugins for [GRA-T](https://github.com/your-grat-repo). It is designed for red teamers, researchers, and security engineers who want a clean workflow for managing post-exploitation or automation scripts in a structured environment.

---
# Take a look !
![gif](./gif.gif)

---

## ⚙️ Features

- **Dark-themed GUI:** Consistent with lab workflows.
- **Metadata sidebar:** View plugin metadata while editing logic.
- **Metadata editor:** Structured popup to edit `plugin.name`, `plugin.description`, `plugin.lang`, `plugin.ositworkswith`, `plugin.commands`, `plugin.args`.
- **Syntax-agnostic editor:** Supports `python`, `powershell`, `bash`, and `batch` plugin types.
- **Validation:** Check plugin readiness before saving or testing.
- **Embedded terminal:**
  - Supports PowerShell, CMD, and Bash.
  - Run arbitrary commands within the IDE.
  - Show/hide toggle for focus.
- **In-terminal plugin testing:**
  - Soon ?
  - Displays live output with colored styling.
- **Tabbed editing:** Work on multiple plugins in one window.

---

## 🧩 Plugin Development Workflow

| Action | Description |
|--------|-------------|
| **New Plugin** | Create a blank `.grataddin`. |
| **Open Plugin** | Load an existing `.grataddin`. |
| **Save / Save As** | Save the plugin with structured metadata and logic. |
| **Edit Metadata** | Modify plugin metadata cleanly. |
| **Validate Plugin** | Check for missing metadata or empty body. |
| **Test Plugin** | Run the plugin within the IDE using the selected shell. |
| **Toggle Terminal** | Show or hide the embedded terminal for focus. |

---

## 🖥️ Technical Overview

| Field | Detail |
|-------|--------|
| Type | Plugin IDE for `.grataddin` |
| Languages | Python 3 |
| GUI Framework | `tkinter`, `ttk` |
| Terminal Integration | subprocess + threading |
| Platform Support | Windows ✅, Linux ✅ |
| Plugin Types | python, powershell, bash, batch |
| Shells Supported | PowerShell, CMD, Bash |
| Developer | [@MohaCHarr](https://github.com/MohaCHarr) |

---

## 🚀 Quick Start

1️⃣ **Clone:**
```bash
wget "https://raw.github.com/MohaCHarr/GRA-T/plugins/GRA-T Editor.py"
````

2️⃣ **Run:**

```bash
python3 "GRA-T Editor.py"
```

3️⃣ **Start editing or testing your plugins.**

---

## 🎹 Keybinds

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
| `F1`           | Stop it, get some help |

---

## Details

* All plugin tests are local and manual
* It still sucks at testing, that's why i didn't include it

---

## 🚧 Use Case Reminder

**GRA-T Editor is NOT malware.**
It is a development tool for `.grataddin` plugin scripting under controlled, authorized environments.

---

## 📄 License

Licensed under the "Use responsibly and do not misuse" license.

---

### 🐐 **Happy scripting.**
