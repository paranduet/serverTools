import sys, os, re, paramiko
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
# import sys, os, re
from serverLayout import *
from dbConnection import *
from commandExecute import *
# import os
# import paramiko

class LoginDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__()
            self.ui = uic.loadUi('patch_upload.ui', self)
            self.mainLayout = MainWindow()
            self.cmdExecute = CommandExe()
            self.dbCon = DBConfig()
            self.localpath = ""
            self.ui.chooseFile.clicked.connect(self.openFileNamesDialog)
            self.ui.send.clicked.connect(self.fileTransfer)
            self.ui.exit.clicked.connect(self.systemExit)
            self.ui.sendM.clicked.connect(self.fileTransfer)
            self.ui.exitM.clicked.connect(self.systemExit)
            self.ui.cancel.clicked.connect(self.hideWindow)
            self.ui.cancelM.clicked.connect(self.hideWindow)

        def fileTransfer(self):
            target_host = self.ui.hostIP.text()
            pwd = self.ui.hostPass.text()

            ########## Check Deafult User or Not ##########
            if self.ui.checkUsr.isChecked() == True:
                un = "root"
            elif self.ui.checkUsr.isChecked() == False and self.ui.hostUsr.text() =="":
                QMessageBox.question(self, 'Host User Alert', "You didn't entered server User Name", QMessageBox.Ok, QMessageBox.Ok)
            else:
                un = self.ui.hostUsr.text()

            remotepath = self.ui.destPath.text()

            ########## Check Default Port or Changed ############
            if self.ui.vmPort.text():
                target_port = self.ui.vmPort.text()
            else:
                target_port = 22
            
            ######## Initially Destination file list empty ##########
            self.ui.destFile.setText("")

            ####### Set All Local files #####
            localpath = self.localpath

            ########## File transfering process ###########
            for file in localpath:
                result = self.cmdExecute.fileTransfer(target_host, un, pwd, target_port, file, remotepath)
                if result == True:
                    self.ui.destFile.append(remotepath + os.path.basename(file))
                else:
                    QMessageBox.question(self, 'File Transfer Failed', "Transfer failed, please try again", QMessageBox.Ok, QMessageBox.Ok)
            

        def hideWindow(self):
            self.ui.setVisible(False)
            self.mainLayout.show()
        def openFileNameDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print(fileName)
        
        def openFileNamesDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(self,"Select Your Transferable Files", "","All Files (*);;Python Files (*.py)", options=options)
            self.ui.sourceFile.setText("")
            self.localpath = ""
            if files:
                self.localpath = files
                for i in files:
                    self.ui.sourceFile.append(i)
            else:
                QMessageBox.question(self, 'Altert !!!', "You didn't select any file", QMessageBox.Ok, QMessageBox.Ok)
        
        def saveFileDialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
            if fileName:
                print(fileName[0])

        def systemExit(self):
        	sys.exit()

if __name__=="__main__":
    app = QApplication(sys.argv)
    mw = LoginDialog()
    mw.show()
    sys.exit(app.exec_())