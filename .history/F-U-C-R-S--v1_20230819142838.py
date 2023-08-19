import os
import subprocess


def scan_dir(dir_path):
    """
    Scan a directory and return a list of files with specific extensions.
    """
    files = [file for file in os.listdir(dir_path) if file.endswith((".zip", ".sh"))]
    return files


def select_file(files):
    """
    Prompt the user to select a file from a list of files.
    """
    print("Select a file:")
    for i, file in enumerate(files):
        print(f"{i+1}. {file}")
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
        print(f"Error occurred while running command: {command}")


def main():
    print("Please ensure your phone is factory reset and ready for flashing.")
    input("Press Enter to continue...")

    android_dir = "/home/alastor/Android"
    firmware_dir = os.path.join(android_dir, "Firmware")
    recovery_dir = os.path.join(android_dir, "Recovery")
    roms_dir = os.path.join(android_dir, "ROMs")
    gapps_dir = os.path.join(android_dir, "GApps")
    addon_gapps_dir = os.path.join(android_dir, "GApps_Addons")
    jailbreak_dir = os.path.join(android_dir, "Jailbreak")

    # Helper functions for scanning dirs and selecting files

    # List all firmware versions found in the Firmware subdirectory
    firmware_versions = os.listdir(firmware_dir)

    # User selects a firmware version
    print("Available firmware versions:")
    for i, version in enumerate(firmware_versions):
        print(f"{i + 1}. {version}")
    while True:
        try:
            selected_version = int(input("Enter the number of the firmware version you want to flash: "))
            selected_folder = firmware_versions[selected_version - 1]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")

    # Scan categories and select files

    print("Scanning categories...")

    firmware_files = scan_dir(os.path.join(firmware_dir, selected_folder))
    firmware_file = select_file(firmware_files)

    recovery_files = scan_dir(recovery_dir)
    recovery_file = select_file(recovery_files)

    rom_files = scan_dir(roms_dir)
    rom_file = select_file(rom_files)

    gapps_files = scan_dir(gapps_dir)
    gapps_file = select_file(gapps_files)

    addon_gapps_files = scan_dir(addon_gapps_dir)
    addon_gapps_files = [select_file(addon_gapps_files) for _ in range(3)]  # select up to 3

    jailbreak_files = scan_dir(jailbreak_dir)
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
    os.chdir(os.path.join(firmware_dir, selected_folder))

    # Run the firmware flashing commands
    run_command(["fastboot", "--set-active=a"])
    run_command(["fastboot", "flash", "vendor_boot_a", "vendor_boot.img"])
    run_command(["fastboot", "flash", "vendor_boot_b", "vendor_boot.img"])
    run_command(["fastboot", "flash", "boot_a", "boot.img"])
    run_command(["fastboot", "flash", "boot_b", "boot.img"])
    run_command(["fastboot", "flash", "dtbo_a", "dtbo.img"])
    run_command(["fastboot", "flash", "dtbo_b", "dtbo.img"])
    run_command(["fastboot", "flash", "--slot=all", "modem", "modem.img"])
    print("###################################################")
    print("# Rebooting into fastbootd mode #")
    run_command(["fastboot", "reboot", "fastboot"])
    print("###################################################")
    print("#### Start to flash img files in fastbootd mode ###")
    run_command(["fastboot", "flash", "--slot=all", "abl", "abl.img"])
    run_command(["fastboot", "flash", "--slot=all", "aop", "aop.img"])
    run_command(["fastboot", "flash", "--slot=all", "bluetooth", "bluetooth.img"])
    run_command(["fastboot", "flash", "--slot=all", "cpucp", "cpucp.img"])
    run_command(["fastboot", "flash", "--slot=all", "devcfg", "devcfg.img"])
    run_command(["fastboot", "flash", "--slot=all", "dsp", "dsp.img"])
    run_command(["fastboot", "flash", "--slot=all", "engineering_cdt", "engineering_cdt.img"])
    run_command(["fastboot", "flash", "--slot=all", "featenabler", "featenabler.img"])
    run_command(["fastboot", "flash", "--slot=all", "hyp", "hyp.img"])
    run_command(["fastboot", "flash", "--slot=all", "imagefv", "imagefv.img"])
    run_command(["fastboot", "flash", "--slot=all", "keymaster", "keymaster.img"])
    run_command(["fastboot", "flash", "--slot=all", "multiimgoem", "multiimgoem.img"])
    run_command(["fastboot", "flash", "--slot=all", "oplus_sec", "oplus_sec.img"])
    run_command(["fastboot", "flash", "--slot=all", "oplusstanvbk", "oplusstanvbk.img"])
    run_command(["fastboot", "flash", "--slot=all", "qupfw", "qupfw.img"])
    run_command(["fastboot", "flash", "--slot=all", "qweslicstore", "qweslicstore.img"])
    run_command(["fastboot", "flash", "--slot=all", "shrm", "shrm.img"])
    run_command(["fastboot", "flash", "--slot=all", "splash", "splash.img"])
    run_command(["fastboot", "flash", "--slot=all", "tz", "tz.img"])
    run_command(["fastboot", "flash", "--slot=all", "uefisecapp", "uefisecapp.img"])
    run_command(["fastboot", "flash", "--slot=all", "vm-bootsys", "vm-bootsys.img"])
    run_command(["fastboot", "flash", "--slot=all", "xbl_config", "xbl_config.img"])
    run_command(["fastboot", "flash", "--slot=all", "xbl", "xbl.img"])
    run_command(["fastboot", "reboot", "bootloader"])
    run_command(["fastboot", "--set-active=a"])

    print("###################################################")
    print("Firmware flash complete! You should be rebooting into recovery to install your custom ROM")
    run_command(["fastboot", "reboot", "recovery"])

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
    main()
