#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import gtk
from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.graphics.toolbutton import ToolButton
from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton
from sugar.graphics.toolbarbox import ToolbarButton
import sugargame.canvas
#import main
from gettext import gettext as _

class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.max_participants = 1
        self._birth = [31, 12, 2011]
        self._today = [31, 12, 2012]

        #self._activity = main.Main(self)
        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.set_canvas(self._pygamecanvas)
        #self._pygamecanvas.run_pygame(self._activity.run)


    def build_toolbar(self):

        toolbox = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbox.toolbar.insert(activity_button, -1)
        activity_button.show()

        self.build_birth_toolbar(toolbox)
        self.build_today_toolbar(toolbox)

        separador13 = gtk.SeparatorToolItem()
        separador13.props.draw = False
        separador13.set_expand(True)
        toolbox.toolbar.insert(separador13, -1)

        stop_button = StopButton(self)
        stop_button.props.accelerator = _('<Ctrl>Q')
        toolbox.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbox(toolbox)
        toolbox.show()

        self.show_all()

    def build_birth_toolbar(self, toolbox):

        birth_bar = gtk.Toolbar()

        item1 = gtk.ToolItem()
        self.label_birth = gtk.Label()
        self.label_birth.set_text(_('Birth:') + ' ' + _('Day') + ' ')
        item1.add(self.label_birth)
        birth_bar.insert(item1, -1)

        item2 = gtk.ToolItem()
        self.day_spin = gtk.SpinButton()
        self.day_spin.set_range(1, 31)
        self.day_spin.set_increments(1, 5)
        self.day_spin.props.value = 31
        self.day_spin.connect('notify::value', self.day_birth_change)
        item2.add(self.day_spin)
        birth_bar.insert(item2, -1)

        item3 = gtk.ToolItem()
        self.label_birth_month = gtk.Label()
        self.label_birth_month.set_text(' ' + _('Month') + ' ')
        item3.add(self.label_birth_month)
        birth_bar.insert(item3, -1)

        item4 = gtk.ToolItem()
        self.month_spin = gtk.SpinButton()
        self.month_spin.set_range(1, 12)
        self.month_spin.set_increments(1, 4)
        self.month_spin.props.value = 12
        self.month_spin.connect('notify::value', self.month_birth_change)
        item4.add(self.month_spin)
        birth_bar.insert(item4, -1)

        item5 = gtk.ToolItem()
        self.label_birth_year = gtk.Label()
        self.label_birth_year.set_text(' ' + _('Year') + ' ')
        item5.add(self.label_birth_year)
        birth_bar.insert(item5, -1)

        item6 = gtk.ToolItem()
        self.year_spin = gtk.SpinButton()
        self.year_spin.set_range(1900, 2012)
        self.year_spin.set_increments(1, 10)
        self.year_spin.props.value = 2011
        self.year_spin.connect('notify::value', self.year_birth_change)
        item6.add(self.year_spin)
        birth_bar.insert(item6, -1)

        birth_bar.show_all()
        birth_button = ToolbarButton(label=_('Birth'),
                page=birth_bar,
                icon_name='write-date')
        toolbox.toolbar.insert(birth_button, -1)
        birth_button.show()

    def build_today_toolbar(self, toolbox):

        today_bar = gtk.Toolbar()

        item1 = gtk.ToolItem()
        self.label_today = gtk.Label()
        self.label_today.set_text(_('Today:') + ' ' + _('Day') + ' ')
        item1.add(self.label_today)
        today_bar.insert(item1, -1)

        item2 = gtk.ToolItem()
        self.day_spin = gtk.SpinButton()
        self.day_spin.set_range(1, 31)
        self.day_spin.set_increments(1, 5)
        self.day_spin.props.value = 31
        self.day_spin.connect('notify::value', self.day_today_change)
        item2.add(self.day_spin)
        today_bar.insert(item2, -1)

        item3 = gtk.ToolItem()
        self.label_today_month = gtk.Label()
        self.label_today_month.set_text(' ' + _('Month') + ' ')
        item3.add(self.label_today_month)
        today_bar.insert(item3, -1)

        item4 = gtk.ToolItem()
        self.month_spin = gtk.SpinButton()
        self.month_spin.set_range(1, 12)
        self.month_spin.set_increments(1, 4)
        self.month_spin.props.value = 12
        self.month_spin.connect('notify::value', self.month_today_change)
        item4.add(self.month_spin)
        today_bar.insert(item4, -1)

        item5 = gtk.ToolItem()
        self.label_today_year = gtk.Label()
        self.label_today_year.set_text(' ' + _('Year') + ' ')
        item5.add(self.label_today_year)
        today_bar.insert(item5, -1)

        item6 = gtk.ToolItem()
        self.year_spin = gtk.SpinButton()
        self.year_spin.set_range(1900, 2012)
        self.year_spin.set_increments(1, 10)
        self.year_spin.props.value = 2012
        self.year_spin.connect('notify::value', self.year_today_change)
        item6.add(self.year_spin)
        today_bar.insert(item6, -1)

        today_bar.show_all()
        today_button = ToolbarButton(label=_('Today'),
                page=today_bar,
                icon_name='write-time')
        toolbox.toolbar.insert(today_button, -1)
        today_button.show()


    # BIRTH
    def day_birth_change(self, day, value):
        self._birth[0] = int(day.props.value)

    def month_birth_change(self, month, value):
        self._birth[1] = int(month.props.value)

    def year_birth_change(self, year, value):
        self._birth[2] = int(year.props.value)

    # TODAY
    def day_today_change(self, day, value):
        self._today[0] = int(day.props.value)

    def month_today_change(self, month, value):
        self._today[1] = int(month.props.value)

    def year_today_change(self, year, value):
        self._today[2] = int(year.props.value)



