from PySide import QtGui
from gui_tele import Ui_Dialog

__author__="Marcos Ferreira"

class Form1(QtGui.QWidget, Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        
        
if __name__ == "__main__":
    import sys
   
    app = QtGui.QApplication(sys.argv)
    form = Form1()
    form.show()
    app.exec_()