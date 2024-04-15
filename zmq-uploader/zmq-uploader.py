import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import PIL
import tempfile

import previewer

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

        self.previewers.append(previewer.PreviewerImage())


    def show(self):
        self.ui.show()
        sys.exit(app.exec_())

    def quit(self):
        print("bye~")
        sys.exit(app.exec_())

    def about(self):
        print("about")

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