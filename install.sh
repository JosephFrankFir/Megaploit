#!/bin/bash
clear

BLACK='\e[30m'
RED='\e[31m'
GREEN='\e[92m'
YELLOW='\e[33m'
ORANGE='\e[93m'
BLUE='\e[34m'
PURPLE='\e[35m'
CYAN='\e[36m'
WHITE='\e[37m'
NC='\e[0m'
purpal='\033[35m'


echo -e "${BLUE}                                    https://github.com/JosephFrankFir/Megaploit ${NC}"

echo -e "${RED}                                   [!] This Tool Must Run As ROOT [!]${NC}"
echo ""
echo -e ${CYAN}              "Select Best Option : "
echo ""
echo -e "${WHITE}	       [2] Arch linux"
echo -e "${WHITE}              [1] Kali Linux / Parrot-Os / Any debian based os"
echo -e "${WHITE}              [0] Exit "
echo -n -e " >> "
read choice
INSTALL_DIR="/usr/share/doc/Megaploit"
BIN_DIR="/usr/bin/"
if [ $choice == 1 ]; then 
	echo "[*] Checking Internet Connection .."
	wget -q --tries=10 --timeout=20 --spider https://google.com
	if [[ $? -eq 0 ]]; then
	    echo -e ${BLUE}"[✔] Loading ... "
	    sudo apt-get update && apt-get upgrade 
	    sudo apt-get install python-pip
	    echo "[✔] Checking directories..."
	    if [ -d "$INSTALL_DIR" ]; then
	        echo "[!] A Directory Megaploit Was Found.. Do You Want To Replace It ? [y/n]:" ;
	        read input
	        if [ "$input" = "y" ]; then
	            rm -R "$INSTALL_DIR"
	        else
	            exit
	        fi
	    fi
    		echo "[✔] Installing ...";
		echo "";
		git clone https://github.com/JosephFrankFir/Megaploit.git "$INSTALL_DIR";
		echo "#!/bin/bash
		python3 $INSTALL_DIR/server.py" '${1+"$@"}' > Megaploit;
		sudo chmod +x Megaploit;
		sudo cp Megaploit /usr/bin/;
		rm Megaploit;
		echo ""; 
		echo "[✔] Trying to installing Requirements ..."
		sudo pip3 install imageio
		sudo pip3 install MouseInfo
		sudo pip3 install Pillow
		sudo pip3 install PyAudio
		sudo pip3 install PyAutoGUI
		sudo pip3 install PyGetWindow
		sudo pip3 install PyMsgBox
		sudo pip3 install pyperclip
		sudo pip3 install PyRect
		sudo pip3 install PyScreeze
		sudo pip3 install python3-xlib
		sudo pip3 install PyTweening
		sudo pip3 install termcolor
		sudo pip3 install argparse
		sudo pip3 install mss
		sudo pip3 install opencv-python
		sudo pip3 install pynput
	else 
		echo -e $RED "Please Check Your Internet Connection ..!!"
	fi

    if [ -d "$INSTALL_DIR" ]; then
        echo "";
        echo "[✔] Successfuly Installed !!! ";
        echo "";
        echo "";
        echo -e $ORANGE "		[+]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[+]"
        echo 		"		[+]						      		[+]"
        echo -e $ORANGE  "		[+]     ✔✔✔ Now Just Type In Terminal (Megaploit)              [+]"
        echo 		"		[+]						      		[+]"
        echo -e $ORANGE "		[+]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[+]"
    else
        echo "[✘] Installation Failed !!! [✘]";
        exit
    fi
elif [ $choice -eq 2 ]; then
	echo "[*] Checking Internet Connection .."
	wget -q --tries=10 --timeout=20 --spider https://google.com
	if [[ $? -eq 0 ]]; then
	    echo -e ${BLUE}"[✔] Loading ... "
	    sudo pacman -Syu && sudo pacman -Syyu 
	    sudo pacman -S python-pip
	    echo "[✔] Checking directories..."
	    if [ -d "$INSTALL_DIR" ]; then
	        echo "[!] A Directory Megaploit Was Found.. Do You Want To Replace It ? [y/n]:" ;
	        read input
	        if [ "$input" = "y" ]; then
	            rm -R "$INSTALL_DIR"
	        else
	            exit
	        fi
	    fi
    		echo "[✔] Installing ...";
		echo "";
		git clone https://github.com/JosephFrankFir/Megaploit.git "$INSTALL_DIR";
		echo "#!/bin/bash
		python3 $INSTALL_DIR/server.py" '${1+"$@"}' > Megaploit;
		sudo chmod +x Megaploit;
		sudo cp Megaploit /usr/bin/;
		rm Megaploit;
		echo ""; 
		echo "[✔] Trying to installing Requirements ..."
		sudo pip3 install imageio
		sudo pip3 install MouseInfo
		sudo pip3 install Pillow
		sudo pip3 install PyAudio
		sudo pip3 install PyAutoGUI
		sudo pip3 install PyGetWindow
		sudo pip3 install PyMsgBox
		sudo pip3 install pyperclip
		sudo pip3 install PyRect
		sudo pip3 install PyScreeze
		sudo pip3 install python3-xlib
		sudo pip3 install PyTweening
		sudo pip3 install termcolor
		sudo pip3 install argparse
		sudo pip3 install mss
		sudo pip3 install opencv-python
		sudo pip3 install pynput
	else 
		echo -e $RED "Please Check Your Internet Connection ..!!"
	fi

    if [ -d "$INSTALL_DIR" ]; then
        echo "";
        echo "[✔] Successfuly Installed !!! ";
        echo "";
        echo "";
        echo -e $ORANGE "		[+]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[+]"
        echo 		"		[+]						      		[+]"
        echo -e $ORANGE  "		[+]     ✔✔✔ Now Just Type In Terminal (Megaploit)              [+]"
        echo 		"		[+]						      		[+]"
        echo -e $ORANGE "		[+]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[+]"
    else
        echo "[✘] Installation Failed !!! [✘]";
        exit
    fi

elif [ $choice -eq 0 ];
then
    echo -e $RED "[✘] Thank Y0u !! [✘] "
    exit
else 
    echo -e $RED "[!] Select Valid Option [!]"
fi
