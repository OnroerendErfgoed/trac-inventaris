import urllib2

import json

from genshi.core import Markup
from genshi.builder import tag
from trac.core import *
from trac.wiki.api import IWikiMacroProvider
from trac.config import Option

class InventarisMacro(Component):

    implements(IWikiMacroProvider)

    """Leg een link naar de Inventaris Onroerend Erfgoed
    """

    revision = "$Rev$"
    url = "$URL$"


    proxy_url = Option('trac-inventaris', 'proxy_url', '')
    
    def expand_macro(self, formatter, name, text, args):
		proxy_support = urllib2.ProxyHandler({"https" : proxy_url})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
								    
		url = 'https://inventaris.onroerenderfgoed.be/erfgoed/node/%s' % (Markup.escape(text))
		req = urllib2.Request(url)
		req.add_header('Accept', 'application/json')
		r = urllib2.urlopen(req)
		data = json.load(r)
		link = tag.a(data['omschrijving'] + ' (' + data['id'] + ')',href=url)
		return link 

class InventarisZoekenMacro(Component):
    implements(IWikiMacroProvider)
    """Doorzoek de inventaris op basis van een query parameter.

    Deze simpele macro ontvangt een query parameter als argument, 
    voert de query uit en geeft de resultaten weer als een lijst.
    """

    revision = "$Rev$"
    url = "$URL$"
    proxy_url = Option('trac-inventaris', 'proxy_url', '')

    def expand_macro(self, formatter, name, text, args):
        proxy_support = urllib2.ProxyHandler({"https" : proxy_url})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
                                
        url = 'https://inventaris.onroerenderfgoed.be/erfgoed/node?query=%s' % (urllib2.quote(text))
        req = urllib2.Request(url)
        req.add_header('Accept', 'application/json')
        r = urllib2.urlopen(req)
        data = json.load(r)
        titel = tag.div(tag.b("Uw zoekopdracht: " + Markup.escape(text)))
        res = tag.em("Resultaten %d - %d van %d" % \
            (data['startIndex'], data['startIndex'] -1 + data['itemsPerPage'], data['totalResults']))
        def make_listitem(item):
            def filter_html_link(link):
                return link['type'] == 'text/html'
            url = filter(filter_html_link,item['links'])[0]['href']
            link = tag.a(item['omschrijving'] + ' (' + item['id'] + ')',href=url)
            return tag.li(link)
        lijst = tag.ul(map(make_listitem,data['items']))
        return titel + res + lijst
