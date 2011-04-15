import string

PLUGIN_PREFIX = "/video/HDTrailers"
TOP_10 = "http://www.hd-trailers.net/TopMovies/"
LATEST = "http://www.hd-trailers.net/Page/"
LIBRARY = "http://www.hd-trailers.net/PosterLibrary/"
OPENING = "http://www.hd-trailers.net/OpeningThisWeek/"
COMING_SOON = "http://www.hd-trailers.net/ComingSoon/"
BLU_RAY = "http://www.hd-trailers.net/BluRay/"
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
  DirectoryItem.thumb = R("icon-default.png")
  HTTP.CacheTime = CACHE_TIME
####################################################################################################

def MainMenu():
  dir = MediaContainer()
  dir.Append(Function(DirectoryItem(TopTen, "Top 10")))
  dir.Append(Function(DirectoryItem(Latest, "Latest")))
  dir.Append(Function(DirectoryItem(Opening, "Opening")))
  dir.Append(Function(DirectoryItem(ComingSoon, "Coming Soon")))
  dir.Append(Function(DirectoryItem(BluRay, "Blu-Ray")))
  dir.Append(Function(DirectoryItem(Library, "Library")))
  dir.Append(PrefsItem("Preferences...", thumb=R('icon-prefs.png')))
  dir.Append(Function(DirectoryItem(about, 'About', thumb=R('icon-about.png'))))
  return dir
  
def TopTen(sender):
  return Videos(sender, TOP_10)
  
def Opening(sender):
  return Videos(sender, OPENING)
  
def ComingSoon(sender):
  return Videos(sender, COMING_SOON)
  
def BluRay(sender):
  return Videos(sender, BLU_RAY)
  
def Latest(sender, page=1):
  dir = Videos(sender, LATEST + str(page))
  dir.Append(Function(DirectoryItem(Latest, "More ..."), page=page+1))
  return dir
  
def Library(sender):
  dir = MediaContainer()
  for page in list(string.uppercase):
      dir.Append(Function(DirectoryItem(Videos, page), pageUrl=LIBRARY+page))
  return dir
  
def Videos(sender, pageUrl):
  dir = MediaContainer()
  for poster in HTML.ElementFromURL(pageUrl).xpath('//td[@class="indexTableTrailerImage"]/a'):
    if len(poster.xpath('./img')) > 0:
       url = BASE + poster.get('href')
       thumb = poster.xpath('./img')[0].get('src')
       title = poster.xpath('./img')[0].get('alt')
       dir.Append(Function(PopupDirectoryItem(VideosMenu, title=title, thumb=thumb), url=url))
  dir.Append(Function(DirectoryItem(about, 'About', thumb=R('icon-about.png'))))
  return dir


def about(sender):
  return MessageContainer(header='About', message='Icon and Code by Ryan McNally. Art by jpmatth on flicker http://www.flickr.com/photos/jpmatth/979337931/', title1='title1', title2='title2')

def VideosMenu(sender, url):
  dir = MediaContainer(title2=sender.itemTitle)
  defaultRes = Prefs['resolution']
  content = HTML.ElementFromURL(url)
  for row in content.xpath('//table[@class="bottomTable"]//tr'):
	      baseTitleItems = row.xpath('./td[@class="bottomTableName"]')
	      baseTitle = None
	      if len(baseTitleItems) > 0:
	      	baseTitle = baseTitleItems[0].xpath('./span')[0].text
	      Log(baseTitle)
	      if baseTitle != None:
	        for res in row.xpath('./td[@class="bottomTableResolution"]/a'):
	           resTitle = res.text
	           videoUrl = res.get('href')
	           include = True
	           if videoUrl.startswith("http://movies.apple.com") and Prefs["exclude.apple"]:
	              include = False
	           if videoUrl.startswith("http://trailers.apple.com") and Prefs["exclude.apple"]:
	              include = False
	           if include and (defaultRes == 'Prompt' or defaultRes == resTitle):
	              Log("Video URL:"+resTitle+":"+videoUrl)
	              dir.Append(VideoItem(videoUrl, title='%s %s' % (baseTitle, resTitle)))
          	   
  return dir

