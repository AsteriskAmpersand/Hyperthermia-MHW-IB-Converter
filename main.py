# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:02:41 2020

@author: AsteriskAmpersand
"""

import os
import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPalette, QColor, QIcon
from gui.IBConverter import Ui_MainWindow
from gui.OptionDialogue2 import Ui_Dialog as dialog2
from gui.OptionDialogue3 import Ui_Dialog as dialog3
from compatibilityCore import CompatibilityEngine

class Options2(QtWidgets.QDialog, dialog2):
    def __init__(self,string,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.text.setText(string)
        self.matchPressed.clicked.connect(self.match)
        self.defaultPressed.clicked.connect(self.default)
    def getValues(self):
        return self.useDefault
    def default(self):
        self.useDefault = True
        self.accept()
        return
    def match(self):
        self.useDefault = False
        self.accept()
        return

class Options3(QtWidgets.QDialog, dialog3):
    def __init__(self,string,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.text.setText(string)
        self.matchPressed.clicked.connect(self.match)
        self.hollowPressed.clicked.connect(self.hollow)
        self.hairPressed.clicked.connect(self.hair)
    def getValues(self):
        return self.choice
    def hollow(self):
        self.choice = "H"
        self.accept()
        return
    def match(self):
        self.choice = "S"
        self.accept()
        return
    def hair(self):
        self.choice = "F"
        self.accept()
        return
    
def appPath(path):
    if getattr(sys, 'frozen', False):
        application_path = Path(sys._MEIPASS)
    elif __file__:
        application_path = Path(os.path.dirname(os.path.dirname(__file__)))
    return application_path.joinpath(path)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, arguments):
        super().__init__()
        self.setWindowIcon(QIcon(str(appPath(r"icon\DodoSama.png"))))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Asterisk's Hyperthermia Converter")
        self.ui.convertButton.clicked.connect(self.convert)
        self.ui.addFolder.clicked.connect(self.openFolder)
        self.ui.addFile.clicked.connect(self.openFile)
        self.ui.removeFile.clicked.connect(self.removeFile)
        self.show()
        
    def convert(self):
        evDefaults = self.getEVDefaults()
        evInputPrompts = self.getEVPrompts()
        output = self.outputPipe()
        engine = CompatibilityEngine(evDefaults,evInputPrompts,output)
        extensions = self.getEnabledExtensions()
        task = []
        output("Starting Conversion Process for Extensions: %s"%', '.join(extensions))        
        for fileFolder in self.getTasks():
            if fileFolder.is_file():
                task.append(fileFolder)
            else:
                for extension in extensions:
                    for file in fileFolder.rglob(extension):
                        task.append(file)
        output("Detected %d files for conversion"%len(task))
        for taskfile in task:
            engine.convert(taskfile,self.getDebug())
        output("Finished conversion process")
        
    def openFile(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if dlg.exec_():
            filename = dlg.selectedFiles()
        self.addFiles(filename)
    def openFolder(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.Directory)
        dlg.setOption(dlg.ShowDirsOnly,False)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
        self.addFiles(filenames)
    def test(self):
        def get2Options(string):
            dlg = Options2(string)
            if dlg.exec():
                return dlg.getValues()
        return get2Options
    
    def addFiles(self,filePaths):
        for file in filePaths:
            data = QtWidgets.QListWidgetItem(str(file))
            self.ui.taskList.addItem(data)
        return
            
    def removeFile(self):
        current = self.ui.taskList.currentRow()
        self.ui.taskList.takeItem(current)
        return
    
    def getTasks(self):
        tasks = []
        for i in range(self.ui.taskList.count()):
            item = self.ui.taskList.item(i)
            if item:
                path = Path(item.data(0))
                tasks.append(path)
        return tasks
    
    def outputPipe(self):
        def write(string):
            self.ui.Log.append(string)
        return write
    
    def getEVPrompts(self):
        caller = {}
        formattableString = lambda x,y:"For %s, what type of %s should be used?\n[%s]"%(x.stem,y,x)
        def getBodyOptions(string):
            dlg = Options2(formattableString(string,"EVBD (Body Modifier)"))
            if dlg.exec():
                return dlg.getValues()
        def getWeaponOptions(string):
            dlg = Options2(formattableString(string,"EVWP (Weapon Sheathed Position)"))
            if dlg.exec():
                return dlg.getValues()
        def getHeadOptions(string):
            dlg = Options3(formattableString(string,"EVHL (Player Head Size/Shape Modifier)"))
            if dlg.exec():
                return dlg.getValues()
        caller["Body"] = getBodyOptions
        caller["Head"] = getHeadOptions
        caller["Weapons"] = getWeaponOptions
        return caller
    
    def getEVDefaults(self):
        decider = {}
        if self.ui.bodyDefault.isChecked(): 
            decider["Body"] = "Default"
        elif self.ui.bodySearch.isChecked(): 
            decider["Body"] = None
        elif self.ui.bodyCase.isChecked():
            decider["Body"] = "Input"
            
        if self.ui.weaponDefault.isChecked(): 
            decider["Weapons"] = "Default"
        elif self.ui.weaponSearch.isChecked(): 
            decider["Weapons"] = None
        elif self.ui.weaponCase.isChecked():
            decider["Weapons"] = "Input"
            
        if self.ui.headSearch.isChecked(): 
            decider["Head"] = None
        elif self.ui.headCase.isChecked(): 
            decider["Head"] = "Input"
        elif self.ui.headHollow.isChecked():
            decider["Head"] = "H"   
        elif self.ui.headHair.isChecked():
            decider["Head"] = "F"
            
        return decider
            
    def getEnabledExtensions(self):
        extensions = []
        if self.ui.convertMrl3.isChecked(): extensions.append("*.mrl3")
        if self.ui.convertCTC.isChecked(): extensions.append("*.ctc")
        if self.ui.convertCCL.isChecked(): extensions.append("*.ccl")
        if self.ui.convertEVHL.isChecked(): extensions.append("*.evhl")
        if self.ui.convertEVBD.isChecked(): extensions.append("*.evbd")
        if self.ui.convertEVWP.isChecked(): extensions.append("*.evwp")
        return extensions       
    
    def getDebug(self):
        return self.ui.debug.isChecked()
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    
    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")
    
    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QPalette.Text, QtCore.Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)


    args = app.arguments()[1:]
    window = MainWindow(args)
    sys.exit(app.exec_())