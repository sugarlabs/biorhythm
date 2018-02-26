#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Gtk

from gi.repository import Pango as pango
from gi.repository import PangoCairo as pangocairo

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.activity.widgets import StopButton
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.graphics import style

from math import sin
from datetime import date
from datetime import datetime

from gettext import gettext as _

class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.max_participants = 1

        self.days = []
        self.days.append(31)
        self.days.append(28)
        self.days.append(31)
        self.days.append(30)
        self.days.append(31)
        self.days.append(30)
        self.days.append(31)
        self.days.append(31)
        self.days.append(30)
        self.days.append(31)
        self.days.append(30)
        self.days.append(31)

        self._now = datetime.now()

        if "birth" in self.metadata:
            birth = self.metadata["birth"].split("/")
            self._birth = map(int, birth)
        else:
            self._birth = [1, 1, 2010]
        self._today = [self._now.day, self._now.month, self._now.year]
        self._bio = [1, 1, 1]

        self.build_toolbar()

        self._biorhythm = Biorhythm(self)
        self.set_canvas(self._biorhythm)

        self.show_all()

        #'alto', 'critico', 'bajo'

    def build_toolbar(self):

        toolbox = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbox.toolbar.insert(activity_button, -1)
        activity_button.show()

        self.build_birth_toolbar(toolbox)
        self.build_today_toolbar(toolbox)

        separador13 = Gtk.SeparatorToolItem()
        separador13.props.draw = False
        separador13.set_expand(True)
        toolbox.toolbar.insert(separador13, -1)

        stop_button = StopButton(self)
        stop_button.props.accelerator = _('<Ctrl>Q')
        toolbox.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbox)
        toolbox.show()

        self.show_all()

    def build_birth_toolbar(self, toolbox):

        birth_bar = Gtk.Toolbar()

        item1 = Gtk.ToolItem()
        self.label_birth = Gtk.Label()
        self.label_birth.set_text(_('Birth:') + ' ' + _('Day') + ' ')
        item1.add(self.label_birth)
        birth_bar.insert(item1, -1)

        item2 = Gtk.ToolItem()
        self.day_birth_spin = Gtk.SpinButton()
        self.day_birth_spin.set_range(1, 31)
        self.day_birth_spin.set_increments(1, 5)
        self.day_birth_spin.props.value = self._birth[0]
        self.day_birth_spin.connect('notify::value', self.day_birth_change)
        item2.add(self.day_birth_spin)
        birth_bar.insert(item2, -1)

        item3 = Gtk.ToolItem()
        self.label_birth_month = Gtk.Label()
        self.label_birth_month.set_text(' ' + _('Month') + ' ')
        item3.add(self.label_birth_month)
        birth_bar.insert(item3, -1)

        item4 = Gtk.ToolItem()
        self.month_birth_spin = Gtk.SpinButton()
        self.month_birth_spin.set_range(1, 12)
        self.month_birth_spin.set_increments(1, 4)
        self.month_birth_spin.props.value = self._birth[1]
        self.month_birth_spin.connect('notify::value', self.month_birth_change)
        item4.add(self.month_birth_spin)
        birth_bar.insert(item4, -1)

        item5 = Gtk.ToolItem()
        self.label_birth_year = Gtk.Label()
        self.label_birth_year.set_text(' ' + _('Year') + ' ')
        item5.add(self.label_birth_year)
        birth_bar.insert(item5, -1)

        item6 = Gtk.ToolItem()
        self.year_birth_spin = Gtk.SpinButton()
        self.year_birth_spin.set_range(1900, self._now.year)
        self.year_birth_spin.set_increments(1, 10)
        self.year_birth_spin.props.value = self._birth[2]
        self.year_birth_spin.connect('notify::value', self.year_birth_change)
        item6.add(self.year_birth_spin)
        birth_bar.insert(item6, -1)

        birth_bar.show_all()
        birth_button = ToolbarButton(label=_('Birth'),
                page=birth_bar,
                icon_name='write-date')
        toolbox.toolbar.insert(birth_button, -1)
        birth_button.show()

    def build_today_toolbar(self, toolbox):

        today_bar = Gtk.Toolbar()

        item1 = Gtk.ToolItem()
        self.label_today = Gtk.Label()
        self.label_today.set_text(_('Today:') + ' ' + _('Day') + ' ')
        item1.add(self.label_today)
        today_bar.insert(item1, -1)

        item2 = Gtk.ToolItem()
        self.day_today_spin = Gtk.SpinButton()
        self.day_today_spin.set_range(1, 31)
        self.day_today_spin.set_increments(1, 5)
        self.day_today_spin.props.value = self._today[0]
        self.day_today_spin.connect('notify::value', self.day_today_change)
        item2.add(self.day_today_spin)
        today_bar.insert(item2, -1)

        item3 = Gtk.ToolItem()
        self.label_today_month = Gtk.Label()
        self.label_today_month.set_text(' ' + _('Month') + ' ')
        item3.add(self.label_today_month)
        today_bar.insert(item3, -1)

        item4 = Gtk.ToolItem()
        self.month_today_spin = Gtk.SpinButton()
        self.month_today_spin.set_range(1, 12)
        self.month_today_spin.set_increments(1, 4)
        self.month_today_spin.props.value = self._today[1]
        self.month_today_spin.connect('notify::value', self.month_today_change)
        item4.add(self.month_today_spin)
        today_bar.insert(item4, -1)

        item5 = Gtk.ToolItem()
        self.label_today_year = Gtk.Label()
        self.label_today_year.set_text(' ' + _('Year') + ' ')
        item5.add(self.label_today_year)
        today_bar.insert(item5, -1)

        item6 = Gtk.ToolItem()
        self.year_today_spin = Gtk.SpinButton()
        self.year_today_spin.set_range(1900, self._now.year + 1)
        self.year_today_spin.set_increments(1, 10)
        self.year_today_spin.props.value = self._today[2]
        self.year_today_spin.connect('notify::value', self.year_today_change)
        item6.add(self.year_today_spin)
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
        self.adjust_day_birth()
        self.calculate_bio()

    def month_birth_change(self, month, value):
        self._birth[1] = int(month.props.value)
        self.adjust_day_birth()
        self.calculate_bio()

    def year_birth_change(self, year, value):
        self._birth[2] = int(year.props.value)
        self.adjust_day_birth()
        self.calculate_bio()

    # TODAY
    def day_today_change(self, day, value):
        self._today[0] = int(day.props.value)
        self.adjust_day_today()
        self.calculate_bio()

    def month_today_change(self, month, value):
        self._today[1] = int(month.props.value)
        self.adjust_day_today()
        self.calculate_bio()

    def year_today_change(self, year, value):
        self._today[2] = int(year.props.value)
        self.adjust_day_today()
        self.calculate_bio()

    def calculate_bio(self):
        self._bio = self._biorhythm.calc()
        self.queue_draw()

    def _is_leap(self, year):
        return (year % 4 == 0 and not year % 100 == 0) or year % 400 == 0

    def adjust_day_birth(self):
        leap = 0

        if (self._birth[1] == 2) and self._is_leap(self._birth[2]):
            leap = 1

        d = self.days[self._birth[1] - 1] + leap

        if self._birth[0] > d:
            self.day_birth_spin.props.value = d

    def adjust_day_today(self):
        leap = 0

        if (self._today[1] == 2) and self._is_leap(self._today[2]):
            leap = 1

        d = self.days[self._today[1] - 1] + leap

        if self._today[0] > d:
            self.day_today_spin.props.value = d

    def write_file(self, filepath):
        self.metadata["birth"] = "/".join(map(str, self._birth))


class Biorhythm(Gtk.DrawingArea):


    def __init__(self, parent):
        super(Biorhythm, self).__init__()

        self._parent = parent

        self.initialized = False

        self._time = datetime.now()
        self._bio = [1, 1, 1]

        self._active = False


        self._scale = 250
        self._line_width = 2


        self._COLOR_P = "#005FE4"
        self._COLOR_E = "#00B20D"
        self._COLOR_I = "#E6000A"
        self._COLOR_WHITE = "#FFFFFF"
        self._COLOR_BLACK = "#000000"

        # Gtk.Widget signals
        self.connect("draw", self._draw_cb)
        self.connect("size-allocate", self._size_allocate_cb)



    def calc(self):

        b = self._parent._birth
        t = self._parent._today

        birth = date(b[2], b[1], b[0])
        today = date(t[2], t[1], t[0])

        dif = today - birth

        # Physical cycle
        p = sin(2 * 3.14159 * dif.days / 23)

        # Emotional cycle
        e = sin(2 * 3.14159 * dif.days / 28)

        # Intellectual cycle
        i = sin(2 * 3.14159 * dif.days / 33)

        self._bio = (p, e, i)

        return self._bio


    def _draw_biorhythm(self, cr):
        self._draw_time_scale(cr)
        self._draw_time(cr)

    def _draw_time_scale(self, cr):

        p_length = int(self._bio[0] * self._scale)
        e_length = int(self._bio[1] * self._scale)
        i_length = int(self._bio[2] * self._scale)

        # Fill background
        width = 70
        x = self._center_x
        y = self._center_y

        cr.set_source_rgba(*style.Color(self._COLOR_WHITE).get_rgba())
        cr.rectangle(self._center_x-(width + 30)-35,
                     (self._center_y - self._scale-10),
                     3*width + 2*20 + 20,
                     self._scale*2+20)
        cr.fill()

        # Physical cycle
        cr.set_source_rgba(*style.Color(self._COLOR_P).get_rgba())
        cr.rectangle(x - (width + 20)-35, y, width, p_length)
        cr.fill()

        # Emotional cycle
        cr.set_source_rgba(*style.Color(self._COLOR_E).get_rgba())
        cr.rectangle(x-35, y, width, e_length)
        cr.fill()

        # Intellectual cycle
        cr.set_source_rgba(*style.Color(self._COLOR_I).get_rgba())
        cr.rectangle(x-35 + (width + 20), y, width, i_length)
        cr.fill()

    def _draw_time(self, cr):


        markup = _('<markup>\
<span lang="en" font_desc="Sans,Monospace Bold 12">\
<span foreground="#E6000A">%s</span></span></markup>')

        cr.set_source_rgba(*style.Color(self._COLOR_E).get_rgba())
        pango_layout = pangocairo.create_layout(cr)
        d = int(self._center_y + self._scale + 20)
        markup_f = markup % "Physical Emotional Intellectual"
        pango_layout.set_markup(markup_f)
        dx, dy = pango_layout.get_pixel_size()
        pango_layout.set_alignment(pango.Alignment.CENTER)
        cr.translate(self._center_x - dx / 2.0, d - dy / 2.0 + 5)
        pangocairo.show_layout(cr, pango_layout)

    def _draw_cb(self, widget, cr):
        self.calc()
        self._draw_biorhythm(cr)
        return True

    def _size_allocate_cb(self, widget, allocation):
        self._center_x = int(allocation.width / 2.0)
        self._center_y = int(allocation.height / 2.0)

    def _redraw_canvas(self):
        pass

    def _update_cb(self):
        pass

