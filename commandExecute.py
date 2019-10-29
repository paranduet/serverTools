from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox
import sys
import sys, os, re, paramiko, base64
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
    		myconn.close()
    		return mystr
    	else:
    		return False

    def encode(self,key, clear):
    	enc = []
    	for i in range(len(clear)):
    		key_c = key[i % len(key)]
    		enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
    		enc.append(enc_c)
    	return base64.urlsafe_b64encode("".join(enc).encode()).decode()

    def decode(self, key, enc):
    	dec = []
    	enc = base64.urlsafe_b64decode(enc).decode()
    	for i in range(len(enc)):
    		key_c = key[i % len(key)]
    		dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
    		dec.append(dec_c)
    	return "".join(dec)

    def passValidation(self, password):
    	flag = 0
    	while True:   
    		if (len(password)<8): 
    			flag = -1
    			break
    		elif not re.search("[a-z]", password): 
    			flag = -1
    			break
    		elif not re.search("[A-Z]", password): 
    			flag = -1
    			break
    		elif not re.search("[0-9]", password): 
    			flag = -1
    			break
    		elif not re.search("[_@$]", password): 
    			flag = -1
    			break
    		elif re.search("\s", password): 
    			flag = -1
    			break
    		else: 
    			flag = 0
    			return True 
    			break
    	if flag ==-1: 
    		return False

    def fileTransfer(self, target_host, un, pwd, target_port, file , remotepath):
    	localpath = file
    	fname = os.path.basename(file)
    	myconn = paramiko.SSHClient()
    	myconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    	if self.is_valid_ip(str(target_host)) :
    		myconn.connect( hostname = target_host , port = target_port , username = un, password = pwd, look_for_keys=False,
                allow_agent=False )
    		sftp = myconn.open_sftp()
    		sftp.put(localpath, os.path.join(remotepath, fname))
    		sftp.close()
    		myconn.close()
    		return True
    	else:
    		return False
'''    		
		ssh = paramiko.SSHClient() 
		# ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
		ssh.connect(server, username=username, password=password)
		sftp = ssh.open_sftp()
		sftp.put(localpath, remotepath)
		sftp.close()
		ssh.close()

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