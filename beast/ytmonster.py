import time
import sys
from json import loads
from requests import Session
from sys import stdout

class YTMonster(object):

  def __init__(self):
    self.session = Session()
    self.online = False
    self.limit = 1000
    self.username = None

  def login(self, username, password):
    payload = { "usernames" : username, "passwords" : password, "submit" : "" }
    self.session.get("http://www.ytmonster.net/login")
    login = self.session.post("http://www.ytmonster.net/login?login=ok", data = payload)
    source = login.text.encode(stdout.encoding, errors="replace")
    if b"<a href=\"/logout\">Sign out</a>" in source:
      self.username = username
      print("User '" + username + "' has been logged in.")
      self.session.headers.update({ 'referer' : "http://www.ytmonster.net/client/" + username })
      self.online = True
    else:
      print("User '" + username + "' failed to login with the credentials specified.")
      self.online = False

  def logout(self):
    self.session.get("http://www.ytmonster.net/logout")
    print("Successfully logged out user '" + self.username + "'.")

  def get_stats(self):
    payload = { "username" : self.username }
    gUserStats = self.session.get("http://www.ytmonster.net/data/api3.php", params = payload)
    rUserStats = gUserStats.text.encode(stdout.encoding, errors="replace")
    return loads(rUserStats.decode("utf-8"))

  def is_online(self):
    return self.online
    
  def watch_video(self, id, seconds):
    time.sleep(int(seconds) + 1)
    payload = { "username" : self.username, "mark" : id }
    gWatchedVideo = self.session.get("http://www.ytmonster.net/watch3.php", params = payload)
    if b"Watched video successfully." in gWatchedVideo.text.encode(stdout.encoding, errors="replace"):
      return True
    else:
      for i in range(2):
        time.sleep(5)
        gWatchedVideo = self.session.get("http://www.ytmonster.net/watch3.php", params = payload)
        if b"Watched video successfully." in gWatchedVideo.text.encode(stdout.encoding, errors="replace"):
          return True
      return False

  def get_video(self):
    payload = { "username" : self.username }
    gNextVideo = self.session.get("http://www.ytmonster.net/watch4.php", params = payload)
    rNextVideo = gNextVideo.text.encode(stdout.encoding, errors="replace")
    if b"http://www.ytmonster.net/refDo.php?url=" in rNextVideo:
      self.session.get(rNextVideo)
      rVideoArgs = rNextVideo.split(b'watch?v=')[1]
      return rVideoArgs.split(b'#')
    elif b"Already watched." in rNextVideo:
      #print("Video given has already been seen.")
      return 0
    else:
      print("Error when attempting to get the next video.")
    return 0

  def set_limit(self, limit):
    self.limit = int(limit)

  def start(self, videos = 1):
    payload = { "username" : self.username }
    current = 0
    self.session.get("http://www.ytmonster.net/waitTime.php")
    self.session.get("http://www.ytmonster.net/wComment3.php", params = payload)
    self.session.get("http://www.ytmonster.net/wSubscribe3.php", params = payload)
    self.session.get("http://www.ytmonster.net/wLike3.php", params = payload)
    while current < videos:
      nextVid = self.get_video()
      if nextVid != 0:
        if int(nextVid[1]) <= self.limit:
          print("Watching " + nextVid[0].decode("utf-8") + " for " + nextVid[1].decode("utf-8") + "s... ", end="")
          sys.stdout.flush()
          if self.watch_video(nextVid[0], nextVid[1]):
            current += 1
            print("Success (" + str(current) + "/" + str(videos) + ")")
            if current % 5 == 0:
              print("'" + self.username + "' currently has " + self.get_stats()['credits'] + ".")
          else:
            print("Failed")