import subprocess
import netifaces
import requests
import psutil
import socket
import json
import time
import os

def get_background_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            process_info = proc.info
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def sys_background ():
    background_processes = get_background_processes()
    data = {
        'coputer_uid': coputer_uid,
        'background_processes': background_processes,
        'time': time.time()
    }
    requests.post(f'http://{server_ip}:{server_port}/background', json=data)

def change_ip (turn_ip):
    gateways = netifaces.gateways()
    default_gateway_info = gateways['default'][netifaces.AF_INET]
    gateway_ip = default_gateway_info[0]
    interface_name = netifaces.interfaces()
    new_ip = turn_ip
    subnet_mask = "255.255.255.0"
    gateway = gateway_ip
    subprocess.run(['netsh', 'interface', 'ip', 'set', 'address', interface_name, 'static', new_ip, subnet_mask, gateway], check=True)

data_json_path = os.path.join(os.path.dirname(__file__), 'data.json')
with open(data_json_path, 'r', encoding='utf-8') as f:
    data_json = json.load(f)
server_ip = data_json['server_ip']
server_port = data_json['server_port']
coputer_uid = data_json['coputer_uid']
coputer_name = socket.gethostname()
coputer_ip = socket.gethostbyname(coputer_name)
first_data = {
    'coputer_uid': coputer_uid,
    'coputer_name': coputer_name,
    'coputer_ip': coputer_ip,
    'time': time.time()
}
requests.post(f'http://{server_ip}:{server_port}/fist', json=first_data)

def work (json):
    code = json['code']
    if code == 'sys_background':
        sys_background()
    elif code == 'turn_ip':
        turn_ip = json['turn_ip']
        change_ip(turn_ip)

def live ():
    coputer_name = socket.gethostname()
    coputer_ip = socket.gethostbyname(coputer_name)
    data = {
        'coputer_uid': coputer_uid,
        'coputer_name': coputer_name,
        'coputer_ip': coputer_ip,
        'time': time.time()
    }
    msg = requests.post(f'http://{server_ip}:{server_port}/live', json=data)
    msg_json = json.loads(msg.text)
    

