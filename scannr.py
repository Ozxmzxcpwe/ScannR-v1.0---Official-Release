import socket
import requests
import re
import os
from colorama import Fore, init

init(autoreset=True)



def logo():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(Fore.RED + """
 ██████  ▄████▄   ▄▄▄       ███▄    █  ███▄    █  ██▀███
▒██    ▒ ▒██▀ ▀█  ▒████▄     ██ ▀█   █  ██ ▀█   █ ▓██ ▒ ██▒
░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██  ▀█ ██▒▓██  ▀█ ██▒▓██ ░▄█ ▒
  ▒   ██▒▒▓▓▄ ▄██▒░██▄▄▄▄██ ▓██▒  ▐▌██▒▓██▒  ▐▌██▒▒██▀▀█▄
▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒▒██░   ▓██░▒██░   ▓██░░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░   ▒ ▒ ░ ▒▓ ░▒▓░
░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░░ ░░   ░ ▒░░ ░░   ░ ▒░  ░▒ ░ ▒░
░  ░  ░  ░          ░   ▒      ░   ░ ░    ░   ░ ░   ░░   ░
      ░  ░ ░            ░  ░         ░          ░    ░
         ░
""")




def check_link(url):
    print(Fore.YELLOW + f"\n[~] URL: {url}")

    risk = 0
    reasons = []

    
    suspicious_domains = [
        "bit.ly", "tinyurl", "t.co", "cutt.ly",
        "2no.co", "grabify", "iplogger", "shorte.st"
    ]

    for d in suspicious_domains:
        if d in url:
            risk += 3
            reasons.append(f"TREMENDO IPLOGGER: {d}")

    
    if "@" in url:
        risk += 1
        reasons.append("URL contains @ (phishing pattern)")

    if len(url) > 75:
        risk += 1
        reasons.append("URL unusually long")

    if any(x in url.lower() for x in ["login", "verify", "secure", "update"]):
        risk += 1
        reasons.append("phishing keywords detected")

    # RESULTADO
    if risk >= 4:
        print(Fore.RED + "\n[!!!] LIMPIO!")
        print(Fore.RED + "RISK SCORE: 90-100")

    elif risk >= 2:
        print(Fore.YELLOW + "\n[!] LINK SOSPECHOSO")
        print(Fore.YELLOW + f"RISK SCORE: {risk * 20}/100")

    else:
        print(Fore.GREEN + "\n[✓] LOW RISK LINK")
        print(Fore.GREEN + f"RISK SCORE: {risk * 10}/100")

    
    if reasons:
        print(Fore.WHITE + "\n--- DETECTION LOG ---")
        for r in reasons:
            print(Fore.RED + f"[+] {r}")



def scan_ports(target):

    print(Fore.YELLOW + f"\n[~] SCANNING: {target}")

    try:
        ip = socket.gethostbyname(target)
    except:
        print(Fore.RED + "[!] INVALID TARGET")
        return

    ports = [21,22,23,25,53,80,110,443,445,3306,3389,8080]

    for port in ports:
        try:
            s = socket.socket()
            s.settimeout(0.3)

            if s.connect_ex((ip, port)) == 0:
                print(Fore.GREEN + f"[OPEN] {port}")

            s.close()

        except:
            pass



def geo_ip(ip):

    print(Fore.CYAN + f"\n[~] GEO: {ip}")

    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()

        if res["status"] == "success":
            print(Fore.WHITE + "\n--- INFO ---")
            print("Country:", res["country"])
            print("City   :", res["city"])
            print("ISP    :", res["isp"])
            print("Lat/Lon:", res["lat"], res["lon"])
            print("------------\n")

        else:
            print(Fore.RED + "[!] NOT FOUND")

    except:
        print(Fore.RED + "[!] ERROR")



def menu():

    while True:
        print("""
[1] Check Link
[2] Port Scan
[3] Geo IP
[0] Exit
""")

        op = input("SCANNR > ")

        if op == "1":
            check_link(input("URL: "))

        elif op == "2":
            scan_ports(input("TARGET: "))

        elif op == "3":
            geo_ip(input("IP: "))

        elif op == "0":
            break

        else:
            print("INVALID")



if __name__ == "__main__":
    logo()
    menu()