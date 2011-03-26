#!/usr/bin/env python
# -*- coding: latin-1 -*-

import threading
import thread
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import dbf
import os.path
from datetime import datetime
import time
import os
import string

from readdbf import ReadDbf

gobject.threads_init()

class SimpleDbfBrowser:
    main_title = "Simple DBF Browser"
    version = "1.0.1-20110327_0208"

    window = None
    content_box = None
    scrolled_window = None
    list_view = None
    dbf_file = None
    dbf_table = None
    dbf_length = None
    row_count = 0

    progress_message = None

    def __init__(self):
        if os.name == 'nt':
            gtk.rc_parse("gtkrc")

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(self.main_title)
        self.window.set_size_request(500,400)

        self.vbox = gtk.VBox(False, 0)
        self.vbox.show()

        self.init_ui_manager()

        self.list_view = gtk.TreeView()
        self.list_view.show()

        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolled_window.add(self.list_view)
        self.scrolled_window.show()

        self.content_box = gtk.VBox(False, 0)
        self.content_box.pack_start(self.scrolled_window, True, True, 0)
        self.content_box.show()

        self.vbox.pack_start(self.content_box, True, True, 0)

        self.window.connect("delete_event", gtk.main_quit)

        self.window.add(self.vbox)
        self.window.show()

    def init_ui_manager(self):
        ui = """<ui>
            <menubar name="MenuBar">
                <menu action="File">
                    <menuitem action="Open" />
                    <separator/>
                    <menuitem action="Exit" />
                </menu>
                <menu action="Help">
                    <menuitem action="About" />
                </menu>
            </menubar>
        </ui>"""

        ui_manager = gtk.UIManager()
        accel_group = ui_manager.get_accel_group()
        self.window.add_accel_group(accel_group)
        action_group = gtk.ActionGroup("Main Action Group")
        action_group.add_actions(
            [
                ("File", None, "_File", None, None, None),
                ("Open", None, "_Open", "<control>O", None, self.show_open_dialog),
                ("Exit", None, "Exit", "<control>X", "Keluar aplikasi", gtk.main_quit),
                ("Help", None, "_Help", None, None, None),
                ("About", None, "_About", "<control>A", None, self.show_about_window),
            ]
        )

        ui_manager.insert_action_group(action_group, 0)
        ui_manager.add_ui_from_string(ui)

        menu_bar = ui_manager.get_widget("/MenuBar")
        self.vbox.pack_start(menu_bar, False, False, 0)
        menu_bar.show()

        return

    def main(self):
        gtk.main()

    def show_open_dialog(self, w):
        dialog = gtk.FileChooserDialog(
            'Open DBF File', self.window, gtk.FILE_CHOOSER_ACTION_OPEN,
            (
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                gtk.STOCK_OPEN, gtk.RESPONSE_OK
            )
        )

        file_filter = gtk.FileFilter()
        file_filter.set_name("DBF files")
        file_filter.add_pattern("*.dbf")
        file_filter.add_pattern("*.DBF")
        file_filter.add_pattern("*.keu")
        file_filter.add_pattern("*.KEU")
        file_filter.add_pattern("*.dja")
        file_filter.add_pattern("*.DJA")
        dialog.add_filter(file_filter)

        file_filter = gtk.FileFilter()
        file_filter.set_name("All files")
        file_filter.add_pattern("*.*")
        file_filter.add_pattern("*")
        dialog.add_filter(file_filter)

        if self.dbf_file:
            dialog.set_current_folder(os.path.dirname(self.dbf_file))

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.dbf_file = dialog.get_filename()
            dialog.destroy()
            self.open_dbf_file(self.dbf_file)
        else:
            dialog.destroy()

    def open_dbf_file(self, dbf_file = None):
        if dbf_file:
            self.dbf_file = dbf_file
        else:
            dbf_file = self.dbf_file

        self.dbf_length = None

        self.row_count = 0
        self.window.set_title("%s: %s" % (self.main_title, os.path.basename(dbf_file)))

        self.progress_window_show()

        print datetime.today(), 'detaching model'
        self.list_view.set_model()
        print datetime.today(), 'model detached'

        read_dbf = ReadDbf(self)
        read_dbf.start()

    def progress_window_show(self):
        self.progress_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.progress_window.set_title('Reading DBF file...')
        self.progress_window.set_border_width(10)
        self.progress_window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_SPLASHSCREEN)
        self.progress_window.set_modal(True)
        self.progress_window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.progress_window.set_property("skip-taskbar-hint", True)
        self.progress_window.set_transient_for(self.window)

        vbox = gtk.VBox(False, 5)

        label = gtk.Label('Please wait while reading DBF file...')
        vbox.pack_start(label, True, True, 5)
        label.show()

        self.progress_message = gtk.Label('preparing')
        vbox.pack_start(self.progress_message, True, True, 5)
        self.progress_message.show()

        self.progress_bar = gtk.ProgressBar()
        self.progress_bar.set_orientation(gtk.PROGRESS_LEFT_TO_RIGHT)
        self.progress_bar.show()
        vbox.pack_start(self.progress_bar, True, True, 5)

        vbox.show()
        self.progress_window.add(vbox)
        self.progress_window.show()

        self.progress_timeout_source_id = gobject.timeout_add(500, self.progress_bar_timeout)

        #while gtk.events_pending():
        #    gtk.main_iteration()

    def progress_bar_timeout(self):
        if self.row_count:
            self.progress_bar_update_status('%s: %d / %d rows' % (os.path.basename(self.dbf_file), self.row_count, self.dbf_length))

            if self.row_count and self.dbf_table and self.dbf_length:
                progress_fraction = 1.0 * self.row_count / self.dbf_length
                self.progress_bar.set_fraction(progress_fraction)
                self.progress_bar.set_text("{0:.0f}%".format(progress_fraction * 100))
            else:
                self.progress_bar.pulse()

        else:
            self.progress_bar.pulse()
        return True

    def progress_bar_update_status(self, message):
        self.progress_message.set_text(message)

    def show_about_window(self, data):
        about_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        about_window.set_title(self.main_title)
        about_window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        about_window.set_resizable(False)
        about_window.set_modal(True)
        about_window.set_property('skip-taskbar-hint', True)
        about_window.set_transient_for(self.window)
        about_window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        about_window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#fff'))

        vbox = gtk.VBox(False, 0)
        vbox.show()

        image = gtk.Image()
        image.set_from_file("resources/logo.png")
        image.show()

        vbox.pack_start(image, False, False, 0)

        textview = gtk.TextView()
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        textbuffer = textview.get_buffer()

        textbuffer.set_text("""
%s %s
http://www.mondial.co.id/products/simpledbfbrowser/

A free and opensource DBF file viewer.
Licensed under GPLv2.

This application would not exists without:
* Python (http://www.python.org/)
* PyGTK (http://www.pygtk.org/)
* dbf python package (http://pypi.python.org/pypi/dbf/)

© PT MONDIAL TEKNOLOGI SOLUSI, 2011
http://www.mondial.co.id/
contact@mondial.co.id

All rights reserved.
""" % (self.main_title, self.version))

        textview.set_left_margin(10)
        textview.set_right_margin(10)
        textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.Color('#F2F1F0'))

        textview.show()

        vbox.pack_start(textview, True, True, 0)
        about_window.add(vbox)
        about_window.show()
        return

if __name__ == "__main__":
    main_app = SimpleDbfBrowser()
    main_app.main()
