import time
import sys
from json import loads
from requests import Session
from sys import stdout

""" Channel """

class Channel(object):
  
  def __init__(self, client):
    self.client = client

  def subscribe(self):
    """ Returns whether or not a channel was successfully subscribed to. """
    payload = { "username" : self.client.get_username() }
    request = self.client.get_session().get("http://www.ytmonster.net/wSubscribe3.php", params = payload)
    source = request.text.encode(stdout.encoding, errors="replace")
  
""" Video """

class Video(object):

  def __init__(self, client):
    self.client = client
  
  def comment(self):
    """ Return whether or not a video was successfully commented on. """
    payload = { "username" : self.client.get_username() }
    request = self.client.get_session().get("http://www.ytmonster.net/wComment3.php", params = payload)
    source = request.text.encode(stdout.encoding, errors="replace")
    
  def like(self):
    """ Return whether or not a video was successfully liked. """
    payload = { "username" : self.client.get_username() }
    request = self.client.get_session().get("http://www.ytmonster.net/wLike3.php", params = payload)
    source = request.text.encode(stdout.encoding, errors="replace")
  
  def watch(self):
    """ Return whether or not a video was successfully considered watched. """
    payload = { "username" : self.client.get_username() }
    request = self.client.get_session().get("http://www.ytmonster.net/watch4.php", params = payload)
    source = request.text.encode(stdout.encoding, errors="replace")
    # Ensure a valid response was received.
    if b"http://www.ytmonster.net/refDo.php?url=" not in source:
      return False
    id = source.split(b'watch?v=')[1].split(b'#')[0].decode("utf-8")
    # Verify that the watch duration is not longer than the limit set.
    duration = int(source.split(b'watch?v=')[1].split(b'#')[1])
    if duration > self.client.get_limit():
      return False
    # Send a GET request to the URL the previous request returned.
    self.client.get_session().get(source)
    payload["mark"] = id
    # Simulate watching the video.
    print("Watching " + id + " for " + str(duration) + "s... ", end="")
    sys.stdout.flush()
    time.sleep(duration)
    # Check for success after telling the server the video was watched.
    finish = self.client.get_session().get("http://www.ytmonster.net/watch3.php", params = payload)
    if b"Watched video successfully." in finish.text.encode(stdout.encoding, errors="replace"):
      print("Succeeded")
      return True
    print("Failed")
    return False

""" YTMonster """

class YTMonster(object):

  def __init__(self):
    self.session = Session()
    self.online = False
    self.limit = 1000
    self.username = None

  def login(self, username, password):
    """ Return whether or not a user has successfully logged in. """
    payload = { "usernames" : username, "passwords" : password, "submit" : "" }
    self.session.get("http://www.ytmonster.net/login")
    login = self.session.post("http://www.ytmonster.net/login?login=ok", data = payload)
    source = login.text.encode(stdout.encoding, errors="replace")
    if b"<a href=\"/logout\">Sign out</a>" in source:
      self.username = username
      print("'" + username + "' has been logged in.")
      self.session.headers.update({ 'referer' : "http://www.ytmonster.net/client/" + username })
      self.online = True
    else:
      print("'" + username + "' failed to login with the credentials given.")
      self.online = False
    return self.online

  def logout(self):
    """ Return that a user has successfully logged out. """
    self.session.get("http://www.ytmonster.net/logout")
    self.session.headers.update({ 'referer' : None })
    self.online = False
    print("Successfully logged out '" + self.username + "'.")
    return True

  def get_limit(self):
    return self.limit

  def get_session(self):
    return self.session

  def get_stats(self):
    """ Return a JSON object of the user statistics. """
    payload = { "username" : self.username }
    gUserStats = self.session.get("http://www.ytmonster.net/data/api3.php", params = payload)
    rUserStats = gUserStats.text.encode(stdout.encoding, errors="replace")
    return loads(rUserStats.decode("utf-8"))
  
  def get_username(self):
    return self.username
    
  def is_online(self):
    return self.online

  def set_limit(self, limit):
    self.limit = int(limit)

  def show_points(self):
    print("'" + self.username + "' currently has " + self.get_stats()['credits'] + ".")
    
  def start(self):
    """ Send the GET request in order to begin actions as the client. """
    self.session.get("http://www.ytmonster.net/waitTime.php")