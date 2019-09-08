from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
import sys
 
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = uic.loadUi('interface.ui', self)
        self.ui.btnShow.clicked.connect(self.btnShow_clicked)
        self.ui.tableWidget.itemDoubleClicked.connect(self.CellClicked)
    def btnShow_clicked(self, source):
        itemList = [('apple','banana','orange'), ('red', 'green', 'blue'), ('cow', 'goat', 'lamb', 'camel')]
        headers = ['One', 'Two', 'Three', 'Four']
        self.ShowOnTable(headers, itemList)
 
    def ShowOnTable(self, headers, source):
        lengths = []
        for item in source:
            lengths.append(len(item))
        highestValue = max(lengths)
        nOfRow = len(source)
        nOfCol = highestValue
        self.ui.tableWidget.setRowCount(nOfRow)
        self.ui.tableWidget.setColumnCount(nOfCol) # adding adding one column for checkbox
        self.ui.tableWidget.setHorizontalHeaderLabels(headers) # making horizontal header lave and adding one more culumn
        for i in range(nOfRow):
            for j in range(len(source[i])):
                self.ui.tableWidget.setItem(i,j, QTableWidgetItem(str(source[i][j]))) # first row then column
    def CellClicked(self, item):
        print('Double clicked on row: %d, column: %d' % (item.row(), item.column()))
        print(item.text())
 
if __name__=="__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())