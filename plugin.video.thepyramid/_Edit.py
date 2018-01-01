import xbmcaddon, base64

Decode = base64.decodestring
MainBase = (Decode('aHR0cDovL3N1cHJlbWFjeS5vcmcudWsvdG9tYnJhaWRlci9weXJhbWlkL2hvbWUudHh0'))
addon = xbmcaddon.Addon('plugin.video.thepyramid')