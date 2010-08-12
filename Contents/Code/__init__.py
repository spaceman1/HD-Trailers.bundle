from PMS import *

import string

PLUGIN_PREFIX = "/video/HDTrailers"
ROOT = "http://www.hd-trailers.net/indexAll.php?displayType=poster&sortBy="
BASE = "http://www.hd-trailers.net"

CACHE_TIME = 3600


# art-default from:
#<div xmlns:cc="http://creativecommons.org/ns#" about="http://www.flickr.com/photos/jpmatth/979337931/"><a rel="cc:attributionURL" href="http://www.flickr.com/photos/jpmatth/">http://www.flickr.com/photos/jpmatth/</a> / <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/2.0/">CC BY-NC-ND 2.0</a></div>
# settings icon from Oxygen

####################################################################################################
def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, "HD Trailers.net", "icon-default.png", "art-default.jpg")
  MediaContainer.title1 = L('HD Trailers.net')
  MediaContainer.art = R('art-default.jpg')
  HTTP.SetCacheTime(CACHE_TIME)
####################################################################################################

def CreatePrefs():
  Prefs.Add(id='sort', type='enum', default='Name', label='Sort by', values='Name|Date')
  Prefs.Add(id='res', type='enum', default='480p', label='Default resolution', values='480p|720p|1080p|Prompt')
  Prefs.Add(id='filter.apple', type='bool', default=True, label='Exclude Apple Trailers')

def MainMenu():
  dir = MediaContainer()
  sort = Prefs.Get('sort').lower()
  Log("Root:"+ROOT+sort)
  for poster in XML.ElementFromURL(ROOT + sort, True).xpath('//td[@class="indexTableTrailerImage"]/a'):
    url = BASE + poster.get('href')
    thumb = poster.xpath('./img')[0].get('src')
    title = poster.xpath('./img')[0].get('alt')
    dir.Append(Function(PopupDirectoryItem(VideosMenu, title=title, thumb=thumb), url=url))
  dir.Append(Function(DirectoryItem(about, 'About', thumb=R('icon-about.png'))))
  dir.Append(PrefsItem(title="Preferences", thumb=R('gear.png')))
  return dir

def about(sender):
  return MessageContainer(header='About', message='Icon and Code by Ryan McNally. Art by jpmatth on flicker http://www.flickr.com/photos/jpmatth/979337931/', title1='title1', title2='title2')

def VideosMenu(sender, url):
  dir = MediaContainer(title2=sender.itemTitle)
  defaultRes = Prefs.Get('res')
  content = XML.ElementFromURL(url, True)
  for row in content.xpath('//table[@class="bottomTable"]//tr'):
      
      baseTitleItems = row.xpath('./td[@class="bottomTableName"]')
      baseTitle = None
      if len(baseTitleItems) > 0:
      	baseTitle = baseTitleItems[0].text
      if baseTitle != None:
        for res in row.xpath('./td[@class="bottomTableResolution"]/a'):
           resTitle = res.text
           url = res.get('href')
           include = True
           if url.startswith("http://movies.apple.com") and Prefs.Get("filter.apple"):
              include = False
           if include and (defaultRes == 'Prompt' or defaultRes == resTitle):
              dir.Append(VideoItem(url, title='%s %s' % (baseTitle, resTitle)))
          	   
  return dir

