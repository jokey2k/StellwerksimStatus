from concurrent.futures import process
from lxml import etree
import socket
import time
import errno
import discordsdk as dsdk
from multiprocessing import Process, Queue, freeze_support
from collections import namedtuple
import queue

import logging
logging.basicConfig(level=logging.NOTSET)
log = logging.getLogger()

# Changelog
# 1.0.0 - initial version
VERSION = "1.0.0"

# Discord Plugin API id
APPLICATION_ID = 934472966455046194
ElementClass = etree.Element("temp").__class__
IngameStatus = namedtuple("IngameStatus", ["name", "region", "online", "simzeit", "playtime"])

class StopRequest(StopIteration):
    pass


# debug callback
def debug_callback(debug, result, *args):
    if result == dsdk.Result.ok:
        log.debug("%s: success" % debug)
    else:
        log.error("%s: failure, %s %s" % (debug, result, args))


class DiscordPlayingPlugin:
    def __init__(self, input_queue):
        self.app = None
        try:
            self.app = dsdk.Discord(APPLICATION_ID, dsdk.CreateFlags.default)
        except Exception as e:
            log.error("Discord Plugin could not connect: %s" % (str(e)))
            return

        self.activity_manager = self.app.get_activity_manager()
        self.previous_state = None

        self.input_queue = input_queue

    def update_activity(self, current_state):
        if self.previous_state and self.previous_state == current_state:
            return

        activity_timestamps = dsdk.ActivityTimestamps()
        activity_timestamps.start = current_state.playtime

        activity_assets_playing = dsdk.ActivityAssets()
        activity_assets_playing.large_image = "signale"

        # sometimes the sim returns weird values, so do string comparison for sanity
        if current_state.online and current_state.online == "true":
            state = "Online"
        else:
            state = "Offline"
        state += ", %s" % current_state.simzeit

        activity = dsdk.Activity()
        activity.state = state
        activity.details = current_state.name
        activity.timestamps = activity_timestamps
        activity.assets = activity_assets_playing

        # we update the activity
        log.debug("Push new playing state")
        self.activity_manager.update_activity(activity, lambda result: debug_callback("update_activity", result))
        self.previous_state = current_state

    def clear_activity(self):
        self.activity_manager.clear_activity()

    def process_message(self, message):
        if isinstance(message, IngameStatus):
            self.update_activity(message)
        elif isinstance(message, StopRequest):
            raise message

    def process_events(self):
        if self.app is None:
            return
        try:
            while True:
                try:
                    message = self.input_queue.get_nowait()
                    self.process_message(message)
                except queue.Empty:
                    pass
                self.app.run_callbacks()
                time.sleep(1/10)
        except StopRequest:
            pass


class StellwerkSimPlugin:
    def __init__(self, ip, port=3691):
        self.ip = ip
        self.port = port
        self.socket = None
        self.parser = None
        self.reset_parser()
        self.reset_state()

    def reset_state(self):
        self.connected = False
        self.registered = False

        self.query_state = None

        self.status_name = None
        self.status_region = None
        self.status_online = None

        self.simzeit = None
        self.playtime = None

    def reset_parser(self):
        result = None
        if self.parser is not None:
            try:
                result = self.parser.close()
            except etree.Error as e:
                # Killing the object anyway, so don't care about errors
                pass
        self.parser = etree.XMLPullParser(events=('end',))
        return result

    def connect(self):
        self.reset_state()
        try:
            log.debug("Trying to connect to %s on %s" % (self.ip, self.port))
            self.socket = socket.create_connection((self.ip, self.port))
        except (socket.error, OSError, IOError) as e:
            log.info("Failed creating connection: %s" % str(e))
            return
        self.socket.setblocking(False)
        self.connected = True
        log.debug("Connection established to %s on %s" % (self.ip, self.port))

    def process_socket(self):
        if self.socket is None:
            return
        try:
            data = self.socket.recv(4096)
            if data is not None:
                log.debug("..Got some data, processing")
            for item in data.decode("utf-8"):
                self.parse_byte(item)
            if data == b"":
                log.debug("..Data is empty, wtf?!, terminating socket")
                try:
                    self.socket.close()
                except:
                    pass
                self.connected = False
                self.socket = None
        except socket.timeout:
            log.info("Socket timeout waiting for data, destroying connection")
            try:
                self.socket.close()
            except:
                pass
            self.connected = False
            self.socket = None
        except (socket.error, OSError, IOError) as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                # no data available
                return
            log.info("Socket error waiting for data, destroying connection. Msg: %s" % str(e))
            try:
                self.socket.close()
            except:
                pass
            self.connected = False
            self.socket = None

    def parse_byte(self, data):
        self.parser.feed(data)
        for action, element in self.parser.read_events():
            log.debug("....Received action %s for tag %s" % (action, element.tag))
            if action == "end" and element.tag == "status":
                tree = self.reset_parser()
                try:
                    code = int(tree.get("code"))
                except ValueError as e:
                    log.error("Unhandled chars in status response: %s, response was: %s" % (str(e), etree.tostring(tree)))
                    continue

                log.debug("....Got status, code: %s, content: %s" % (code, element.text))
                if code == 300 and not self.registered:
                    log.debug("....Got register request")
                    self.trigger_register()
                    continue
                elif code == 220 and self.query_state is not None and self.query_state == "register":
                    log.debug("....register was accepted")
                    self.query_state = None
                    self.registered = True
                    pass
                else:
                    log.warning(".XX.Unexpected status code received: %s" % etree.tostring(tree))
            elif action == "end" and element.tag == "anlageninfo":
                log.debug("....Got info response")
                tree = self.reset_parser()
                try:
                    self.status_name = tree.get("name")
                    log.debug("......Name: %s" % self.status_name)
                    self.status_region = tree.get("region")
                    log.debug("......Region: %s" % self.status_region)
                    self.status_online = tree.get("online")
                    log.debug("......Online: %s" % self.status_online)
                except etree.Error as e:
                    log.warning("Unexpected anlageninfo received: %s" % etree.tostring(tree))
                self.query_state = None
            elif action == "end" and element.tag == "simzeit":
                log.debug("....Got simzeit response")
                tree = self.reset_parser()
                try:
                    try:
                        time = int(tree.get("zeit"))
                    except ValueError as e:
                        log.warning("Could not convert %s to int for simzeit" % tree.get("zeit"))
                    seconds = time / 1000
                    minutes = seconds / 60
                    hours = int(minutes / 60)
                    minutes = int(minutes % 60)

                    self.simzeit = "%s:%s" % (str(hours).zfill(2), str(minutes).zfill(2))
                    log.debug("......simzeit: %s" % self.simzeit)
                except etree.Error as e:
                    log.warning("Unexpected simzeit received: %s" % etree.tostring(tree))
                self.query_state = None
            else:
                log.debug("....Got tag end for %s but not used, ignored" % element.tag)

    def trigger_register(self):
        self.query_state = "register"
        elem = etree.Element("register")
        elem.set("name", "StellwerksimDiscordStatus")
        elem.set("autor", "Markus Ullmann <mail@markus-ullmann.de>")
        elem.set("version", "1.0.0")
        elem.set("protokoll", "1")
        elem.set("text", "Shows current game info in discord")
        self.write_socket(elem)
        log.debug("..sent register")

    def trigger_status(self):
        self.query_state = "anlageninfo"
        elem = etree.Element("anlageninfo")
        self.write_socket(elem)
        log.debug("..sent status request")

    def trigger_simzeit(self):
        self.query_state = "simzeit"
        elem = etree.Element("simzeit")
        elem.set("sender", "123456")
        self.write_socket(elem)
        log.debug("..sent status request")

    def write_socket(self, data):
        if self.socket is None:
            return

        if isinstance(data, ElementClass):
            data = etree.tostring(data)

        try:
            self.socket.send(data)
            self.socket.send(b"\n")
        except (socket.error, OSError, IOError):
            pass

    def combine_status(self):
        if self.registered and self.status_name and self.status_region and self.status_online and self.simzeit:
            return IngameStatus(self.status_name, self.status_region, self.status_online, self.simzeit, self.playtime)
        else:
            return None

def run_discord_process(input_queue):
    plugin = DiscordPlayingPlugin(input_queue)
    plugin.process_events()


def main(stop_signal=None):
    freeze_support()

    discordprocess = None
    discordqueue = None

    stellwerksim = StellwerkSimPlugin("localhost")
    i = 0
    while True:
        if not stellwerksim.connected:
            if discordprocess is not None:
                log.debug("Discord Status process will be shut down")
                if discordprocess.is_alive():
                    discordqueue.put(StopRequest())
                    discordprocess.join()
                    discordqueue.close()
                discordprocess = None
                discordqueue = None
            stellwerksim.connect()
            stellwerksim.playtime = time.time()
        if not stellwerksim.connected:
            time.sleep(5)
            continue
        if stellwerksim.connected and not stellwerksim.registered:
            stellwerksim.process_socket()
            time.sleep(0.1)
            continue

        if discordprocess is None:
            log.debug("Discord Status process will be launched")
            discordqueue = Queue()
            discordprocess = Process(target=run_discord_process, args=(discordqueue,))
            discordprocess.start()

        i += 1
        if not i % 10:
            if stellwerksim.query_state is None:
                stellwerksim.trigger_status()
        if not (i+5) % 10:
            if stellwerksim.query_state is None:
                stellwerksim.trigger_simzeit()
        stellwerksim.process_socket()
        discordqueue.put(stellwerksim.combine_status())
        time.sleep(1)

        if stop_signal is not None and stop_signal.is_set():
            break
    
    if discordprocess.is_alive():
        discordqueue.put(StopRequest())
        discordprocess.join()
        discordqueue.close()
    discordprocess = None
    discordqueue = None


if __name__ == "__main__":
    main()