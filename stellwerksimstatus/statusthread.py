import base64

import psutil
from PySide6.QtCore import QThread, Signal

from stellwerksimstatus import StellwerkSimPlugin, IngameStatus

class StellwerksimStatusThread(QThread):
    statusChanged = Signal(IngameStatus)

    def __init__(self, settings, parent=None):
        super(StellwerksimStatusThread, self).__init__(parent)
        self.settings = settings

    def set_offline(self):
        self.currentStatus = {
            'process_running': False,
            'process_pid': None,
            'socket_active': False
        }

    def stop_request(self):
        self.stop_requested = True

    def run(self):
        self.set_offline()
        self.stop_requested = False
        self.stellwerksim_socket = StellwerkSimPlugin(self.settings.value('communicatorhost'))

        i = 0

        previous_status = None

        while not self.stop_requested:
            if not self.stellwerksim_socket.connected:
                if i % 5 == 0:
                    # only check every 5 seconds, this is somehow expensive
                    # FIXME: Add psutil.pid_exists(pid) to possibly skip this, needs performance check
                    self.currentStatus['process_running'] = self.check_communicator_process()
                    if self.currentStatus['process_running']:
                        self.stellwerksim_socket.connect()
                    status = {'process_status': 'Connector running' if self.currentStatus['process_running'] else 'Connector not running'}
                    if not self.stellwerksim_socket.connected:
                        self.statusChanged.emit(status)
                        i += 1
                        self.sleep(1)
                        continue
            else:
                self.currentStatus['process_running'] = True

            if i % 10 == 0:
                self.stellwerksim_socket.trigger_simzeit()
                self.stellwerksim_socket.trigger_status()

            self.stellwerksim_socket.process_socket()
            current_status = self.stellwerksim_socket.combine_status()
            if current_status is not None and previous_status != current_status:
                self.statusChanged.emit(current_status)
            previous_status = current_status
            i += 1
            self.sleep(1)

    def check_communicator_process(self):
        found_running = False

        for proc in psutil.process_iter():
            cmdline = []
            try:
                processName = proc.name()
                if not processName.startswith("jp2launcher"):
                    continue
                cmdline = proc.cmdline()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

            if self.currentStatus['process_pid'] == proc.pid:
                found_running = True
                break
            if '-vma' not in cmdline:
                continue
            vma_data_index = cmdline.index('-vma') + 1
            if len(cmdline) < vma_data_index:
                continue

            process_data_encoded = cmdline[vma_data_index]
            process_data = base64.b64decode(process_data_encoded)

            process_data_parts = process_data.split(b'\x00')
            if b'-Djnlp.webserver=www.stellwerksim.de' in process_data_parts:
                self.currentStatus['process_pid'] = proc.pid
                found_running = True
                break

        return found_running
