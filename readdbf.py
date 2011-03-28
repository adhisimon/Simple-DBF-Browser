#!/usr/bin/env python

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

class ReadDbf(threading.Thread):
    finished = None
    caller = None

    def __init__(self, caller):
        super(ReadDbf, self).__init__()
        self.caller = caller

    def run(self):
        caller = self.caller
        statusbar_context_id = caller.statusbar.get_context_id('ReadDbf Thread')

        if caller.scrolled_window:
            print datetime.today(), "destroying old visualization"
            gobject.idle_add(caller.scrolled_window.destroy)
            print datetime.today(), "old visualization destroyed"

        print datetime.today(), "opening dbf file"
        gobject.idle_add(caller.statusbar.push, statusbar_context_id, 'opening %s' % caller.dbf_file)
        caller.dbf_table = dbf.Table(caller.dbf_file, read_only = True)
        caller.dbf_length = len(caller.dbf_table)

        print datetime.today(), "retrieving fields"
        fields = dbf.get_fields(caller.dbf_table)
        print datetime.today(), "fields retrieved"

        print datetime.today(), "creating new visualization"

        store_param= [str] * len(fields)
        store_param.insert(0, int)

        store = gtk.ListStore(*store_param)
        caller.list_view = gtk.TreeView(store)
        caller.list_view.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_HORIZONTAL)

        caller.scrolled_window = gtk.ScrolledWindow()
        caller.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        caller.scrolled_window.add(caller.list_view)
        caller.content_box.pack_start(caller.scrolled_window, True, True, 0)

        i = 0
        print datetime.today(), "populating list view"
        column = gtk.TreeViewColumn("No.")
        caller.list_view.append_column(column)
        cell = gtk.CellRendererText()
        cell.set_alignment(1, 0)
        column.pack_start(cell, True)
        column.add_attribute(cell, 'text', i)

        print datetime.today(), "creating columns for fields"
        for field_name in fields:
            i += 1
            column = gtk.TreeViewColumn(field_name)
            caller.list_view.append_column(column)
            cell = gtk.CellRendererText()
            column.pack_start(cell, True)
            column.add_attribute(cell, 'text', i)
            column.set_resizable(True)

        print datetime.today(), "retrieving old model"
        model = caller.list_view.get_model()
        print datetime.today(), "unset model"
        caller.list_view.set_model()

        caller.row_count = 0
        print datetime.today(), "iterating table"
        for row in caller.dbf_table:
            caller.row_count += 1
            try:
                data = list(row)
                data.insert(0, caller.row_count)
                model.append(data)
            except:
                print datetime.today(), 'error detected (64b68)'
                print row
            #time.sleep(1)

        print datetime.today(), "setting list view model"
        caller.list_view.set_model(model)
        print datetime.today(), "queue to show list view"
        gobject.idle_add(caller.list_view.show)
        print datetime.today(), "queue to show scrolled window"
        gobject.idle_add(caller.scrolled_window.show)
        print datetime.today(), "queue to destroy progress window"
        gobject.idle_add(caller.progress_window.destroy)

        print datetime.today(), "removing progress pulse"
        gobject.source_remove(caller.progress_timeout_source_id)

        gobject.idle_add(caller.statusbar.push, statusbar_context_id, "%s (%d rows)" % (os.path.basename(caller.dbf_file), caller.dbf_length))
        gobject.idle_add(caller.table_info_menu_item.set_sensitive, True)

        self.finished = True

if __name__ == "__main__":
    from simpledbfbrowser import SimpleDbfBrowser
    main_app = SimpleDbfBrowser()
    main_app.main()
