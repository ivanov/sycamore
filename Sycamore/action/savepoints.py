# Imports
import time, string, os
import xml.dom.minidom
from Sycamore import config, user, util, wikiutil, mapping
from Sycamore.Page import Page

def clean(text):
	text=text.replace('\x85','&#8230;') # elipsis
	text=text.replace('\x91','&#8216;') # opening single quote
	text=text.replace('\x92','&#8217;') # closing single quote
	text=text.replace('\x93','&#8220;') # opening double quote
	text=text.replace('\x94','&#8221;') # closing double quote
	text=text.replace('\x96','&#8211;') # en-dash
	text=text.replace('\x97','&#8212;') # em-dash
	return text

def execute(pagename, request):
    actname = __name__.split('.')[-1]

    request.http_headers()

    if not request.form.has_key('name'):
      request.write('Error: no name');
      raise util.SycamoreNoFooter
    if not request.form.has_key('xml'):
      request.write('Error: no xml')
      raise util.SycamoreNoFooter
    findName = request.form.get("name")[0]
    
    # be extra paranoid
    page = Page(pagename, request)
    if not request.user.may.edit(page):
      request.write('You may not edit this page.')
      return
                    
    changes_xml = request.form.get("xml")[0]

    dom = xml.dom.minidom.parseString(changes_xml)
    # we need to convert it to the proper map xml format
    mapPoints = mapping.convert_xml(dom)
	
    mapping.update_points(mapPoints, request, pagename=pagename)

    request.write('Your map changes have been saved.')
    return 