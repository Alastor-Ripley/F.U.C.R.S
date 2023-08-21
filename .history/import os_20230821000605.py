import os
import requests
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

def get_os():
    """
    Get the operating system name.
    """
    return platform.system()

def get_android_dir(os_name):
    """
    Get the Android directory based on the operating system.
    """
    if os_name == "Windows":
        return "C:\\Android"
    elif os_name == "Linux":
        return "/home/alastor/Android"
    elif os_name == "Darwin":
        return "/Users/alastor/Android"
    else:
        return None

def get_tool_dir(os_name):
    """
    Get the directory for tools like adb and fastboot based on the operating system.
    """
    if os_name == "Windows":
        return "C:\\Android\\Tools"
    elif os_name == "Linux":
        return "/home/alastor/Android/Tools"
    elif os_name == "Darwin":
        return "/Users/alastor/Android/Tools"
    else:
        return None

def scan_dir(dir_path, extensions):
    """
    Scan a directory and return a list of files with specific extensions.
    """
    try:
        with os.scandir(dir_path) as entries:
            files = [entry.name for entry in entries if entry.is_file() and entry.name.endswith(extensions)]
        return files
    except Exception:
        print("Error occurred while scanning directory.")
        return []

def select_file(files):
    """
    Prompt the user to select a file from a list of files.
    """
    print("Select a file:")
    for i, file in enumerate(files):
        print(f"i + 1. file")
    while True:
        try:
            selection = int(input("> "))
            selected_file = files[selection - 1]
            return selected_file
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")

def run_command(command):
    """
    Run a command and handle any exceptions.
    """
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"Error occurred while running command: command")

def validate_selection(min_value, max_value):
    """
    Validate user input for selecting files.
    """
    while True:
        try:
            selection = int(input("> "))
            if min_value <= selection <= max_value:
                return selection
            else:
                print("Invalid selection. Please try again.")
        except Exception:
            print("Invalid selection. Please try again.")

def scan_and_select_files(directory, extensions):
    """
    Scan a directory and select a file from the scanned files.
    """
    files = scan_dir(directory, extensions)
    selected_file = select_file(files)
    return selected_file

def get_latest_version(url):
    """
    Get the latest version number from a URL.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        version = soup.find("span", class_="version").text.strip()
        return version
    except Exception:
        print("Error occurred while getting the latest version.")
        return None

def download_file(url, save_path):
    """
    Download a file from a URL and save it to the specified path.
    """
    try:
        response = requests.get(url)
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded: {save_path}")
    except Exception:
        print("Error occurred while downloading the file.")

def main():
    os_name = get_os()
    android_dir = get_android_dir(os_name)
    tool_dir = get_tool_dir(os_name)

    # Adjust the directories accordingly based on the operating system

    directories = 
        "firmware": os.path.join(android_dir, "Firmware"),
        "recovery": os.path.join(android_dir, "Recovery"),
        "roms": os.path.join(android_dir, "ROMs"),
        "gapps": os.path.join(android_dir, "GApps"),
        "addon_gapps": os.path.join(android_dir, "GApps_Addons"),
        "jailbreak": os.path.join(android_dir, "Jailbreak"),
        "tools": tool_dir
    

    # Rest of the code...

    # Helper function for scanning directories and selecting files
    def scan_and_select(directory, extensions):
        return scan_and_select_files(directories[directory], extensions)

    # List all firmware versions found in the Firmware subdirectory
    firmware_versions = os.listdir(directories["firmware"])

    # User selects a firmware version
    print("Available firmware versions:")
    for i, version in enumerate(firmware_versions):
        print(f"i + 1. version")
    selected_version = validate_selection(1, len(firmware_versions))
    selected_folder = firmware_versions[selected_version - 1]

    # Scan categories and select files
    print("Scanning categories...")

    with ThreadPoolExecutor() as executor:
        firmware_files = executor.submit(scan_and_select, "firmware", (".img"))
        recovery_files = executor.submit(scan_and_select, "recovery", (".zip"))
        rom_files = executor.submit(scan_and_select, "roms", (".zip"))
        gapps_files = executor.submit(scan_and_select, "gapps", (".zip"))
        addon_gapps_files = [scan_and_select("addon_gapps", (".zip")) for _ in range(5)]  # select up to 5
        jailbreak_files = executor.submit(scan_and_select, "jailbreak", (".zip", ".apk"))

        firmware_files = firmware_files.result()
        recovery_files = recovery_files.result()
        rom_files = rom_files.result()
        gapps_files = gapps_files.result()
        addon_gapps_files = [addon_gapps_files[i].result() for i in range(5)]
        jailbreak_files = jailbreak_files.result()

    # Placeholder URLs for the ROMs
    rom_urls = {
        "crDroid": "https://sourceforge.net/projects/crdroid/files/lemonadep/9.x/",
        "Evolution X": "https://sourceforge.net/projects/evolution-x/files/lemonadep/13/",
        "ROM 3": "URL 3",
        "ROM 4": "URL 4",
        "ROM 5": "URL 5",
        "ROM 6": "URL 6"
    }

    # Get the latest version for each ROM
    rom_versions = {}
    for rom, url in rom_urls.items():
        latest_version = get_latest_version(url)
        rom_versions

    firmware_file = select_file(firmware_files)
    recovery_file = select_file(recovery_files)
    rom_file = select_file(rom_files)
    gapps_file = select_file(gapps_files)
    jailbreak_file = select_file(jailbreak_files)

    # Confirm selections
    print("Your selections:")
    print(f"Firmware: {firmware_file}")
    print(f"Recovery: {recovery_file}")
    print(f"ROM: {rom_file}")
    print(f"GApps: {gapps_file}")
    print(f"Addon GApps: {addon_gapps_files}")
    print(f"Jailbreak: {jailbreak_file}")

    input("Press Enter to confirm and begin flashing...")

    # Flash selections
    print("Firmware Flashing Section")

    # Change directory to the selected firmware folder
    os.chdir(os.path.join(directories["firmware"], selected_folder))


    # Run the firmware flashing commands
    commands = [
        ["fastboot", "--set-active=a"],
        ["fastboot", "flash", "vendor_boot_a", "vendor_boot.img"],
        ["fastboot", "flash", "vendor_boot_b", "vendor_boot.img"],
        ["fastboot", "flash", "boot_a", "boot.img"],
        ["fastboot", "flash", "boot_b", "boot.img"],
        ["fastboot", "flash", "dtbo_a", "dtbo.img"],
        ["fastboot", "flash", "dtbo_b", "dtbo.img"],
        ["fastboot", "flash", "--slot=all", "modem", "modem.img"],
        ["fastboot", "reboot", "fastboot"],
        ["fastboot", "flash", "--slot=all", "abl", "abl.img"],
        ["fastboot", "flash", "--slot=all", "aop", "aop.img"],
        ["fastboot", "flash", "--slot=all", "bluetooth", "bluetooth.img"],
        ["fastboot", "flash", "--slot=all", "cpucp", "cpucp.img"],
        ["fastboot", "flash", "--slot=all", "devcfg", "devcfg.img"],
        ["fastboot", "flash", "--slot=all", "dsp", "dsp.img"],
        ["fastboot", "flash", "--slot=all", "engineering_cdt", "engineering_cdt.img"],
        ["fastboot", "flash", "--slot=all", "featenabler", "featenabler.img"],
        ["fastboot", "flash", "--slot=all", "hyp", "hyp.img"],
        ["fastboot", "flash", "--slot=all", "imagefv", "imagefv.img"],
        ["fastboot", "flash", "--slot=all", "keymaster", "keymaster.img"],
        ["fastboot", "flash", "--slot=all", "multiimgoem", "multiimgoem.img"],
        ["fastboot", "flash", "--slot=all", "oplus_sec", "oplus_sec.img"],
        ["fastboot", "flash", "--slot=all", "oplusstanvbk", "oplusstanvbk.img"],
        ["fastboot", "flash", "--slot=all", "qupfw", "qupfw.img"],
        ["fastboot", "flash", "--slot=all", "qweslicstore", "qweslicstore.img"],
        ["fastboot", "flash", "--slot=all", "shrm", "shrm.img"],
        ["fastboot", "flash", "--slot=all", "splash", "splash.img"],
        ["fastboot", "flash", "--slot=all", "tz", "tz.img"],
        ["fastboot", "flash", "--slot=all", "uefisecapp", "uefisecapp.img"],
        ["fastboot", "flash", "--slot=all", "vm-bootsys", "vm-bootsys.img"],
        ["fastboot", "flash", "--slot=all", "xbl_config", "xbl_config.img"],
        ["fastboot", "flash", "--slot=all", "xbl", "xbl.img"],
        ["fastboot", "reboot", "bootloader"],
        ["fastboot", "--set-active=a"]
    ]

    for command in commands:
        run_command(command)

    print("Firmware flash complete! You should be rebooting into recovery to install your custom ROM")

    # Recovery Flashing Section
    print("Recovery Flashing Section")
    print("TWRP, flashing this custom recovery will make things easier down the line, so enable ADB, apply update, and press enter to start!")
    input("Press Enter to confirm and begin flashing...")
    run_command(["adb", "sideload", os.path.join(recovery_dir, recovery_file)])
    run_command(["adb", "reboot", "bootloader"])
    run_command(["fastboot", "--set-active=a"])
    run_command(["fastboot", "reboot", "recovery"])

    # Rom Slot A Flashing Section
    print("Rom Slot A Flashing Section")
    print("First we'll flash the rom to slot A, so enable ADB, apply update, and press enter to start!")
    input("Press Enter to confirm and begin flashing...")
    run_command(["adb", "reboot", "recovery"])
    run_command(["adb", "sideload", os.path.join(roms_dir, rom_file)])
    run_command(["adb", "reboot", "bootloader"])
    run_command(["fastboot", "--set-active=b"])
    run_command(["fastboot", "reboot", "recovery"])

    # Rom Slot B Flashing Section
    print("Rom Slot B Flashing Section")
    print("Now for the B side, so enable ADB, apply update, and press enter to start!")
    input("Press Enter to confirm and begin flashing...")
    run_command(["adb", "sideload", os.path.join(roms_dir, rom_file)])
    run_command(["adb", "reboot", "bootloader"])
    run_command(["fastboot", "--set-active=a"])
    run_command(["fastboot", "reboot", "recovery"])

    # GApps Flashing Section
    if gapps_file:
        print("GApps Flashing Section")
        print("Ahh so the rom you choose doesn't include GApps? No problem, your choice will be flashed here, so enable ADB, apply update, and press enter to start!")
        input("Press Enter to confirm and begin flashing...")
        run_command(["adb", "sideload", os.path.join(gapps_dir, gapps_file)])
        run_command(["adb", "reboot", "bootloader"])
        run_command(["fastboot", "--set-active=a"])
        run_command(["fastboot", "reboot", "recovery"])

    # Addon_GApps Flashing Section
    print("Addon_GApps Flashing Section")
    print("Addon GApps are a great way to fine-tune what apps are on your device from the start, so enable ADB, apply update, and press enter to start!")
    input("Press Enter to confirm and begin flashing...")
    for addon_gapps_file in addon_gapps_files:
        run_command(["adb", "sideload", os.path.join(addon_gapps_dir, addon_gapps_file)])
        run_command(["adb", "reboot", "bootloader"])
        run_command(["fastboot", "--set-active=a"])
        run_command(["fastboot", "reboot", "recovery"])

    # Jailbreak Flashing Section
    print("Jailbreak Flashing Section")
    print("Take full control of your android device with Root privileges, aka jailbreaking, so enable ADB, apply update, and press enter to start!")
    input("Press Enter to confirm and begin flashing...")
    run_command(["adb", "sideload", os.path.join(jailbreak_dir, jailbreak_file)])
    run_command(["adb", "reboot"])

    print("Flashing complete! Your phone should now boot into your new OS. If it doesn't, unbrick and try again.")

if __name__ == "__main__":
