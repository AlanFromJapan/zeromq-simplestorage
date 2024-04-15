import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import PIL
import tempfile

import previewer
import zmqcommands
import config

class UIMain():
    currentFile = None
    previewers = []

    def __init__(self) -> None:
        self.currentFile = None

        self.ui = uic.loadUi('ui-main.ui')
        self.ui.action_Quit.triggered.connect(self.quit)
        self.ui.menu_About.triggered.connect(self.about)
        self.ui.btnPickAFile.clicked.connect(self.pickAFile)
        self.ui.actionPick_a_File.triggered.connect(self.pickAFile)
        self.ui.btnZMQStatus.clicked.connect(self.zmqStatus)
        self.ui.btnZMQList.clicked.connect(self.zmqList)
        self.ui.btnStore.clicked.connect(self.zmqStoreFile)
        self.ui.btnZMQDropHead.clicked.connect(self.zmqDropHead)

        self.previewers.append(previewer.PreviewerImage())

        self.ui.lblServerURL.setText(config.config["zmq_server"])

    def show(self):
        self.ui.show()
        sys.exit(app.exec_())

    def quit(self):
        print("bye~")
        sys.exit(app.exec_())

    def about(self):
        print("about")

    def zmqStatus(self):
        QMessageBox.information(self.ui, "ZMQ Status", zmqcommands.ping())

    def zmqList(self):
        QMessageBox.information(self.ui, "ZMQ current list", zmqcommands.list())

    def zmqStoreFile(self):
        if self.currentFile is None:
            QMessageBox.warning(self.ui, "No file selected", "Please select a file first")
            return        
        QMessageBox.information(self.ui, "ZMQ upload", zmqcommands.storeFile(self.currentFile))

    
    def zmqDropHead(self):
        if QMessageBox.Yes == QMessageBox.question(self.ui, "Confirmation", "Are you sure you want to drop the head of the MQ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No):
            #let's do it
            zmqcommands.dropHead()

    def pickAFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self.ui, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.currentFile = fileName
            self.ui.lblFile.setText(fileName)
            self.ui.btnStore.setEnabled(True)

            #try to make a preview
            try:
                self.ui.lblPreview.clear()

                for p in self.previewers:
                    if fileName.split('.')[-1] in p.capableExt():
                        imgPIL = p.preview(fileName)

                        #PIL install broken, but this should work
                        #self.ui.lblPreview.setPixmap(QPixmap.fromImage(PIL.ImageQt.ImageQt(imgPIL).copy()))

                        #forgive me for this
                        with tempfile.TemporaryDirectory() as temp:
                            fname = os.path.join(temp, "temp.jpg")
                            try:
                                imgPIL.save(fname)
                                self.ui.lblPreview.setScaledContents(True)
                                self.ui.lblPreview.setPixmap(QPixmap(fname))
                            finally:
                                os.remove(fname)

                        break
                
            except Exception as e:
                print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UIMain()
    ui.show()