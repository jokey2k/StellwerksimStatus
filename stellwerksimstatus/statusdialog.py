import sys

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMessageBox, QDialog, QMenu

import status_rc

class StatusDialog(QDialog):
    def __init__(self):
        super(StatusDialog, self).__init__()

        self.createActions()
        self.createTrayIcon()

        self.updateTrayIconMenu(init=True)
        
    def runStellwerkSim(self):
        print("Blubb")
        pass

    def showNormal(self):
        super(StatusDialog, self).showNormal()
        self.updateTrayIconMenu()

    def hide(self):
        super(StatusDialog, self).hide()
        self.updateTrayIconMenu()

    def createActions(self):
        self.minimizeAction = QAction("Mi&nimize", self, triggered=self.hide)
        self.showAction = QAction("&Show", self, triggered=self.showNormal)
        self.runStwAction = QAction("&Run Stellwerksim", self, triggered=self.runStellwerkSim)
        self.quitAction = QAction("&Quit", self, triggered=self.quitProgram)

    def createTrayIcon(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.mini_icon = QIcon(':/frontal-train-and-rails-svgrepo-com.svg')
        self.trayIcon.setIcon(self.mini_icon)
        self.trayIcon.setToolTip("StellwerkSim Discord Status")
        self.trayIcon.show()
        self.setWindowIcon(self.mini_icon)

    def updateTrayIconMenu(self, init=False):
        self.trayIconMenu = QMenu(self)
        if self.isHidden() and not init:
            self.trayIconMenu.addAction(self.showAction)
        else:
            self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.runStwAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon.setContextMenu(self.trayIconMenu)

    def quitProgram(self):
        qApp.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)
    window = StatusDialog()
    window.show()
    sys.exit(app.exec())
