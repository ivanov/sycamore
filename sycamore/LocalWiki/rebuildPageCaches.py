import sys, cStringIO
sys.path.extend(['/usr/local/lib/python2.4/site-packages','/var/www/installhtml/dwiki'])
from LocalWiki import wikiutil, config, request, caching, wikidb
from LocalWiki.Page import Page

db = wikidb.connect()
cursor = db.cursor()

def clearCaches():
  print "Clearing page caches..."
  plist = wikiutil.getPageList(cursor)
  arena = 'Page.py'
  for pname in plist:
    key = pname
    cache = caching.CacheEntry(arena, key)
    cache.clear()

def buildCaches():
  print "Building page caches...It is _normal_ for this to produce errors!"
  # this is hackish, but it will work
  # the idea is to view every page to build the cache
  # we should actually refactor send_page()
  req = request.RequestCGI(db)
  req.redirect(cStringIO.StringIO())
  for pname in wikiutil.getPageList():
   Page(pname, req.cursor).getPageLinks(req, docache=True)
  req.redirect()

clearCaches()
buildCaches()
cursor.close()
db.close()
