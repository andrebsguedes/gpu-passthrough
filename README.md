# gpu-passthrough

Install a Ubuntu 16.04 server on the host machine and unpack the following file in the user home folder

https://drive.google.com/file/d/0B9nWtptYH6uNOFM4WTZNVGdZMnM/view?usp=sharing

Enter the passthrough folder and run the vfio-config.sh with root privileges

Wait for the system to reboot and change the vmubuntu.sh with root privileges to add the keyboard and mouse ids from the lsusb output and run the file to start the virtual machine.

The virtual machine filesystem was shrank to reduce the folder size, it is recomended to increase the filesystem using

qemu-img resize userver.img +10G

and inside the vm increase the partition size.

Clone the git repository inside the vm, enter the folder and activate the python virtual environment by running

cd crispy-horse
sudo apt install python-pip
sudo pip install virtualenv
./setup.sh
source .env/bin/activate

After the setup run the server to start the web interface

gunicorn crispy-horse:app -b 0.0.0.0 -w 4
