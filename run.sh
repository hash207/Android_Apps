sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip install -r requirements.txt
# add the following line at the end of your ~/.bashrc file
export PATH=$PATH:~/.local/bin/
