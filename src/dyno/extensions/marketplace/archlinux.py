import subprocess
import logging
import time

from dyno.extensions.extension import ParentExtension


class LinuxInterface(ParentExtension):

    @classmethod
    def open_terminal(cls, **kwargs):
        try:
            subprocess.Popen(['urxvt'], stderr=subprocess.PIPE, shell=False).communicate()
        except Exception as e:
            cls.response("Cant open terminal as {0}".format(e))

    @classmethod
    def open_editor(cls, **kwargs):
        try:
            subprocess.Popen(['gedit'], stderr=subprocess.PIPE, shell=False).communicate()
        except FileNotFoundError:
            cls.response("Cant open gedit")

    @classmethod
    def open_browser(cls, **kwargs):
        try:
            subprocess.Popen(['chromium'], stderr=subprocess.PIPE, shell=False).communicate()
        except Exception as e:
            cls.response("Cant open chromium as {0}".format(e))
            