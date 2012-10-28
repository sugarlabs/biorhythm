#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys


import gobject
gobject.threads_init()

import pygtk
import gtk
from gtk import gdk

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.graphics.toolbutton import ToolButton
from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton
from sugar.graphics.toolbarbox import ToolbarButton

from sugar.graphics import style
import pango
import gst
import cairo
import pangocairo

from math import sin
from datetime import date

from datetime import datetime

from gettext import gettext as _

class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.max_participants = 1
        self._now = datetime.now()

        self._birth = [31, 12, 2011]
        self._today = [self._now.day, self._now.month, self._now.year]
        self._bio = [1, 1, 1]

        self.build_toolbar()
        self._make_display()
        self.show_all()

        
        #self.calculate_bio()

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
        self.day_spin.props.value = self._today[0]
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
        self.month_spin.props.value = self._today[1]
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
        self.year_spin.props.value = self._today[2]
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
        self.calculate_bio()

    def month_birth_change(self, month, value):
        self._birth[1] = int(month.props.value)
        self.calculate_bio()

    def year_birth_change(self, year, value):
        self._birth[2] = int(year.props.value)
        self.calculate_bio()

    # TODAY
    def day_today_change(self, day, value):
        self._today[0] = int(day.props.value)
        self.calculate_bio()

    def month_today_change(self, month, value):
        self._today[1] = int(month.props.value)
        self.calculate_bio()

    def year_today_change(self, year, value):
        self._today[2] = int(year.props.value)
        self.calculate_bio()

    def calculate_bio(self):
        birth = date(self._birth[2], self._birth[1], self._birth[0])
        bio = date(self._today[2], self._today[1], self._today[0])
        self._bio = self._biorhytm.calc(birth, bio)
        self._biorhytm._draw_digital_clock()

    def _make_display(self):

        self._biorhytm = BiorhytmImage()

        # The label to print the time in full letters
        self._time_letters = gtk.Label()
        self._time_letters.set_no_show_all(True)

        self._time_letters.set_markup('holaaaaa')

        # The label to write the date
        self._date = gtk.Label()
        self._date.set_no_show_all(True)
        self._date.set_markup('pepe')

        # Put all these widgets in a vertical box
        vbox = gtk.VBox(False)
        vbox.pack_start(self._biorhytm, True)
        vbox.pack_start(self._time_letters, False)
        vbox.pack_start(self._date, False)

        # Attach the display to the activity
        self.set_canvas(vbox)


class BiorhytmImage(gtk.DrawingArea):


    def __init__(self):

        super(BiorhytmImage, self).__init__()

        # Set to True when the variables to draw the clock are set:
        self.initialized = False

        self._time = datetime.now()
        self._bio = [1, 1, 1]
        
        self._active = False


        self._scale = 200
        self._line_width = 2


        # XO Medium Blue
        self._COLOR_HOURS = "#005FE4"

        # XO Medium Green
        self._COLOR_MINUTES = "#00B20D"

        # XO Medium Red
        self._COLOR_SECONDS = "#E6000A"

        # White
        self._COLOR_WHITE = "#FFFFFF"

        # Black
        self._COLOR_BLACK = "#000000"

        # gtk.Widget signals
        self.connect("expose-event", self._expose_cb)
        self.connect("size-allocate", self._size_allocate_cb)


    def calc(self, birth, bio_date):

        dif = bio_date - birth

        NumbersDays = dif.days

        # Physical cycle
        p = sin(2 * 3.14159 * NumbersDays / 23)

        # Emotional cycle
        e = sin(2 * 3.14159 * NumbersDays / 28)

        # Intellectual cycle
        i = sin(2 * 3.14159 * NumbersDays / 33)

        #print 'bio', p, e, i
        self._bio = (p, e, i)
        return self._bio


    def _draw_digital_clock(self):
        self._draw_time_scale()
        #self._draw_time()

    def _draw_time_scale(self):

        p_length = int(self._bio[0] * self._scale)
        e_length = int(self._bio[1] * self._scale)
        i_length = int(self._bio[2] * self._scale)

        # Fill background
        cr = self.window.cairo_create()
        h = 50
        x = self._center_x
        y = self._center_y

        cr.set_source_rgba(*style.Color(self._COLOR_WHITE).get_rgba())
        cr.rectangle(self._center_x-85,
                     (self._center_y - self._scale-10),
                     220,
                     self._scale*2+20)
        cr.fill()



        # Physical cycle
        cr.set_source_rgba(*style.Color(self._COLOR_HOURS).get_rgba())
        cr.rectangle(x-70, y, h, p_length)
        cr.fill()

        # Emotional cycle
        cr.set_source_rgba(*style.Color(self._COLOR_MINUTES).get_rgba())
        cr.rectangle(x, y, h, e_length)
        cr.fill()

        # Intellectual cycle
        cr.set_source_rgba(*style.Color(self._COLOR_SECONDS).get_rgba())
        cr.rectangle(x + 70, y, h, i_length)
        cr.fill()

    def _draw_time(self):


        markup = _('<markup>\
<span lang="en" font_desc="Sans,Monospace Bold 64">\
<span foreground="#E6000A">%s</span></span></markup>')

        cr = self.window.cairo_create()
        cr = pangocairo.CairoContext(cr)
        cr.set_source_rgba(*style.Color(self._COLOR_BLACK).get_rgba())
        pango_layout = cr.create_layout()
        d = int(self._center_y + 0.3 * self._scale)
        markup = markup % "prueba2"

        pango_layout.set_markup(markup)
        dx, dy = pango_layout.get_pixel_size()
        pango_layout.set_alignment(pango.ALIGN_CENTER)
        cr.translate(self._center_x - dx / 2.0, d - dy / 2.0)
        cr.show_layout(pango_layout)

    def _expose_cb(self, widget, event):
        #self.queue_resize()
        self._draw_digital_clock()
        pass

    def _size_allocate_cb(self, widget, allocation):

        # Store the measures of the clock face widget
        self._center_x = int(allocation.width / 2.0)
        self._center_y = int(allocation.height / 2.0)

    def _redraw_canvas(self):
        #self.queue_draw()
        #self.window.process_updates(True)
        pass

    def _update_cb(self):
        # update the time and force a redraw of the clock
        self._time = datetime.now()

        #gobject.idle_add(self._redraw_canvas)
