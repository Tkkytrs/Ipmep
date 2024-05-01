import socket
import random
import json
import requests, lolcat
import os
import colorama
import pyfiglet
import threading

c = colorama.Fore
s = colorama.Style

# Printing the banner
print(s.BRIGHT)
os.system(f"echo '{pyfiglet.figlet_format('IPmep', 'slant')}'|lolcat")
os.system("echo '"+ "\n[•] Made By: @TkkytrsP(Telegram)\n[•] Github: @Tkkytrs\n[!] A Project Where You Can Find Unseen Site IPs' |lolcat")
input(c.CYAN + "\n[Press [Enter] To Start]")

# Function to check if an IP address is valid
def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

# Function to query Shodan InternetDB API and get data for a given IP
def query_shodan(ip):
    try:
        xp = {}
        data = {}
        url = f"https://internetdb.shodan.io/{ip}"
        response = requests.get(url)
        if response.status_code == 200:
            xp = response.json()
        else:
            #print(response.json())
            #print (c.GREEN+"["+c.RED+"!"+c.GREEN+"]"+c.WHITE+"Invalid IP")
            return None
        response = requests.get(f"http://ipinfo.io/{ip}/json")
        data = response.json()
        if data.get("readme") == "https://ipinfo.io/missingauth":
                data["readme"] = None
        for name, datas in data.items():
            if datas == "not found":
                data[name] = "null"
        
        return {"data": xp, "data2": data}

            
    except Exception as e:
        print(f"Error querying Shodan InternetDB API: {e}")
        return None

# Function to process IPs
def process_ip():
    global i
    while True:
        #print(i)
        random_ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
        if is_valid_ip(random_ip):
            #print(42,i)
            shodan_data = query_shodan(random_ip)
            if shodan_data:
                #print(99,i)
                result = {"ip": random_ip, "data": shodan_data}
                x = ""
                x += "=" * 40 +"\n"
                for key, value in result["data"]["data"].items():
                    x += f"{key}: {value}\n"
                for key, value in result["data"]["data2"].items():
                    x += f"{key}: {value}\n"
                x += "Total Checked-: "+str(i)+"\n"
                x += "=" * 40
                with open("saved_ips.txt", "a") as file:
                    file.write("\n"+x+"")
                
                os.system(f"echo '{x}' |lolcat")
        i += 1

# Main loop
i = 0
num_threads = 10  # Adjust the number of threads as needed
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=process_ip)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
