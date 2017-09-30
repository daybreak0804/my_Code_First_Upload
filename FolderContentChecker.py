# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 18:45:46 2017

@author: user1
"""

import sys
import os
import pandas as pd

# for PyQt 
from PyQt4 import uic, QtGui
from PyQt4.QtGui import QMainWindow, QApplication
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QFileDialog


form_class = uic.loadUiType(".\\FolderContentChecker.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.setupUi(self)

        # table widget init code
        self.tableWidget_FolderContentChecker.setColumnCount(50)
        self.tableWidget_FolderContentChecker.setRowCount(50)
        
        # push buttons init code
        self.pushButton_excelFileDialog.clicked.connect(self.excelFileDialog)
        self.pushButton_excelFolderDialog.clicked.connect(self.excelFolderDialog)
        self.pushButton_checkClipBoard.clicked.connect(self.checkClipBoard)
        self.pushButton_checkSelectedItemsInFolder.clicked.connect(self.checkSelectedItemsInFolder)
        
        # line edit init code
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.lineEdit_currentFolder.setText(dir_path)
        
        # set the shortcut ctrl+v for paste
        QtGui.QShortcut(QtGui.QKeySequence('Ctrl+v'),self).activated.connect(self.checkClipBoard)
        
    def checkFolder(self, filename, i_row, i_col):
        #print "filename is 1: " + filename
        tempStr = str("")
        tempStr = self.lineEdit_currentFolder.text()
        dirpath = str("")
        for (dirpath, dirnames, filenames) in os.walk(tempStr):
            print "type(dirpath):" +str(type(dirpath))
            print "type(dirnames):" +str(type(dirnames))
            print "type(filenames):" +str(type(filenames))
            print "type(tempStr):" +str(type(tempStr))
            #print "filenames: " + str(filenames)
            #print "filename is 2: " + filename
            for fname in filenames:
                #print fname
                if fname == filename+".vbf":
                    aItem = QTableWidgetItem()
                    aItem.setText(fname)
                    self.tableWidget_FolderContentChecker.setItem(i_row, i_col+1, aItem)
             
    def checkClipBoard(self):
        clipboard_text = QtGui.QApplication.instance().clipboard().text()
        
        list1 = str(clipboard_text).split('\n')
        del(list1[-1])
        #print "list1: " + str(list1)
        list3 = [[]]
        list3.remove([])
        for l in list1:
            list2 = []
            temp_str = l
            list2 = temp_str.split('\t')
            list3.append(list2)
            #print "list3: "+str(list3)
        
        df = pd.DataFrame(list3)
        
        for c in range(0, len(df.columns)+1):
            for r in range(0, len(df.index)+1):
                aItem = QTableWidgetItem()
                try:
                    temp_str = str(df.iloc[r][c])
                    aItem.setText(temp_str)
                except:
                    print "set error"
                self.tableWidget_FolderContentChecker.setItem(r,c,aItem)

    def checkSelectedItemsInFolder(self):
        print 1
        print self.tableWidget_FolderContentChecker.selectedItems()
        for aitem in self.tableWidget_FolderContentChecker.selectedItems():
            #print "text in cell: " + aitem.text()
            i_column = aitem.column()-1
            i_row = aitem.row()
            item_text = ""
            if self.tableWidget_FolderContentChecker.item(i_row, i_column).text() <> "":
                item_text = str(self.tableWidget_FolderContentChecker.item(i_row, i_column).text().replace("/", ""))
            #print "item_text: "+item_text
            #print type(item_text)
            #print type(i_row)
            #print type(i_column)
            self.checkFolder(item_text, i_row, i_column)
        
    def excelFileDialog(self):
        try:
            filez = QFileDialog.getOpenFileName()
        except:
            print 'file load error\n'
        try:
            FileList = str(filez).strip("\(\)\"").split(",")
        except:
            print 'file path split error\n'

        for aFile in FileList:
            if aFile is not "":
                self.lineEdit_excelPath.setText(aFile)
    def excelFolderDialog(self):
        try:
            folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        except:
            print 'folder load error\n'
        self.lineEdit_currentFolder.setText(folder)
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #setup_logging()
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()