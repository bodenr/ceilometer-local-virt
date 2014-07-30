import netifaces
import socket


def hostname():
    return str(socket.gethostname())

def private_ip():
    # SoftLayer private always on eth0
    return netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']

def public_ip():
    # SoftLayer public always on eth1
    return netifaces.ifaddresses('eth1')[netifaces.AF_INET][0]['addr']
