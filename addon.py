# -*- coding: utf-8 -*-
import urllib.request as urllib
import os
from re import compile as Compile
from xbmc import log,Player
from xbmcgui import Dialog,ListItem
from xbmcaddon import Addon
from xbmcvfs import translatePath
import routing
from xbmcplugin import addDirectoryItem, endOfDirectory
from settings import *

ADDON_PATH=ADDON_PATH = translatePath(Addon().getAddonInfo('path'))
TV_THUMBNAIL_DIR = os.path.join(ADDON_PATH, 'resources', 'media')

plugin = routing.Plugin()
opener=urllib.build_opener(urllib.HTTPHandler,urllib.HTTPRedirectHandler())
urllib.install_opener(opener)

@plugin.route('/')
def index():
    for tv in TV_LIST:
        icon=os.path.join(TV_THUMBNAIL_DIR, tv['thumbnail'])
        list_item = ListItem(tv['title'])
        list_item.setArt({'icon':icon})
        addDirectoryItem(plugin.handle, plugin.url_for(play_video,name=tv['title'],video=tv['url'],icon=icon), list_item, True)
    endOfDirectory(plugin.handle)
 
@plugin.route('/stream')
def play_video():
    url = plugin.args['video'][0]
    name = plugin.args['name'][0]
    icon = plugin.args['icon'][0]
    try:
        source=openUrl(url)
    except:
        source=None
    if  source:
        video_url = Compile('file:"(.+?)"').findall(source)[0]
        item = ListItem(name,'',video_url)
        item.setArt({'icon':icon})
        Player().play(video_url,item,False)
        Dialog().notification(name,'',icon,8000,sound=False)
    else:
        log('Error: missing video url')

def openUrl(url):
    req=urllib.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    req.add_header('Accept-Language','en-US,en;q=0.9')
    req.add_header('Cache-Control','no-cache')
    req.add_header('Pragma','no-cache')
    try:
        response=urllib.urlopen(req)
        source=response.read().decode('utf-8')
        response.close()
    except urllib.HTTPError as e:
        print('error %s' % e)
        source=e.read().decode('utf-8')
    return source

if __name__ == '__main__':
    plugin.run()