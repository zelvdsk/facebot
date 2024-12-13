# Account login
```py
# import object
from facebot.changepp import ChangeProfilePicture

# login using str cookies
fb = ChangeProfilePicture(cookie='')
# login using dict cookies
fb = ChangeProfilePicture(cookie={})
# login using session
import requests
session = requests.session()
fb = ChangeProfilePicture(session=session)
```
# Upload pictures
```py
upload = fb.upload(pictures=b'') #bytes pictures
if upload.success:
    fbid = upload.fbid
    pict_url = upload.picture_url
```
# Change Profile Picture
```py
change = fb.change(fbid=fbid, caption='') # caption default set None
if change.success:
    print(change.posts_url)
```
   
