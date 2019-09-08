"""
This program for maintaining Remote Server
Author: H.M. Shah Paran Ali
Email: paran.duet@gmail.com
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (QMainWindow, QApplication , QPushButton,
 QToolTip, QDialog, QMessageBox)
import sys, os, re
from serverLayout import *
# from dbConnection import *


class TestEnv(QDialog):
	def __init__(self, parent=None):
		super().__init__()
	
		self.ui = uic.loadUi('test.ui', self)
		self.ui.btnExe.clicked.connect(self.btnExecute)
		self.ui.btnHome.clicked.connect(self.forwardLayout)
		self.ui.btnExit.clicked.connect(self.systemExit)
		# self.ui.homeMenu.triggered.connect(self.forwardLayout)
		# self.ui.hostIp.textChanged.connect(self.hostValidate)
		
	def is_valid_ip(self, ip):
		m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
		return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

	def sshConnect(self, target_host, un, pwd,cmd):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# target_host = self.ui.hostIp.text()
		target_port = 22
		# pwd = self.ui.passwd.text()
		# un = self.ui.usr.text()
		# cmd = self.ui.cmdLine.text()
		if self.is_valid_ip(str(target_host)) :
			ssh.connect( hostname = target_host , username = un, password = pwd )
			stdin, stdout, stderr = ssh.exec_command(str(cmd))
			txt = "%s" %(stdout.read())
			self.ui.display.append(txt)
		else:
			QMessageBox.question(self, 'Wrong IP', "You typed: " + target_host, QMessageBox.Ok, QMessageBox.Ok)
		
		
	def btnExecute(self):
		self.ui.display.setText("")
		target_host = self.ui.hostIp.text()
		# target_port = 22
		pwd = self.ui.passwd.text()
		un = self.ui.usr.text()
		cmd = self.ui.cmdLine.text()
		if target_host == "" or un == "" or pwd == "" or cmd == "":
			QMessageBox.question(self, "Execution Info !!!", "You have missed any of field", QMessageBox.Ok)
		else:
			self.sshConnect(target_host, un, pwd,cmd)

	def forwardLayout(self):
		self.layout = MainWindow()
		self.ui.setVisible(False)
		self.layout.show()
	
	def systemExit(self):
		sys.exit(1)

# if __name__=="__main__":
#     app = QApplication(sys.argv)
#     mw = LoginDialog()
#     mw.show()
#     sys.exit(app.exec_())