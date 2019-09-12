from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox
import sys
import sys, os, re, paramiko
from subprocess import Popen, PIPE
from pythonping import ping
 
 
class CommandExe(QDialog):
    def __init__(self):
        super().__init__()

    def is_valid_ip(self, ip):
    	m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    	return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

    def sshConnect(self, target_host, un, pwd,cmd):
    	myconn = paramiko.SSHClient()
    	myconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    	target_port = 22

    	if self.is_valid_ip(str(target_host)) :
    		myconn.connect( hostname = target_host , port=22, username = un, password = pwd, look_for_keys=False,
                allow_agent=False )
    		stdin, stdout, stderr = myconn.exec_command(str(cmd))
    		mystr = "%s" %(stdout.read().decode(encoding='UTF-8'))
    		return mystr
    	else:
    		return False
'''
    def checkIP(self, ip):
    	hostname = ip #example
    	# response = os.system("ping -c 3 " + hostname)
    	result = ping(hostname, verbose=True)
    	print(result)
    	if response != "Request timed out.":
    		# print(hostname, 'is up!')
    		return True
    	else:
    		# print(hostname, 'is down!')
    		return False
    		'''