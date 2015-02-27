import urllib
import urllib2


def audio_extract(input_text):
    if len(input_text) > 0:
        mp3url = "http://translate.google.com/translate_tts?tl=%s&q=%s" % ('en-us', urllib.quote(input_text), )
        headers = {
            "Host": "translate.google.com",
            "Referer": "http://www.gstatic.com/translate/sound_player2.swf",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) "
                          "AppleWebKit/535.19 (KHTML, like Gecko) "
                          "Chrome/18.0.1025.163 Safari/535.19"
        }
        req = urllib2.Request(mp3url, '', headers)
        try:
            return urllib2.urlopen(req)
        except urllib2.URLError as e:
            print ('%s' % e)
