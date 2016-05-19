import sys
from beast.ytmonster import YTMonster

if len(sys.argv) == 3:
  # Create client instance
  client = YTMonster()
  # Set the maximum length (seconds) that a video watch request may be
  client.set_limit(125)
  # Attempt to login
  client.login(sys.argv[1], sys.argv[2])
  if client.is_online():
    # Successfully complete watching 25 videos
    client.start(5)
    client.logout()
else:
  print("Usage:\n\n\tExample_-_Video_Viewer.py Username Password")