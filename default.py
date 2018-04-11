# -*- coding: utf-8 -*-
#Библиотеки, които използват python и Kodi в тази приставка
import re
import sys
import os
import urllib
import urllib2
import base64
import xbmc, xbmcplugin,xbmcgui,xbmcaddon

#Място за дефиниране на константи, които ще се използват няколкократно из отделните модули
__addon_id__= 'plugin.video.arenabg'
__Addon = xbmcaddon.Addon(__addon_id__)
__settings__ = xbmcaddon.Addon(id='plugin.video.arenabg')
username = xbmcaddon.Addon().getSetting('settings_username')
password = xbmcaddon.Addon().getSetting('settings_password')
searchicon = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/search.png")
movies = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/movies.png")
series = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/series.png")
xxl = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/18icon.png")
nextico = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/next.png")
dirmov = base64.b64decode("aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vdHlwZToxL3N1YnRpdGxlczoxNy8=")
dirser = base64.b64decode("aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vdHlwZTo1NS9zdWJ0aXRsZXM6MTcv")
dirsea = base64.b64decode("aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vdGV4dDo=")
dirx = base64.b64decode("aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vdHlwZTo1Ni8=")
MozilaFirefoxV51 = base64.b64decode("QXJlbmFQTEFZLTEuMC4w")
basedir = base64.b64decode("aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vcGxheWVyLw==")
lenght = base64.b64decode("Lz90aW1lPTE1MTQ2Njc3NzU=")
dirmovhd = base64.b64decode('aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vc3VidGl0bGVzOjE3L2NhdGVnb3J5OjQ2Lw==')
arenabgtv = base64.b64decode('aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vc3VidGl0bGVzOjE3L2NhdGVnb3J5Ojcv')
xvid = base64.b64decode('aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vc3VidGl0bGVzOjE3L2NhdGVnb3J5Ojgv')
x264 = base64.b64decode('aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vc3VidGl0bGVzOjE3L2NhdGVnb3J5OjExLw==')
dokumentalni = base64.b64decode('aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vc3VidGl0bGVzOjE3L2NhdGVnb3J5OjE1Lw==')
hd = base64.b64decode('aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vc3VidGl0bGVzOjE3L2NhdGVnb3J5OjUzLw==')
x265 = base64.b64decode('aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vc3VidGl0bGVzOjE3L2NhdGVnb3J5OjU3Lw==')
serieshd = base64.b64decode('aHR0cHM6Ly9wbGF5ZXIuYXJlbmFiZy5jb20vc3VidGl0bGVzOjE3L2NhdGVnb3J5OjEwLw==')
player = xbmcaddon.Addon().getSetting('player')
xxx = xbmcaddon.Addon().getSetting('xxx')
if not username or not password or not __settings__:
        xbmcaddon.Addon().openSettings()
if xbmcaddon.Addon().getSetting('xxx') == 'true':
  xxx = True
else:
  xxx = False
MUA = 'Mozilla/5.0 (Linux; Android 5.0.2; bg-bg; SAMSUNG GT-I9195 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19' #За симулиране на заявка от мобилно устройство
UA = MozilaFirefoxV51 #За симулиране на заявка от  компютърен браузър


#Меню с директории в приставката
def CATEGORIES():
        addDir('Търсене на видео',dirsea,2,searchicon)
        addDir('Последно добавени',dirmov,1,movies)
        addDir('Филми HD',hd,1,movies)
        addDir('Филми HDTV',dirmovhd,1,movies)
        addDir('Филми ArenaBGTV',arenabgtv,1,movies)
        addDir('Филми Xvid',xvid,1,movies)
        addDir('Филми X264',x264,1,movies)
        addDir('Филми X264',x265,1,movies)
        addDir('Документални',dokumentalni,1,movies)
        addDir('Сериали',dirser,1,series)
        addDir('Сериали HD',serieshd,1,series)
        if xxx == True:
         addDir('ХХХ',dirx,1,xxl)
        #addDir('','',1,'')




#Разлистване видеата на първата подадена страница
def INDEXPAGES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()

        #Начало на обхождането
        br = 0 #Брояч на видеата в страницата - 24 за този сайт
        match = re.compile('alt="(.+?)"></a>\s+.*\s+.*\s+.*(https.+?jpg).*player..(\d+).*false.*">\s+\W(\w+.+\S)\s+.*\s+.*\s+.*\s+.*\s+.*\s+.*\s+.*\s+.*\W(\w+.\w+.\w+)\s+.*\s+.*\s+(\w+)').findall(data)
        for form,thumbnail,idmov,title,size,seed in match:
         desc = 'Формат: ' + form + ' ' + ',Брой сийдъри: ' + seed + ' ' + ',Размер: ' + size
         addLink(title,idmov,3,desc,thumbnail)
         br = br + 1
        if br == 25: #тогава имаме следваща страница и конструираме нейния адрес
            getpage=re.compile('<li class="active"><a href="(.+?)/page:(.+?)">').findall(data)
            for baseurl,page in getpage:
                newpage = int(page)+1
                url = baseurl + '/page:' + str(newpage)
                print 'URL OF THE NEXT PAGE IS' + url
                thumbnail = nextico
                addDir('следваща страница>>'+str(newpage),url,1,thumbnail)


#Търсачка
def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Търсачка')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
            searchText=searchText.replace(' ','+')
            searchurl = url + searchText
            searchurl = searchurl.encode('utf-8')
            #print 'SEARCHING:' + searchurl
            req = urllib2.Request(searchurl)
            req.add_header('User-Agent', UA)
            response = urllib2.urlopen(req)
            #print 'request page url:' + url
            data=response.read()
            response.close()
            br = 0
            match = re.compile('alt="(.+?)"></a>\s+.*\s+.*\s+.*(https.+?jpg).*player..(\d+).*false.*">\s+\W(\w+.+\S)').findall(data)
            for form,thumbnail,idmov,title in match:
             desc = 'ФОРМАТ:' + form
             addLink(title,idmov,3,desc,thumbnail)
             br = br + 1
        if br >= 22: #тогава имаме следваща страница и конструираме нейния адрес
            getpage=re.compile('<li class="active"><a href="(.+?)/page:(.+?)">').findall(data)
            for baseurl,page in getpage:
                newpage = int(page)+1
                url = baseurl + '/page:' + str(newpage)
                print 'URL OF THE NEXT PAGE IS' + url
                thumbnail = nextico
                addDir('следваща страница>>'+str(newpage),url,4,thumbnail)     
        else:
            addDir('Върнете се назад в главното меню за да продължите','','',"DefaultFolderBack.png")

#Зареждане на видео
def PLAY(name,url,iconimage):
       url = basedir + url + lenght
       req = urllib2.Request(url)
       req.add_header('User-Agent', UA)
       response = urllib2.urlopen(req)
       data=response.read()
       response.close()
       match = re.compile('peerflix..(.+?).,').findall(data)
       for link in match:
        print link
        link2 = urllib.quote_plus(link)
        if '0' in player:
         p = 'plugin://plugin.video.quasar/play?uri=%s' % (link)
        if '1' in player:
         p = 'plugin://plugin.video.yatp/?action=play&torrent=%s&file_index=dialog' % (link)
        if '2' in player:
         app      = 'rocks.turkeytorrent.player'
         intent   = 'android.intent.action.VIEW'
         dataType = ''
         dataURI  = link
         p = 'StartAndroidActivity("%s", "%s", "%s", "%s")' % (app, intent, dataType, dataURI)
         xbmc.executebuiltin(p)         
        if '3' in player:
         app      = 'com.torrent_player'
         intent   = 'android.intent.action.VIEW'
         dataType = ''
         dataURI  = link
         p = 'StartAndroidActivity("%s", "%s", "%s", "%s")' % (app, intent, dataType, dataURI)
         xbmc.executebuiltin(p) 
        if '4' in player:
         p = 'plugin://plugin.video.elementum/play?uri=%s' % (link)
        li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=p)
       try:
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
       except:
            xbmc.executebuiltin("Notification('Грешка','Видеото липсва на сървъра!')")

def NEXTSEARCH(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()
        br = 0
        match = re.compile('alt="(.+?)"></a>\s+.*\s+.*\s+.*(https.+?jpg).*player..(\d+).*false.*">\s+\W(\w+.+\S)').findall(data)
        for form,thumbnail,idmov,title in match:
         desc = 'ФОРМАТ:' + form
         addLink(title,idmov,3,desc,thumbnail)
         br = br + 1
        if br >= 18: #тогава имаме следваща страница и конструираме нейния адрес
         getpage=re.compile('<li class="active"><a href="(.+?)/page:(.+?)">').findall(data)
         for baseurl,page in getpage:
                newpage = int(page)+1
                url = baseurl + '/page:' + str(newpage)
                print 'URL OF THE NEXT PAGE IS' + url
                thumbnail = nextico
                addDir('следваща страница>>'+str(newpage),url,4,thumbnail) 




#Модул за добавяне на отделно заглавие и неговите атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addLink(name,url,mode,plot,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addLink2(name,url,mode):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok


#Модул за добавяне на отделна директория и нейните атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


#НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param







params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass


#Списък на отделните подпрограми/модули в тази приставка - трябва напълно да отговаря на кода отгоре
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
    
elif mode==1:
        print ""+url
        INDEXPAGES(url)

elif mode==2:
        print ""+url
        SEARCH(url)

elif mode==3:
        print ""+url
        PLAY(name,url,iconimage)

elif mode==4:
        print ""+url
        NEXTSEARCH(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
