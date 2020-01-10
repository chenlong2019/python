from PyQt5 import QtWidgets
from   MainForm import  Ui_MainWindow

def test(text):
    print( 'text')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui=Ui_MainWindow()
    Ui_MainWindow.setupUi(ui,MainWindow)
    MainWindow.show()
    QtWidgets.QApplication.processEvents()
    ###################
    # app.installEventFilter(MainWindow)
    sys.exit(app.exec_())