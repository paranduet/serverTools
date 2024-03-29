"""

This program for maintaining Remote Server
Author: H.M. Shah Paran Ali
Email: paran.duet@gmail.com
"""

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication , QPushButton, QToolTip, QMessageBox, QTableWidgetItem
import sys, os, re, paramiko
from subprocess import Popen, PIPE
from commandExecute import *
from test import *
from dbConnection import *


class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__()
	
		self.ui = uic.loadUi('serverMainLayout.ui', self)
		# self.ui.btnExe.clicked.connect(self.btnExecute)
		self.ui.phServerInfo.triggered.connect(self.phServerReport)
		self.ui.usrInfo.triggered.connect(self.userInfo)
		self.ui.cmdExeMenu.triggered.connect(self.cmdEnv)
		self.ui.actionServer.triggered.connect(self.appServerInfo)

	def appServerInfo(self):
		self.appServerInfo = AppServerInfo()
		self.appServerInfo.show()
		
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
			self.showOutput(txt)
		else:
			QMessageBox.question(self, 'Wrong IP', "You typed: " + target_host, QMessageBox.Ok, QMessageBox.Ok)

	def showOutput(self, txt):
		self.ui.display.append(txt)
		
	def cmdEnv(self):
		self.cmdEnvLayout = CmdEnv()
		self.ui.setVisible(False)
		self.cmdEnvLayout.show()

	def userInfo(self):
		self.usrReport = UserInfo()
		self.usrReport.show()

	def phServerReport(self):
		self.phReport = PhyServerInfo()
		self.phReport.show()

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

	def hostValidate(self):
		host_ip = self.ui.hostIp.text()
		if self.is_valid_ip(str(host_ip)) == False :
			QMessageBox.question(self, 'Host Ip !!!', "You typed: " + target_host, QMessageBox.Ok, QMessageBox.Ok)

	def systemExit(self):
		sys.exit()


class CmdEnv(QMainWindow):
	def __init__(self, parent=None):
		super().__init__()
	
		self.ui = uic.loadUi('cmdEnvLayout.ui', self)
		self.ui.btnExe.clicked.connect(self.btnExecute)
		self.ui.btnHome.clicked.connect(self.forwardLayout)
		self.ui.btnExit.clicked.connect(self.systemExit)
		self.ui.homeMenu.triggered.connect(self.forwardLayout)
			
	def btnExecute(self):
		self.comExe = CommandExe()
		self.ui.display.setText("")
		target_host = self.ui.hostIp.text()
		# target_port = 22
		pwd = self.ui.passwd.text()
		un = self.ui.usr.text()
		cmd = self.ui.cmdLine.text()
		if target_host == "" or un == "" or pwd == "" or cmd == "":
			QMessageBox.question(self, "Execution Info !!!", "You have missed any of field", QMessageBox.Ok)
		elif self.comExe.sshConnect(target_host, un, pwd,cmd) == False :
			QMessageBox.question(self, 'Wrong IP', "You typed: " + target_host, QMessageBox.Ok, QMessageBox.Ok)
		else:
			self.ui.display.append(self.comExe.sshConnect(target_host, un, pwd,cmd))

	def sshConnect(self, target_host, un, pwd,cmd):
		myconn = paramiko.SSHClient()
		myconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		target_port = 22
		
		self.mainLayout = MainWindow()
		if self.mainLayout.is_valid_ip(str(target_host)) :
			myconn.connect( hostname = target_host , port=22, username = un, password = pwd, look_for_keys=False,
                allow_agent=False )
			stdin, stdout, stderr = myconn.exec_command(str(cmd))
			# mystr = stdout.read().decode(encoding='UTF-8')
			mystr = "%s" %(stdout.read().decode(encoding='UTF-8'))
			self.ui.display.append(mystr)
			
		else:
			QMessageBox.question(self, 'Wrong IP', "You typed: " + target_host, QMessageBox.Ok, QMessageBox.Ok)

	
	def forwardLayout(self):
		self.layout = MainWindow()
		self.ui.setVisible(False)
		self.layout.show()
	
	def systemExit(self):
		sys.exit(1)

class UserInfo(QMainWindow):
	def __init__(self, parent=None):
		super().__init__()

		self.usrInfoUi = uic.loadUi('userInfo.ui', self)
		self.usrInfoUi.usrDetails.clicked.connect(self.btnShow_clicked)
		self.usrInfoUi.closeInfo.clicked.connect(self.exitWindow)
		self.usrInfoUi.tblView.itemDoubleClicked.connect(self.CellClicked)

	def btnShow_clicked(self):
		self.dbCon = DBConfig()
		headers = ['User Name', 'User Ip', 'Last Login Info', 'Info Update Date', 'Status']
		self.usrInfoUi.tblView.setRowCount(0)
		self.usrInfoUi.tblView.setColumnCount(5)
		self.usrInfoUi.tblView.setHorizontalHeaderLabels(headers)

		for rowNumber, rowData in enumerate(self.dbCon.userInfo()):
			self.usrInfoUi.tblView.insertRow(rowNumber)
			for colNumber, colData in enumerate(rowData):
				# if colData == 1 :
				# 	self.usrInfoUi.tblView.setItem(rowNumber,colNumber, QTableWidgetItem("Active"))
				# elif colData == 2 :
				# 	self.usrInfoUi.tblView.setItem(rowNumber,colNumber, QTableWidgetItem("Inactive"))
				self.usrInfoUi.tblView.setItem(rowNumber,colNumber, QTableWidgetItem(str(colData)))
		self.dbCon.close()

	def CellClicked(self, item):
		print('Double clicked on row: %d, column: %d' % (item.row(), item.column()))
		print(item.text())

	def exitWindow(self):
		self.usrInfoUi.hide()

class PhyServerInfo(QDialog):
	def __init__(self, parent=None):
		super().__init__()

		self.PhInfoUi = uic.loadUi('phServerInfo.ui', self)
		self.PhInfoUi.dc.clicked.connect(self.dcReport)
		self.PhInfoUi.hdr.clicked.connect(self.hdrReport)
		self.PhInfoUi.rdr.clicked.connect(self.rdrReport)
		self.PhInfoUi.closeInfo.clicked.connect(self.exitWindow)
		self.PhInfoUi.tblView.itemDoubleClicked.connect(self.CellClicked)

	def dcReport(self):
		state = 1
		self.detailsReport(state)

	def hdrReport(self):
		state = 2
		self.detailsReport(state)

	def rdrReport(self):
		state = 3
		self.detailsReport(state)

	def detailsReport(self, state):
		self.dbCon = DBConfig()
		headers = ['IP Address', 'User', 'Key', 'OS Name', 'OS Version', 'Tag Name', 'RAM', 'HDD', 'Issue Date', 'Status']
		self.PhInfoUi.tblView.setRowCount(0)  #### To Initially Empty Table or removeRow(0)
		self.PhInfoUi.tblView.setColumnCount(len(headers))
		self.PhInfoUi.tblView.setHorizontalHeaderLabels(headers)

		for rowNumber, rowData in enumerate(self.dbCon.phyServerInfo(state)):
			self.PhInfoUi.tblView.insertRow(rowNumber)
			for colNumber, colData in enumerate(rowData):
				# if colData == 1 :
				# 	self.usrInfoUi.tblView.setItem(rowNumber,colNumber, QTableWidgetItem("Active"))
				# elif colData == 2 :
				# 	self.usrInfoUi.tblView.setItem(rowNumber,colNumber, QTableWidgetItem("Inactive"))
				self.PhInfoUi.tblView.setItem(rowNumber,colNumber, QTableWidgetItem(str(colData)))
		self.dbCon.close()

	def CellClicked(self, item):
		print('Double clicked on row: %d, column: %d' % (item.row(), item.column()))
		print(item.text())

	def exitWindow(self):
		self.PhInfoUi.hide()

class AppServerInfo(QMainWindow):
	def __init__(self, parent=None):
		super().__init__()

		self.appServerInfo = uic.loadUi('appServerInfo.ui', self)
		self.dbcon = DBConfig()
		self.appServerInfo.virtualIp.activated.connect(self.loadAppServerIP)
		self.populateIp()

	def loadAppServerIP(self):
		self.comExe = CommandExe()
		currIP = self.appServerInfo.virtualIp.currentText()
		data = self.dbCon.appServerInfo(currIP)
		self.appServerInfo.virIP.setText(currIP)
		if data:
			try:
				self.appServerInfo.PhIP.setText(data[0][0])
				self.appServerInfo.vmName.setText(data[0][1])
				self.appServerInfo.osVersion.setText(data[0][2])
				self.appServerInfo.hardenStatus.setText(data[0][3])
				self.appServerInfo.appLocation.setText(data[0][4])
				if data[0][5] == 1:
					self.appServerInfo.serverStatus.setText("Active")
				elif data[0][5] == 2 :
					self.appServerInfo.serverStatus.setText("Inactive")
				else:
					self.appServerInfo.serverStatus.setText("Not Updated")

				###########Check Running Application and Tomcat ########
				if not data[0][4] :
					cmd ="ls -l /opt/tomcat/webapps/ |  awk '{print $9}'"
					self.appServerInfo.appList.setText(self.comExe.sshConnect(currIP,"root","!bbl@2Q17",cmd))
					
				else:
					cmd = "service tomcat status | grep 'running'"
					tomStatus = self.comExe.sshConnect(currIP,"root","!bbl@2Q17",cmd)
					if tomStatus == "" :
						self.appServerInfo.tomcatStatus.setText("Not Running")
					else:
						self.appServerInfo.tomcatStatus.setText("Running")

					txt = data[0][4]
					cmd = "ls -l '%s'" %str(txt) + " |  awk '{print $9}'"
					self.appServerInfo.appList.setText(self.comExe.sshConnect(currIP,"root","!bbl@2Q17",cmd))
			except:
				QMessageBox.question(self, 'Exception Info', "Out of Index", QMessageBox.Ok, QMessageBox.Ok)


	def populateIp(self):
		# data = self.dbCon.appServerIp()
		self.dbCon = DBConfig()
		for ip in self.dbCon.appServerIp() :
			self.appServerInfo.virtualIp.addItem(ip[0])

'''
if __name__=="__main__":
    app = QApplication(sys.argv)
    mw = UserInfo()
    mw.show()
    sys.exit(app.exec_())
    '''