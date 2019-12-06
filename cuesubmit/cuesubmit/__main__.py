#!/usr/bin/env python

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


import sys

from PySide2 import QtWidgets

from cuesubmit import Constants
from cuesubmit import JobTypes
from cuesubmit.ui import Style
from cuesubmit.ui import Submit

from mv_vfx_framework_ui.widget_header.title_bar import DefaultTitleBar
import mv_vfx_framework_ui.styling as styling

class CueSubmitApp(QtWidgets.QApplication):
    """Standalone submission application"""

    def __init__(self, args):
        super(CueSubmitApp, self).__init__(args)
        self.mainWindow = CueSubmitMainWindow(Constants.SUBMIT_APP_WINDOW_TITLE)

    def startup(self):
        self.setApplicationName(Constants.SUBMIT_APP_WINDOW_TITLE)
        Style.init()
        self.mainWindow.show()
        self.mainWindow.submitWidget.jobTreeWidget.table.setFocus()


class CueSubmitMainWindow(QtWidgets.QMainWindow):
    """Main Window object for the standalone submission"""

    def __init__(self, name, *args, **kwargs):
        super(CueSubmitMainWindow, self).__init__(*args, **kwargs)
        self.submitWidget = Submit.CueSubmitWidget(
            settingsWidgetType=JobTypes.JobTypes.SHELL,
            parent=self
        )
        titlebar = DefaultTitleBar('OpenCue Submitter', '0.1.0', parent=self)
        style = titlebar.stylesheet_file
        styling.apply_stylesheet(titlebar, external_stylesheet=[style])
        central_widget = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(titlebar)
        central_layout.addWidget(self.submitWidget)
        self.setCentralWidget(central_widget)
        self.setWindowTitle(name)
        self.setMinimumWidth(650)
        self.resize(self.minimumWidth(), 1000)
        self.setStyleSheet(Style.MAIN_WINDOW)


def main():
    app = CueSubmitApp(sys.argv)
    app.startup()
    app.exec_()


if __name__ == '__main__':
    main()
