# -*- coding: iso-8859-1 -*-
"""
    Sycamore - BR Macro

    This very complicated macro produces a line break.

    @copyright: 2000 by J�rgen Hermann <jh@web.de>
    @license: GNU GPL, see COPYING for details.
"""

from Sycamore.Page import Page

Dependencies = []

def execute(macro, args, formatter=None):
    if not formatter: formatter = macro.formatter
    return formatter.linebreak(0) + str(formatter.page)
