# BYD ADB Assistant
This is a helpful GUI utility to sideload apps onto a BYD car using Android Debug Bridge (ADB).

## Installation
You can clone this repository (git clone https://github.com/alahmedi/bydadb) then run either the CLI Script (bydadb.py) or the GUI Script (bydadb_gui.py) easily.

## Usage
### Installing required APKs
You must use this option before using ADB installation. This option downloads the required APKs to a drive of your choosing, which you must plug into the car and install the required APKs from there. The USB must be formatted as FAT32. 
### Installing APKs with ADB
You can enter in the IP of the car (it is found in Settings > Wi-Fi > tap the info button of your connected Wi-Fi network > IP Address), then you select the APKs you want to install.

## Requirements
You must install Python, Android Platform Tools (includes ADB), and the "adbutils" Python library (allows the script to interact with ADB).

### Python

* Windows
  You can get it from the Microsoft store.

* macOS/Linux
  It comes pre-installed, you can skip this.

### Android Platform Tools

* Windows
  You can use the APT installer, provided by https://github.com/cli-stuff/platform-tools-installer-windows
  Run this command in PowerShell: powershell -ExecutionPolicy Bypass -c "irm cutt.ly/platform-tools | iex"

* macOS
  You can use HomeBrew to install APT.
  Install HomeBrew if you don't already have it, run this in Terminal: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  Then, run this command: brew install android-platform-tools

* Linux
  It depends on your distro and your package manager. Please check and install.

### adbutils Python library 
  Run this in PowerShell/Terminal: pip install adbutils
  (If you're on Windows, you must already have Python installed.)

## todo (ignore this) 
* write full guide
* make it more user friendly
