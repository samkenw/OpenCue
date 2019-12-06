#!/usr/bin/python

#  Copyright (c) 2018 Sony Pictures Imageworks Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


"""Nimby allows a desktop to be used as a render host when not used."""


import os
import select
import time
import signal
import threading
import logging as log
import pynput

import rqconstants
import rqutil


class Nimby(threading.Thread):
    """Nimby == Not In My Back Yard.
       If enabled, nimby will lock and kill all frames running on the host if
       keyboard or mouse activity is detected. If sufficient idle time has
       passed, defined in the Constants class, nimby will then unlock the host
       and make it available for rendering."""

    
    def __init__(self, rqCore):
        """Nimby initialization
        @type    rqCore: RqCore
        @param   rqCore: Main RQD Object"""
        threading.Thread.__init__(self)

        self.rqCore = rqCore

        self.mouse_listener = pynput.mouse.Listener(on_move=self.on_interaction, on_click=self.on_interaction, on_scroll=self.on_interaction)
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_interaction)

        self.locked = False
        self.active = False

        self.thread = None

        self.interaction_detected = False

        signal.signal(signal.SIGINT, self.signalHandler)

    def on_interaction(self, *args):
        self.interaction_detected = True

    def signalHandler(self, sig, frame):
        """If a signal is detected, call .stop()"""
        self.stop()

    def lockNimby(self):
        """Activates the nimby lock, calls lockNimby() in rqcore"""
        if self.active and not self.locked:
            self.locked = True
            log.info("Locked nimby")
            self.rqCore.onNimbyLock()

    def unlockNimby(self, asOf=None):
        """Deactivates the nimby lock, calls unlockNimby() in rqcore
        @param asOf: Time when idle state began, if known."""
        if self.locked:
            self.locked = False
            log.info("Unlocked nimby")
            self.rqCore.onNimbyUnlock(asOf=asOf)

    def lockedInUse(self):
        """Nimby State: Machine is in use, host is locked,
                        waiting for sufficient idle time"""
        log.debug("lockedInUse")

        self.interaction_detected = False
        
        time.sleep(5)
        if self.active and self.interaction_detected == False:
            self.lockedIdle()
        elif self.active:

            self.thread = threading.Timer(rqconstants.CHECK_INTERVAL_LOCKED,
                                          self.lockedInUse)
            self.thread.start()

    def lockedIdle(self):
        """Nimby State: Machine is idle,
                        waiting for sufficient idle time to unlock"""
        log.debug("locked_idle")
        waitStartTime = time.time()

        time.sleep(rqconstants.MINIMUM_IDLE)

        if self.active and self.interaction_detected == False and \
           self.rqCore.machine.isNimbySafeToUnlock():

            self.unlockNimby(asOf=waitStartTime)
            self.unlockedIdle()
        elif self.active:

            self.thread = threading.Timer(rqconstants.CHECK_INTERVAL_LOCKED,
                                          self.lockedInUse)
            self.thread.start()

    def unlockedIdle(self):
        """Nimby State: Machine is idle, host is unlocked,
                        waiting for user activity"""
        log.debug("unlockedIdle")

        while self.active and \
              self.interaction_detected == False and \
              self.rqCore.machine.isNimbySafeToRunJobs():

            time.sleep(5)

            if not self.rqCore.machine.isNimbySafeToRunJobs():
                log.warning("memory threshold has been exceeded, locking nimby")
                self.active = True

        if self.active:
            self.lockNimby()
            self.thread = threading.Timer(rqconstants.CHECK_INTERVAL_LOCKED,
                                          self.lockedInUse)
            self.thread.start()

    def run(self):
        """Starts the Nimby thread"""
        log.debug("nimby.run()")
        self.active = True
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.unlockedIdle()

    def stop(self):
        """Stops the Nimby thread"""
        log.debug("nimby.stop()")
        if self.thread:
            self.thread.cancel()
        self.active = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.unlockNimby()
