import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Toplevel
import os
import shutil
import adbutils
import re
import signal

IP_STORAGE_FILE = ".ips.dat"  # File to store previously used IPs
TIMEOUT_SECONDS = 180  # Timeout for connecting and installing (3 minutes)

def is_valid_ip(ip):
    """Validate the IP address format."""
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(pattern, ip) is not None

def save_ip(ip):
    """Save the IP address to the storage file, keeping only the last 3 IPs."""
    if not os.path.exists(IP_STORAGE_FILE):
        with open(IP_STORAGE_FILE, "w") as f:
            f.write(ip + "\n")
    else:
        with open(IP_STORAGE_FILE, "r") as f:
            ips = f.readlines()
        ips = [line.strip() for line in ips]
        if ip in ips:
            ips.remove(ip)  # Remove the IP if it already exists to avoid duplicates
        ips.append(ip)  # Add the new IP to the end
        ips = ips[-3:]  # Keep only the last 3 IPs
        with open(IP_STORAGE_FILE, "w") as f:
            f.write("\n".join(ips) + "\n")

def load_ips():
    """Load previously used IPs from the storage file."""
    if os.path.exists(IP_STORAGE_FILE):
        with open(IP_STORAGE_FILE, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

def timeout_handler(signum, frame):
    """Handle timeout for long-running operations."""
    raise TimeoutError("The operation timed out after 3 minutes.")

def copy_apks_to_usb(apk_folder, usb_path):
    """Copy APK files to a USB drive."""
    try:
        if not os.path.isdir(usb_path):
            messagebox.showerror("Error", "The specified USB path does not exist. Please check and try again.")
            return

        apk_files = [f for f in os.listdir(apk_folder) if f.endswith(".apk")]
        if not apk_files:
            messagebox.showinfo("No APKs", "No APK files found in the folder.")
            return

        for apk_file in apk_files:
            full_apk_path = os.path.join(apk_folder, apk_file)
            shutil.copy(full_apk_path, usb_path)

        messagebox.showinfo("Success", "All APKs have been successfully copied to the USB drive.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while copying APKs: {e}")

def adb_installer(car_ip, apk_paths, root):
    """Install APKs using ADB."""
    if not is_valid_ip(car_ip):
        messagebox.showerror("Error", "Invalid IP address format. Please try again.")
        return

    save_ip(car_ip)  # Save the IP before attempting to connect

    # Create a new dialog to show the current action
    action_dialog = Toplevel(root)
    action_dialog.title("Installing APKs")
    action_dialog.geometry("400x200")  # Set dialog size
    action_label = tk.Label(action_dialog, text="Starting installation...", font=("Helvetica", 14))
    action_label.pack(pady=40)
    action_dialog.transient(root)
    action_dialog.grab_set()
    root.update()

    try:
        # Set a timeout for the operation
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(TIMEOUT_SECONDS)

        # Step 1: Connect to ADB
        action_label.config(text="Connecting to ADB...")
        root.update()
        adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        adb.connect(car_ip)

        # Step 2: Install each APK
        for apk_path in apk_paths:
            action_label.config(text=f"Installing {os.path.basename(apk_path)}...")
            root.update()
            device = adb.device()
            device.install(apk_path)

        # Cancel the timeout if the operation succeeds
        signal.alarm(0)

        # Step 3: Notify success
        action_label.config(text="All APKs installed successfully!")
        root.update()
        messagebox.showinfo("Success", "All APKs have been installed successfully!")
    except TimeoutError:
        action_label.config(text="Operation timed out.")
        root.update()
        messagebox.showerror("Timeout", "The operation timed out after 3 minutes. Please try again.")
    except adbutils.errors.AdbError as adb_err:
        action_label.config(text="ADB error occurred.")
        root.update()
        messagebox.showerror("ADB Error", f"ADB error occurred: {adb_err}")
    except Exception as e:
        action_label.config(text="An unexpected error occurred.")
        root.update()
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    finally:
        action_dialog.destroy()

def select_usb_path():
    """Open a dialog to select the USB path."""
    return filedialog.askdirectory(title="Select USB Drive")

def select_apk_file():
    """Open a dialog to select an APK file."""
    return filedialog.askopenfilename(title="Select APK File", filetypes=[("APK Files", "*.apk")])

def show_ip_input_dialog(root):
    """Show a dialog with manual IP input and previously used IPs as clickable buttons."""
    ips = load_ips()
    selected_ip = tk.StringVar()

    def select_ip(ip):
        selected_ip.set(ip)
        ip_window.destroy()

    ip_window = Toplevel(root)
    ip_window.title("Enter or Select IP Address")

    tk.Label(ip_window, text="Enter your car's IP address:", font=("Helvetica", 14)).pack(pady=10)
    ip_entry = tk.Entry(ip_window, textvariable=selected_ip, width=30, font=("Helvetica", 12))
    ip_entry.pack(pady=5)

    if ips:
        tk.Label(ip_window, text="Previously used IPs:", font=("Helvetica", 14)).pack(pady=10)
        for ip in ips:
            tk.Button(ip_window, text=ip, command=lambda ip=ip: select_ip(ip), width=20, font=("Helvetica", 12)).pack(pady=5)

    tk.Button(ip_window, text="OK", command=lambda: ip_window.destroy(), width=10, font=("Helvetica", 12)).pack(pady=10)

    ip_window.transient(root)
    ip_window.grab_set()
    root.wait_window(ip_window)

    return selected_ip.get() if selected_ip.get() else ip_entry.get()

def main():
    # Create the main window
    root = tk.Tk()
    root.title("BYD ADB Assistant")
    root.geometry("500x240")  # Set main window size

    # Create the GUI layout
    tk.Label(root, text="Welcome to BYD ADB Assistant", font=("Helvetica", 20)).pack(pady=10)

    # Add a description text under the main label
    tk.Label(root, text="You can use this utility to install APKs on your BYD car using ADB.", font=("Helvetica", 14)).pack(pady=5)

    # Option 1: Copy APKs to USB
    def handle_copy_to_usb():
        usb_path = select_usb_path()
        if usb_path:
            apk_folder = "/Users/kma/bydadb/APKs"
            copy_apks_to_usb(apk_folder, usb_path)

    tk.Button(root, text="Install Required APKs to USB Drive", command=handle_copy_to_usb, width=40, font=("Helvetica", 12)).pack(pady=5)

    # Option 2: Install APKs using ADB
    def handle_adb_install():
        car_ip = show_ip_input_dialog(root)
        if car_ip:
            apk_paths = filedialog.askopenfilenames(
                title="Select APK Files",
                filetypes=[("APK Files", "*.apk")]
            )
            if apk_paths:
                adb_installer(car_ip, apk_paths, root)

    tk.Button(root, text="Install APKs using ADB", command=handle_adb_install, width=40, font=("Helvetica", 12)).pack(pady=5)
    tk.Label(root, text="Made by Khalifa Alahmedi, 2025.", font=("Helvetica", 10)).pack(pady=5)
    tk.Label(root, text="Open-Source and free forever <3", font=("Helvetica", 10)).pack(pady=5)

    # Run the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()