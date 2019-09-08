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
            db = mdb.connect('x.x.x.x', 'x', 'x', 'x')
            return db
 
        except mdb.Error as e:
            return False
    
    def loginForm(self, userName, usrPass):
        if self.DBConnection() != False :
            result = self.DBConnection().cursor()
            query = ("SELECT username, password FROM user_tbl WHERE username = '%s'" %str(userName) + " AND password = '%s'" %str(usrPass))
            # get_password = ("SELECT password FROM users WHERE password = '%s'"%str(usrPass).md5())
            result_output = result.execute(query)
            if result_output == 1 :
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

# App = QApplication(sys.argv)
# window = DBConfig()
# window.loginForm()
# sys.exit(App.exec())
