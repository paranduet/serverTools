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
from dbConnection import *


class LoginDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__()
            self.ui = uic.loadUi('login.ui', self)
            self.dbCon = DBConfig()
            self.ui.btnLogin.clicked.connect(self.loginExecute)
            self.ui.btnExit.clicked.connect(self.systemExit)

        def loginExecute(self):
        	userName = self.ui.usrName.text()
        	usrPass = self.ui.usrPass.text()
        	if userName != "" and usrPass != "" and self.dbCon.loginForm(userName, usrPass) == True :
        		self.dbCon.closedConnection()
        		self.mainLayout = MainWindow()
        		# self.mainLayout.ui.usr.setText(userName)
        		self.ui.setVisible(False)
	        	self.mainLayout.show()
        	else:
        		QMessageBox.question(self, 'Login Alert !!!', "User Name OR Password Field is Empty or Invalid", QMessageBox.Ok, QMessageBox.Ok)

        def systemExit(self):
        	sys.exit()

if __name__=="__main__":
    app = QApplication(sys.argv)
    mw = LoginDialog()
    mw.show()
    sys.exit(app.exec_())