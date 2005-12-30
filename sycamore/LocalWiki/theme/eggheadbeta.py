# -*- coding: iso-8859-1 -*-
"""
    LocalWiki default theme.  Base code copied from rightsidebar MoinMoin theme.
"""
from LocalWiki.Page import Page
from LocalWiki import config, wikiutil
from classic import Theme as ThemeBase
import string

class Theme(ThemeBase):
    """ here are the functions generating the html responsible for
        the look and feel of your wiki site
    """

    name = "eggheadbeta"
    showapplet = 0

    stylesheets_print = (
        # theme charset         media       basename
        (name,  'iso-8859-1',   'all',      'common'),
        (name,  'iso-8859-1',   'all',      'print'),
        )
    
    stylesheets = (
        # theme charset         media       basename
        (name,  'iso-8859-1',   'all',      'common'),
        (name,  'iso-8859-1',   'screen',   'screen'),
        (name,  'iso-8859-1',   'print',    'print'),
        )
    
    def __init__(self, request):
      ThemeBase.__init__(self, request)
      self.icons['www'] = ("[WWW]", "localwiki-www.png", 14, 11)


    # Header stuff #######################################################

    def banner(self,d):
        """
        Assemble the banner

        @rtype: string
        @return: banner html
        """
        if config.relative_dir: add_on = '/'
        else: add_on = ''

        if d['script_name']:
            html ='&nbsp;<a href="%(script_name)s">' % d
        else:
            html ='&nbsp;<a href="/' + config.relative_dir + add_on + 'Front_Page">' % d
        html = html + '<img align="middle" src="%s/%s" border=0></a>' % (config.web_dir, config.default_logo)
        return html

    def new_iconbar(self, d):
      return """<td valign="bottom">&nbsp;&nbsp;&nbsp;&nbsp;</td>
      	     %s
	     %s
	     %s
	     %s
	     """ % (self.editicon(d), self.infoicon(d), self.talkicon(d), self.mapicon(d))

    def editicon(self,d):
      editable = self.request.user.may.edit(d['page_name']) and d['page'].isWritable()
      if editable:
        return """<td style="font-size: 7pt;" align="center" valign="bottom">%s</a></td>""" % (wikiutil.link_tag_explicit('style="text-decoration: none;" onmouseover="a.hover"', self.request, wikiutil.quoteWikiname(d['page_name'])+'?action=edit',
	   '<img class="borderless" src="%s" hspace="8" width="24" height="24"/><p style="margin: 0; padding: 0;">Edit</p>'
	      % self.img_url('edit.png')))
      else:  return ''

    def infoicon(self, d):
       return """<td style="font-size: 7pt;" align="center" valign="bottom">%s</a></td>""" % (wikiutil.link_tag_explicit('style="text-decoration: none;" onmouseover="a.hover"', self.request, wikiutil.quoteWikiname(d['page_name'])+'?action=info',
	   '<img class="borderless" src="%s" hspace="8" width="24" height="24"/><p style="margin: 0; padding: 0;">Info</p>'
	      % self.img_url('info.png')))

    def is_talk_page(self, d):
       if len(d['page_name']) >= 5:
         if d['page_name'][len(d['page_name'])-5:] == '/Talk':
	   return True
       return False

    def talkicon(self, d):
      if config.talk_pages:
        if self.is_talk_page(d):
	   article_name = d['page_name'][:len(d['page_name'])-5]
	   return """<td style="font-size: 7pt;" align="center" valign="bottom">%s</a></td>""" % (wikiutil.link_tag_explicit('style="text-decoration: none;" onmouseover="a.hover"', self.request, wikiutil.quoteWikiname(article_name),
	   '<img class="borderless" src="%s" hspace="8" width="24" height="24"/><p style="margin: 0; padding: 0;">Article</p>'
	      % self.img_url('article.png')))
	else:
	  talk_page = Page(d['page_name']+'/Talk')
	  if talk_page.exists():
	    return """<td style="font-size: 7pt;" align="center" valign="bottom">%s</a></td>""" % (wikiutil.link_tag_explicit('style="text-decoration: none;" onmouseover="a.hover"', self.request, wikiutil.quoteWikiname(d['page_name'])+'/Talk',
	     '<img class="borderless" src="%s" hspace="8" width="24" height="24"/><p style="margin: 0; padding: 0;">Talk</p>'
	      % self.img_url('talk.png')))
	  else:
	    # if the viewer can't edit the talk page, let's spare them from looking at a useless link to an empty page:
	    if not self.request.user.may.edit(talk_page):
	      return ''
	    return """<td style="font-size: 7pt;" align="center" valign="bottom">%s</a></td>""" % (wikiutil.link_tag_explicit('class="tinyNonexistent" onmouseover="a.hover"', self.request, wikiutil.quoteWikiname(d['page_name'])+'/Talk',
	     '<img class="borderless" src="%s" hspace="8" width="24" height="24"/><p style="margin: 0; padding: 0;">Talk</p>'
	      % self.img_url('talk.png')))



    def mapicon(self, d):
      if self.showapplet:
        return """<td style="font-size: 7pt;" align="center" valign="bottom" id="show"><a href="#" style="text-decoration: none;" onmouseover="a.hover" onclick="doshow();"><img class="borderless" src="%s" hspace="8" width="24" height="24"/><p style="margin: 0; padding:0;">Map</p></a></td>
	          <td style="font-size: 7pt; display: none;" align="center" valign="bottom" id="hide"><a href="#" style="text-decoration: none;" onmouseover="a.hover" onclick="dohide();"><img class="borderless" src="%s" hspace="8" width="24" height="24"/><p style="margin: 0; padding:0;">Map</p></a></td>""" % (self.img_url('viewmap.png'), self.img_url('hidemap.png'))
      else: return ''


    def title(self, d):
        """
        Assemble the title
        
        @param d: parameter dictionary
        @rtype: string
        @return: title html
        """
        _ = self.request.getText
        html = []
        if d['title_link']:
            if d['polite_msg']:
                polite_html = '<div style="font-size: 10px; color: #404040; clear:both;">\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(%s)\
</div>' % d['polite_msg']
            else:
                polite_html = ''
            html.append('<h1 style="clear: none; float: left;"><a title="%s" href="%s">%s</a></h1>%s' % (
                _('Click here to do a full-text search for this title'),
                d['title_link'],
                wikiutil.escape(d['title_text']), polite_html))
	    html.append(self.new_iconbar(d))
	    
        else:
            html.append('<h1>%s</h1>' % wikiutil.escape(d['title_text']))
        return ''.join(html)

    def username(self, d):
        """
        Assemble the username / userprefs link
        
        @param d: parameter dictionary
        @rtype: string
        @return: username html
        """
        _ = self.request.getText
        html = []
        if config.relative_dir:
            relative_dir = '/' + config.relative_dir
        else:
            relative_dir = ''
        if self.request.user.valid:
            html.append('<div class="user"><table align="center" border="0" cellpadding="2"><tr><td>Welcome, ') 
           
            html.append('%s' % wikiutil.link_tag(self.request, self.request.user.name))
            html.append('<br />')
            html.append('</td></tr>')
            html.append('<form action="%s" method="POST">' % config.relative_dir)
            html.append('<input type="hidden" name="action" value="userform">')
            html.append('<input type="hidden" name="logout" value="Logout">')
            html.append('<tr><td align="right"><a href="%s/User Preferences"><img src="%s" class="actionButton"></a>' % (relative_dir, self.img_url('settings.png')))
            html.append('<br/><input type="image" name="Submit" value="Submit" src="%s" height="13" width="78" class="actionButton"></td></tr></table>' % self.img_url('logout.png'))
            html.append('</form></div>')
        else:
            html.append('<div class="user"><form action="%s/%s" method="POST">' % (relative_dir, d['page_name']))
            html.append('<input type="hidden" name="action" value="userform">')
            html.append('<table width="225" border="0" cellspacing="2" cellpadding="0">')
            html.append('<tr> <td width="50%" align="right" nowrap>User name:</td>')
            html.append('<td colspan="2" align="left" nowrap><input class="formfields" size="22" name="username" type="text">') 
            html.append('</td> </tr> <tr>')
            html.append('<td align="right">Password:</td>')
            html.append('<td colspan="2" align="left" nowrap> <input class="formfields" size="22" type="password" name="password"> ')
            html.append('<input type="hidden" name="login" value="Login">')
            html.append('</td></tr><tr><td></td><td align="left" nowrap><input type="image" src="%s" name="login" value="Login" class="actionButton"></td><td align="right"><a href="%s/User Preferences"><img src="%s" class="actionButton"></a></td></tr></table>' % (self.img_url('login.png'), relative_dir, self.img_url('newuser.png')))
            html.append('</form></div>')
        return ''.join(html)

    def navibar(self, d):
        """
        Assemble the navibar
        
        @param d: parameter dictionary
        @rtype: string
        @return: navibar html
        """
        _ = self.request.getText
        html = []
        html.append('<div class="sidetitle">%s</div>\n' % _("Site"))
        html.append('<ul id="navibar">\n')
        if d['navibar']:
            # Print site name in first field of navibar
            # html.append(('<li>%(site_name)s</li>\n') % d)
            for (link, navi_link) in d['navibar']:
                html.append((
                    '<li><a href="%(link)s">%(navi_link)s</a></li>\n') % {
                        'link': link,
                        'navi_link': navi_link,
                    })
        html.append('</ul>')
        return ''.join(html)

    def isEdit(self, d):
        """
	Are we in the page editing interface?
	"""
	if self.request.form.has_key('action') and self.request.form['action'][0] == 'edit':
	  return True
	else:
	  return False

    def isInfo(self, d):
        """
	Are we in the info interface?
	"""
	if self.request.form.has_key('action') and (self.request.form['action'][0] == 'info' or self.request.form['action'][0] == 'Files'):
	  return True
	else:
	  return False
        
    def navbar(self, d):
        """
        Assemble the new nav bar
        
        @param d: parameter dictionary
        @rtype: string
        @return: navibar html
        """
        _ = self.request.getText
        front_class = "tab"
        recent_class = "tab"
        map_class = "tab"
        people_class = "tab"
        bookmarks_class = "tab"
        other_page_html = ""

	# so our formatting here looks nicer :)
        if config.relative_dir:
            d['relative_dir'] = '/' + config.relative_dir
        else:
            d['relative_dir'] = ''

        if d['page_name']:
            if d['page_name'] == "Front Page":
              front_class += ' activeTab'
            elif d['page_name'] == "Recent Changes":
              recent_class += ' activeTab'
            elif d['page_name'] == "Map":
              map_class += ' activeTab'
            elif d['page_name'] == "People":
              people_class += ' activeTab'
            elif d['page_name'] == "Bookmarks" and self.request.user.valid:
              bookmarks_class += ' activeTab'
            else:
              other_page_html = '<a href="%(relative_dir)s/%(q_page_name)s" class="tab activeTab">%(page_name)s</a>' % d
        

        dict = {
            'frontpage_class': front_class,
            'davismap_class': map_class,
            'recent_class': recent_class,
            'people_class': people_class,
            'bookmarks_class': bookmarks_class,
            'other_html': other_page_html
        }
        dict.update(d)
        
        
        if self.request.user.valid:
            html = """
<div class="tabArea">
<a href="%(relative_dir)s/Front_Page" class="%(frontpage_class)s">Front Page</a>
<a href="%(relative_dir)s/Map" class="%(davismap_class)s">Map</a>
<a href="%(relative_dir)s/People" class="%(people_class)s">People</a>
<a href="%(relative_dir)s/Bookmarks" class="%(bookmarks_class)s">Bookmarks</a>
<a href="%(relative_dir)s/Recent_Changes" class="%(recent_class)s">Recent Changes</a>
%(other_html)s
</div>
""" % dict
        else:
            html = """
<div class="tabArea">
<a href="%(relative_dir)s/Front_Page" class="%(frontpage_class)s">Front Page</a>
<a href="%(relative_dir)s/Map" class="%(davismap_class)s">Map</a>
<a href="%(relative_dir)s/People" class="%(people_class)s">People</a>
<a href="%(relative_dir)s/Recent_Changes" class="%(recent_class)s">Recent Changes</a>
%(other_html)s
</div>
""" % dict

        return ''.join(html)


    def make_iconlink(self, which, d, actionButton=False):
        """
        Make a link with an icon

        @param which: icon id (dictionary key)
        @param d: parameter dictionary
        @rtype: string
        @return: html link tag
        """
        page_params, title, icon = config.page_icons_table[which]
        d['title'] = title % d
        d['i18ntitle'] = self.request.getText(d['title'])
        img_src = self.make_icon(icon, d, actionButton)
        return wikiutil.link_tag(self.request, page_params % d, d['i18ntitle'], attrs='title="%(title)s"' % d)


    #def iconbar(self, d):
    #    """
    #    Assemble the iconbar
    #    
    #    @param d: parameter dictionary
    #    @rtype: string
    #    @return: iconbar html
    #    """
    #    _ = self.request.getText
    #    iconbar = []
    #    if config.page_iconbar and d['page_name']:
    #        iconbar.append('<div class="sidetitle">%s</div>\n' % _("Page"))
    #        iconbar.append('<ul id="iconbar">\n')
    #        icons = config.page_iconbar[:]
    #        for icon in icons:
    #            if icon == "up":
    #                if d['page_parent_page']:
    #                    iconbar.append('<li>%s</li>\n' % self.make_iconlink(icon, d))
    #            elif icon == "home":
    #                if d['page_home_page']:
    #                    iconbar.append('<li>%s</li>\n' % self.make_iconlink(icon, d))
    #            else:
    #                iconbar.append('<li>%s</li>\n' % self.make_iconlink(icon, d))
    #        iconbar.append('</ul>\n')
    #    return ''.join(iconbar)

    #def trail(self, d):
    #    """
    #    Assemble page trail
    #    
    #    @param d: parameter dictionary
    #    @rtype: string
    #    @return: trail html
    #    """
    #    html = []
    #    if d['trail']:
    #        pagetrail = d['trail']
    #        html.append('<ul id="pagetrail">\n')
    #        for p in pagetrail[:-1]:
    #            html.append('<li><span>%s</span></li>\n' % (Page(p).link_to(self.request),))
    #        html.append('<li><span>%s</span></li>\n' % wikiutil.escape(pagetrail[-1]))
    #        html.append('</ul>\n')
    #    else:
    #        html.append('<!-- pagetrail would be here -->\n')
#   #        html.append('<hr id="pagetrail">\n')
    #    return ''.join(html)

    #def edittexthead_link(self, d, **keywords):

    #    _ = self.request.getText
    #    html = []
    #    if keywords.get('editable', 1):
    #            if d['page_name']:
    #                editable = self.request.user.may.edit(d['page_name']) and d['page'].isWritable()
    #                if editable:
    #                  style = 'pageIcon'
    #                  html.append("%s" % (wikiutil.link_tag_style(style, self.request, d['q_page_name']+'?action=edit', _('Edit'))))
    #    return ''.join(html)
        
    def edittext_link(self, d, **keywords):
        """
        Assemble EditText link (or indication that page cannot be edited)
        
        @param d: parameter dictionary
        @rtype: string
        @return: edittext link html
        """
        _ = self.request.getText
        html = []
        if keywords.get('editable', 1):
            editable = self.request.user.may.edit(d['page_name']) and d['page'].isWritable()
            html.append('<script language="JavaScript">\nvar donate2=new Image();donate2.src="%s";var donate=new Image();donate.src="%s";</script>' % (self.img_url('donate2.png'), self.img_url('donate.png')))
            html.append('<div id="footer">')
            html.append('<table width="100%%" border="0" cellspacing="0" cellpadding="0"><tr>')
	    # noedit is a keyword that tells us if we are in an area where an edit link just logically makes no sense, such as the info tab.
	    if not keywords.get('noedit'):
	     html.append('<td align="left" width="50%%">')
             if editable:
                 html.append("%s" % (
                     wikiutil.link_tag(self.request, d['q_page_name']+'?action=edit', _('Edit'))))
                 html.append(' this page')
                 html.append(' %(last_edit_info)s </div>' % d)
             else :
               html.append('Most pages are editable.  Please login to edit and add comments.</div>')
	
	    # if editing doesnt make sense then we have more room for the license note
	    if not keywords.get('noedit'):
              license_text = """
<!-- Creative Commons Licence --><font style="font-size:9px;">Except where otherwise noted, this content is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/2.0/">Creative Commons License</a>.  See %s.</font><!-- /Creative Commons License --><!--  <rdf:RDF xmlns="http://web.resource.org/cc/" xmlns:dc="http://purl.org/dc/elements/1.1/"     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <Work rdf:about=""><dc:type rdf:resource="http://purl.org/dc/dcmitype/Text" /><license rdf:resource="http://creativecommons.org/licenses/by/2.0/" /> </Work>  <License rdf:about="http://creativecommons.org/licenses/by/2.0/"> <permits rdf:resource="http://web.resource.org/cc/Reproduction" /> <permits rdf:resource="http://web.resource.org/cc/Distribution" /> <requires rdf:resource="http://web.resource.org/cc/Notice" /> <requires rdf:resource="http://web.resource.org/cc/Attribution" /> <permits rdf:resource="http://web.resource.org/cc/DerivativeWorks" /> </License>  </rdf:RDF>  -->
""" % (Page("Copyrights").link_to(self.request))
	    else:
	      license_text = """
<!-- Creative Commons Licence --><font style="font-size:9px;">Except where otherwise noted, this content is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/2.0/">Creative Commons License</a>.  See %s.</font><!-- /Creative Commons License --><!--  <rdf:RDF xmlns="http://web.resource.org/cc/" xmlns:dc="http://purl.org/dc/elements/1.1/"     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <Work rdf:about=""><dc:type rdf:resource="http://purl.org/dc/dcmitype/Text" /><license rdf:resource="http://creativecommons.org/licenses/by/2.0/" /> </Work>  <License rdf:about="http://creativecommons.org/licenses/by/2.0/"> <permits rdf:resource="http://web.resource.org/cc/Reproduction" /> <permits rdf:resource="http://web.resource.org/cc/Distribution" /> <requires rdf:resource="http://web.resource.org/cc/Notice" /> <requires rdf:resource="http://web.resource.org/cc/Attribution" /> <permits rdf:resource="http://web.resource.org/cc/DerivativeWorks" /> </License>  </rdf:RDF>  -->
""" % (Page("Copyrights").link_to(self.request))

	
            cc_button = '<a href="http://creativecommons.org/licenses/by/2.0/"><img alt="Creative Commons License" border="0" src="%s"/></a>' % self.img_url('cc.png')
            html.append('</td><td align="center" valign="middle">%s</td><td align="center" valign="middle" width="190px">%s %s</td></tr></table></div>' % (license_text, cc_button, wikiutil.link_tag(self.request, 'Donate', _('<img name="rollover" onMouseOver="document.rollover.src=donate2.src;" onMouseOut="document.rollover.src=donate.src;" src="%s" border="0"/>' % self.img_url('donate.png')))))
            html.append('<br/>')
        return ''.join(html)
        
    #def info_link(self, d):
    #    """
    #    Assemble InfoLink link
    #    
    #    @param d: parameter dictionary
    #    @rtype: string
    #    @return: info link html
    #    """
    #    _ = self.request.getText
    #    html = []
    #    if d['q_page_name']:
    #      style = 'pageIcon'
    #      if string.lower(d['title_text']).startswith('info for "') or string.lower(d['title_text']).startswith('image "') or string.lower(d['title_text']).startswith('images for "') or string.lower(d['title_text']).startswith('deleted images for "'):
    #        style += ' pageIconActive'
    #      html.append("%s" % (wikiutil.link_tag_style(style, self.request, d['q_page_name']+'?action=info', _('Info'))))

    #    return ''.join(html)
        
    def html_head(self, d):
        """
        Assemble html head
        
        @param d: parameter dictionary
        @rtype: string
        @return: html head
        """
        dict = {
            'stylesheets_html': self.html_stylesheets(d),
        }
        dict.update(d)
        dict['newtitle'] = None
        dict['newtitle'] = dict['title']
        if dict['title'] == 'Front Page':
            dict['newtitle'] = config.catchphrase
	dict['web_dir'] = config.web_dir
	if dict['newtitle'] is config.catchphrase: 
        	html = """
<title>%(sitename)s - %(newtitle)s</title><SCRIPT 
SRC="%(web_dir)s/utils.js"></SCRIPT>
%(stylesheets_html)s
		""" % dict
	else:
                html = """
<title>%(newtitle)s - %(sitename)s</title><SCRIPT 
SRC="%(web_dir)s/utils.js"></SCRIPT>
%(stylesheets_html)s
                """ % dict	

        return html

    def header(self, d):
        """
        Assemble page header
        
        @param d: parameter dictionary
        @rtype: string
        @return: page header html
        """
        title_str = '"%s"' %  d['title_text']
	if d['page_name'] and d['page'].hasMapPoints() and not self.isEdit(d):
           self.showapplet = True
        apphtml = ""
        if self.showapplet:
           relative_dir = ''
           if config.relative_dir:
               relative_dir = '/' + config.relative_dir
           apphtml = '<table id="map" width="810" height="460" style="display: none; margin-top: -1px;" border="0" cellpadding="0" cellspacing="0"><tr><td bgcolor="#ccddff" style="border-right: 1px dashed #aaaaaa; border-bottom: 1px dashed #aaaaaa;"><applet code="WikiMap.class" archive="%s/map.jar, %s/txp.jar" height=460 width=810 border="1"><param name="map" value="%s/map.xml"><param name="points" value="%s/Map?action=mapPointsXML"><param name="highlight" value="%s"><param name="wiki" value="%s">You do not have Java enabled.</applet></td></tr></table>' % (config.web_dir, config.web_dir, config.web_dir, relative_dir, d['title_text'], relative_dir)
        dict = {
            'config_header1_html': self.emit_custom_html(config.page_header1),
            'config_header2_html': self.emit_custom_html(config.page_header2),
            # 'logo_html':  self.logo(d),
            'banner_html': self.banner(d),
            'title_html':  self.title(d),
            'username_html':  self.username(d),
            'navbar_html': self.navbar(d),
            'iconbar_html': self.iconbar(d),
            'msg_html': self.msg(d),
            'search_form_html': self.searchform(d),
            'applet_html': apphtml,
        }
        dict.update(d)

# %(logo_html)s ### from...
        html = """
%(config_header1_html)s
<div id="banner">
<table width="100%%" border="0" cellspacing="0" cellpadding="0">
<tr height="40">
<td>
%(banner_html)s
</td>
<td valign="top" width="230">
%(username_html)s
</td>
</tr>
</table>
%(navbar_html)s
</div>
<div id="title">
<table width="100%%" valign="middle" border="0" cellspacing="0" cellpadding="0">
<tr valign="middle"><td height="40" nowrap>
%(title_html)s
</td>
<td width="100%%" align="right">
<p>
%(search_form_html)s
</p>
</td></tr></table></div>
%(config_header2_html)s
%(applet_html)s
%(msg_html)s
""" % dict
        # Next parts will use config.default_lang direction, as set in the <body>
        return html

    # Footer stuff #######################################################
    
    def searchform(self, d):
        """
        assemble HTML code for the search forms
        
        @param d: parameter dictionary
        @rtype: string
        @return: search form html
        """
        _ = self.request.getText
        sitenav_pagename = wikiutil.getSysPage(self.request, 'SiteNavigation').page_name
        dict = {
            'search_title': _("Search"),
            'search_html': _("Search: %(textsearch)s&nbsp;&nbsp;") % d,
        }
        dict.update(d)
        
        html = """
<form method="POST" action="%(script_name)s/%(q_page_name)s">
<input type="hidden" name="action" value="inlinesearch">
<input type="hidden" name="context" value="40">
<input type="hidden" name="button_new.x" value="0">
%(search_html)s
</form>
""" % dict

        return html

    #def availableactions(self, d):    
    #    """
    #    assemble HTML code for the available actions
    #    
    #    @param d: parameter dictionary
    #    @rtype: string
    #    @return: available actions html
    #    """
    #    _ = self.request.getText
    #    html = []
    #    html.append('<div class="sidetitle">%s</div>\n' % _("Actions"))
    #    html.append('<ul id="actions">\n')
    #    for action in d['available_actions']:
    #        html.append("<li>%s</li>\n" % (
    #            wikiutil.link_tag(self.request, '%s?action=%s' % (d['q_page_name'], action), action)
    #        ))
    #    html.append('</ul>')
    #    return ''.join(html)

    def footer(self, d, **keywords):
        """
        Assemble page footer
        
        @param d: parameter dictionary
        @keyword ...:...
        @rtype: string
        @return: page footer html
        """
        dict = {
            'config_page_footer1_html': self.emit_custom_html(config.page_footer1),
            'config_page_footer2_html': self.emit_custom_html(config.page_footer2),
            'showtext_html': self.showtext_link(d, **keywords),
            'edittext_html': self.edittext_link(d, **keywords),
            'version_html': self.showversion(d, **keywords),
            'footer_fragments_html': self.footer_fragments(d, **keywords),
        }
        dict.update(d)
        
        html = """
%(edittext_html)s
%(version_html)s
""" % dict

        
	# I guess this is probably the best place for this now
	self.request.user.checkFavorites(d['page_name'])

        return html

def execute(request):
    """
    Generate and return a theme object
        
    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)
    
def is_word_in_file(file, word):
      """
      Pass me a file location and i tell you if word is in that file
      """
      f = open(file)
      lines = f.readlines()
      f.close()
      for line in lines:
         if string.find(line, word) >= 0:
            return 1
      return 0

