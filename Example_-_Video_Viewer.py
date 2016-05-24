import sys
from beast.ytmonster import YTMonster, Video

if len(sys.argv) == 3:

  # Create the client instance.
  client = YTMonster()
  
  # Set the maximum length (in seconds) that a video watch request may be.
  client.set_limit(100)
  
  # Attempt to login with the supplied credentials.
  client.login(sys.argv[1], sys.argv[2])
  if client.is_online():
    client.start()
    
    # Attempt to watch 5 videos.
    videos = Video(client)
    watched = 0
    while watched < 5:
      if videos.watch():
        watched += 1
    
    # Display the user's current points.
    client.show_points()
  
    # Log out when all actions are complete.
    client.logout()

else:
  print("Usage:\n\n\tExample_-_Video_Viewer.py Username Password")