import adbutils
import os
import re
import shutil

def is_valid_ip(ip):
    """Validate the IP address format."""
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(pattern, ip) is not None

def copy_apks_to_usb(apk_folder, usb_path):
    """Copy APK files to a USB drive."""
    try:
        if not os.path.isdir(usb_path):
            print("The specified USB path does not exist. Please check and try again.")
            return

        print("Copying APKs to USB drive...")
        for apk_file in os.listdir(apk_folder):
            full_apk_path = os.path.join(apk_folder, apk_file)
            if os.path.isfile(full_apk_path) and apk_file.endswith(".apk"):
                shutil.copy(full_apk_path, usb_path)
                print(f"Copied {apk_file} to {usb_path}")
        print("All APKs have been successfully copied to the USB drive.")
    except Exception as e:
        print(f"An error occurred while copying APKs: {e}")

def adb_installer():
    """Install APKs using ADB."""
    car_ip = input("Enter your car's IP address (e.g., 192.168.1.100): ")
    if not is_valid_ip(car_ip):
        print("Invalid IP address format. Please try again.")
        return

    try:
        # Create an ADB client instance
        adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

        print(f"Connecting to {car_ip}...")
        adb.connect(car_ip)
        print(f"Successfully connected to {car_ip}.")

        apk_path = input("Enter the full path to the APK file you want to install: ")
        if not os.path.isfile(apk_path):
            print("The specified APK file does not exist. Please check the path and try again.")
            return

        print("Installing the APK...")
        # Get the connected device
        device = adb.device()
        device.install(apk_path)
        print("APK installed successfully!")

    except adbutils.errors.AdbError as adb_err:
        print(f"ADB error occurred: {adb_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    print()
    print("                           -----------------------------")
    print("                          |       BYD ADB Assistant      |")
    print("                          |       Made by KMA, 2025      |")
    print("                           -----------------------------")
    print()
    print("Welcome to BYD ADB Assistant! This script lets you install apps on your BYD car easily using Android Debug Bridge.")
    print()

    print("Please select an option:")
    print("1. Install required APKs to USB Drive (necessary to use option 2)")
    print("2. Install APKs using ADB")
    print()

    choice = input("Enter your choice (1 or 2): ")
    if choice == "1":
        apk_folder = "/Users/kma/bydadb/APKs"
        usb_path = input("Enter the path to your USB drive: ")
        copy_apks_to_usb(apk_folder, usb_path)
    elif choice == "2":
        adb_installer()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()