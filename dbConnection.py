from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox
import sys
import MySQLdb as mdb
 
 
class DBConfig(QDialog):
    def __init__(self):
        super().__init__()

        self.DBConnection()
 
 
    def DBConnection(self):
        try:
            db = mdb.connect('10.190.42.172', 'vmms', 'vmms123', 'vmms_db')
            return db
 
        except mdb.Error as e:
            return False
    
    def loginForm(self, userName, usrPass):
        if self.DBConnection() != False :
            connectString = self.DBConnection().cursor()
            query = ("SELECT username, isactive FROM user_tbl WHERE username = '%s'" %str(userName) + " AND password = '%s'" %str(usrPass))
            result = connectString.execute(query)
            data = connectString.fetchall()
            # print(data[0][1])
            if result == 1 :
                return True
            else:
                self.closedConnection()
        else:
            QMessageBox.question(self, "Database Info !!!", "Database Connection Established Error", QMessageBox.Ok)
            sys.exit(1)

    def closedConnection(self):
        self.DBConnection().close()

    def userInfo(self):
        if self.DBConnection() != False :
            connectString = self.DBConnection().cursor()
            query = ("SELECT username, last_ip, last_login_date, update_date, isactive FROM user_tbl")
            connectString.execute(query)
            result = connectString.fetchall()
            return result
        else:
            QMessageBox.question(self, "Database Info !!!", "Database Connection Established Error", QMessageBox.Ok)
            sys.exit(1)
    
    def phyServerInfo(self, state):
        if self.DBConnection() != False :
            connectString = self.DBConnection().cursor()
            query = ("SELECT ps_ip, ps_user, ps_pass, ps_os, ps_os_version,ps_tag_name,ps_ram, ps_hdd, isactive, issue_date FROM physical_server_tbl WHERE st_id = '%s'" %str(state))
            connectString.execute(query)
            result = connectString.fetchall()
            return result
        else:
            QMessageBox.question(self, "Database Info !!!", "Database Connection Established Error", QMessageBox.Ok)
            sys.exit(1)

    def appServerIp(self):
        if self.DBConnection() != False :
            connectString = self.DBConnection().cursor()
            query = ("SELECT vm_ip FROM vm_server_tbl")
            connectString.execute(query)
            result = connectString.fetchall()
            return result
        else:
            QMessageBox.question(self, "Database Info !!!", "Database Connection Established Error", QMessageBox.Ok)
            sys.exit(1)

    def appServerInfo(self, vm_ip):
        if self.DBConnection() != False :
            connectString = self.DBConnection().cursor()
            query = ("SELECT ph.ps_ip, vm.vm_name, vm.vm_os_version, vm.vm_is_hardening, vm.vm_tomcat_location, vm.isactive FROM vm_server_tbl AS vm, physical_server_tbl AS ph WHERE vm.vm_ip= '%s' " %str(vm_ip) + " AND ph.ps_id = vm.ps_id")
            connectString.execute(query)
            result = connectString.fetchall()
            # print(result)
            return result
        else:
            QMessageBox.question(self, "Database Info !!!", "Database Connection Established Error", QMessageBox.Ok)
            sys.exit(1)
# App = QApplication(sys.argv)
# window = DBConfig()
# window.loginForm()
# sys.exit(App.exec())