# Bluepineapple
Repository for the Bluepineapple project development.

Bluepineapple is a project to integrate different bluetooth tools to simulate a Pineapple like device. It has been developed for using on Raspberry Pi 4 with Kali Linux installed.

The script may also work with diffirent kali devices and installations.


# Dependencies
The current project uses the following tools in order to scan, gather information and perform attacks on bluetooth devices:
- Bluelog
- Blueranger
- Sdptool
- Btlesniffer
- Bluesnarfer
- Blueborne POC from https://github.com/ojasookert/CVE-2017-0785 with specific dependencies
- Bluetooth DoS script by jieggil

To install most of these dependencies run the included setup pythong file "bpa-set-up.py"
