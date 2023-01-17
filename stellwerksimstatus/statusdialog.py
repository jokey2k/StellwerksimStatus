import sentry_sdk
sentry_sdk.init(
    dsn="https://537836497cdd4f9c8929b23b9fc07b25@sentry.hbch.de/3",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

import multiprocessing
import sys
import time

from PySide6.QtCore import QSettings, QUrl, QDateTime, QByteArray
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMessageBox, QDialog, QMenu
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtNetwork import QNetworkCookie

from stellwerksimstatus.ui_statusdialog import Ui_Dialog
from stellwerksimstatus.statusthread import StellwerksimStatusThread
from stellwerksimstatus import IngameStatus
import stellwerksimstatus.status_rc

STWSIM_COOKIENAMES = [
    'cb-enabled',
    'phpbb3_8isz4_sid',
    'phpbb3_8isz4_k',
    'phpbb3_8isz4_u'
]
DEFAULT_SETTINGS = {
    'homepage': 'https://www.stellwerksim.de/anlagen.php',
    'communicatorhost': 'localhost',
    'mainwindow_width': 700,
    'mainwindow_height': 700,
}

class StatusDialog(QDialog):
    def __init__(self):
        super(StatusDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.settings = QSettings()
        self.initialSettings()
        self.resize(self.settings.value('mainwindow_width'), self.settings.value('mainwindow_height'))
        self.load_application_settings()

        self.ui.browserWidget = QWebEngineView()
        self.ui.verticalLayout_2.addWidget(self.ui.browserWidget)

        self.ui.browserWidget.page().profile().cookieStore().cookieAdded.connect(self.saveWebsiteCookie)
        self.loadWebsiteCookies()
        self.ui.browserWidget.load(QUrl(self.settings.value('homepage')))

        self.createActions()
        self.createTrayIcon()

        self.updateTrayIconMenu(init=True)

        self.checkThread = None
        self.start_thread()
        self.stellwerksim_state = None

    def initialSettings(self):
        """Check that all relevant settings are configured"""

        for name, value in DEFAULT_SETTINGS.items():
            current_value = self.settings.value(name)
            if not current_value:
                self.settings.setValue(name, value)

    def load_application_settings(self):
        self.ui.homepageLineEdit.setText(self.settings.value('homepage'))
        self.ui.homepageLineEdit.returnPressed.connect(self.save_application_settings)
        self.ui.communicatorAddressLineEdit.setText(self.settings.value('communicatorhost')),
        self.ui.communicatorAddressLineEdit.returnPressed.connect(self.save_application_settings)

    def save_application_settings(self):
        self.settings.setValue('homepage', self.ui.homepageLineEdit.text())
        self.settings.setValue('communicatorhost', self.ui.communicatorAddressLineEdit.text())

    def loadWebsiteCookies(self):
        cookiestore = self.ui.browserWidget.page().profile().cookieStore()

        for cookie_name in STWSIM_COOKIENAMES:
            saved_cookie_content = self.settings.value("COOKIE_" + cookie_name)
            if not saved_cookie_content:
                continue
            cookie = QNetworkCookie()
            cookie.setName(QByteArray(cookie_name.encode('utf-8')))
            cookie.setValue(saved_cookie_content)
            cookie.setDomain('.stellwerksim.de')
            cookie.setPath('/')
            cookie.setExpirationDate(QDateTime.currentDateTime().addMonths(12))
            cookie.setHttpOnly(True)
            cookie.setSecure(False)
            cookiestore.setCookie(cookie, QUrl())

    def saveWebsiteCookie(self, newCookie):
        cookiename = newCookie.name()
        if cookiename not in STWSIM_COOKIENAMES:
            return
        self.settings.setValue("COOKIE_" + cookiename, newCookie.value())

    def runStellwerkSim(self):
        print("Blubb")
        pass

    def resizeEvent(self, event):
        super(StatusDialog, self).resizeEvent(event)
        self.settings.setValue("mainwindow_width", event.size().width())
        self.settings.setValue("mainwindow_height", event.size().height())

    def showNormal(self):
        super(StatusDialog, self).showNormal()
        self.updateTrayIconMenu()

    def hide(self):
        super(StatusDialog, self).hide()
        self.updateTrayIconMenu()

    def tray_clicked(self, reason):
        if reason != QSystemTrayIcon.ActivationReason.Trigger:
            return
        if self.isHidden():
            self.showNormal()
        else:
            self.hide()

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
        self.trayIcon.activated.connect(self.tray_clicked)

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

    def start_thread(self):
        self.checkThread = StellwerksimStatusThread(self.settings, self)
        self.checkThread.statusChanged.connect(self.update_stellwerksim_state)
        self.checkThread.start()

    def update_stellwerksim_state(self, new_state):
        if new_state is None:
            return

        self.setUpdatesEnabled(False)
        if not isinstance(new_state, IngameStatus):
            self.reset_state_labels()
            self.ui.currentRailwayControlCenterLineEdit.setText(new_state['process_status'])
            self.stellwerksim_state = None
            self.setUpdatesEnabled(True)
            return

        if new_state != self.stellwerksim_state:
            self.ui.currentRailwayControlCenterLineEdit.setText(new_state.name)
            self.ui.currentRailwayControlCenterRegionLineEdit.setText(new_state.region)
            self.ui.inGameClockLineEdit.setText(new_state.simzeit)
            self.ui.onlineLineEdit.setText('online' if new_state.online else 'offline')
            play_duration = time.time() - new_state.playtime
            secs = "%s" % (int(play_duration % 60))
            play_duration /= 60
            mins = "%s" % (int(play_duration % 60))
            play_duration /= 60
            hours = "%s" % int(play_duration)
            self.ui.playDurationLineEdit.setText(str("%s:%s:%s" % (hours, mins, secs)))

        self.setUpdatesEnabled(True)
        self.stellwerksim_state = new_state

    def reset_state_labels(self):
        self.ui.currentRailwayControlCenterLineEdit.clear()
        self.ui.currentRailwayControlCenterRegionLineEdit.clear()
        self.ui.inGameClockLineEdit.clear()
        self.ui.onlineLineEdit.clear()
        self.ui.playDurationLineEdit.clear()

    def quitProgram(self):
        qApp.quit()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)

    app.setApplicationName("StellwerksimStatusTool")
    app.setOrganizationName("JokeyMagicApps")

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)
    window = StatusDialog()
    window.show()
    sys.exit(app.exec())
