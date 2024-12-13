import requests
import re, json, random
from typing import Union
from . import utils

class ChangeProfilePicture:
    def __init__(self, session: object=None, cookie: Union[str, dict]=None) -> None:
        self.session = session or requests.session()
        
        if cookie:
            if isinstance(cookie, str): self.session.cookies['cookie'] = cookie
            elif isinstance(cookie, dict): self.session.cookies['cookie'] = '; '.join(f'{k__}={v__}' for k__, v__ in cookie.items())

    def upload(self, picture: bytes) -> utils.Response:
        params = utils.payload(self.session.get('https://web.facebook.com/me').text)
        params.update({'profile_id': params['__user'],'photo_source': "57"})

        upload_pictures = self.session.post('https://web.facebook.com/profile/picture/upload/', params=params, files={'file': ('images.jpg', picture)}).text
        try:
            fbid = re.search(r'fbid":"(.*?)"', upload_pictures).group(1)
            picture_url = re.search(r'imageURI":"(.*?)"', upload_pictures).group(1)
            
            return utils.Response(success=True, fbid=fbid, picture_url=picture_url)
        except AttributeError:
            return utils.Response(success=False)

    def change(self, fbid: str, caption: str=None) -> utils.Response:
        data = utils.payload(self.session.get('https://web.facebook.com/me').text)
        data.update({'fb_api_req_friendly_name': 'ProfileCometProfilePictureSetMutation','variables': json.dumps({"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1734088367059,314474,190055527696468,,","caption":caption,"existing_photo_id":fbid,"expiration_time":None,"profile_id":data['__user'],"profile_pic_method":"EXISTING","profile_pic_source":"TIMELINE","scaled_crop_rect":{"height":0.66667,"width":1,"x":0,"y":0},"skip_cropping":True,"actor_id":data['__user'],"client_mutation_id":"1"},"isPage":False,"isProfile":True,"sectionToken":"UNKNOWN","collectionToken":"UNKNOWN","scale":3,"__relay_internal__pv__ProfileGeminiIsCoinFlipEnabledrelayprovider":False}),'doc_id': '8839375402787576'})

        change_upload = self.session.post('https://web.facebook.com/api/graphql/', data=data).text
        if fbid in change_upload:
            return utils.Response(success=True, posts_url=re.search(r'"profilePhoto":{"url":"(.*?)"', change_upload).group(1))
        else:
            return  utils.response(success=False)
