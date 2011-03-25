#!/usr/bin/env python
# -*- coding: latin-1 -*-

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import dbf
import os.path
from datetime import datetime

class EksplorasiDbf:
    main_title = "Simple DBF Browser"
    version = "1.0.0-20110325_1729"

    window = None
    content_box = None
    scrolled_window = None
    list_view = None
    dbf_file = None

    def __init__(self):
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
            self.open_dbf_file(dialog.get_filename())

        dialog.destroy()

    def open_dbf_file(self, dbf_file):
        self.dbf_file = dbf_file
        self.window.set_title("%s: %s" % (self.main_title, os.path.basename(dbf_file)))

        print datetime.today(), "opening dbf file"
        self.dbf_table = dbf.Table(dbf_file, read_only = True)

        print datetime.today(), "retrieving fields"
        fields = dbf.get_fields(self.dbf_table)
        print datetime.today(), "fields retrieved"

        if self.scrolled_window:
            print datetime.today(), "destroying old visualization"
            self.scrolled_window.destroy()


        print datetime.today(), "creating new visualization"

        store_param= [str] * len(fields)
        store_param.insert(0, int)

        store = gtk.ListStore(*store_param)
        self.list_view = gtk.TreeView(store)
        self.list_view.show()
        self.list_view.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_HORIZONTAL)

        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolled_window.add(self.list_view)
        self.scrolled_window.show()
        self.content_box.pack_start(self.scrolled_window, True, True, 0)

        i = 0
        print datetime.today(), "populating list view"
        column = gtk.TreeViewColumn("No.")
        self.list_view.append_column(column)
        cell = gtk.CellRendererText()
        cell.set_alignment(1, 0)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', i)

        for field_name in fields:
            i = i + 1
            column = gtk.TreeViewColumn(field_name)
            self.list_view.append_column(column)
            cell = gtk.CellRendererText()
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', i)
            column.set_resizable(True)

        model = self.list_view.get_model()
        self.list_view.set_model()

        row_count = 0
        for row in self.dbf_table:
            row_count = row_count + 1
            data = list(row)
            data.insert(0, row_count)
            model.append(data)

        self.list_view.set_model(model)

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
    eksplorasi_dbf = EksplorasiDbf()
    eksplorasi_dbf.main()
