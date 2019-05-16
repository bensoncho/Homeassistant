"""
Custom component for Home Assistant to enable sending messages via Notify Line API.
Example configuration.yaml entry:
notify:
  - name: dropbox_upload
    platform: dropbox_upload
    access_token: 'dropbox_api_key'    
    
With this custom component loaded, you can upload to Dropbox.
"""
import json
import requests
import logging
import voluptuous as vol
 
from aiohttp.hdrs import AUTHORIZATION, CONTENT_TYPE
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_ACCESS_TOKEN 
from homeassistant.components.notify import (
    ATTR_DATA, PLATFORM_SCHEMA, BaseNotificationService)

_LOGGER = logging.getLogger(__name__)

BASE_URL = 'https://content.dropboxapi.com/2/files/upload'
ATTR_FILE = 'file'
ATTR_FILENAME = 'filename'


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ACCESS_TOKEN): cv.string,
})

def get_service(hass, config, discovery_info=None):
    """Get the Line notification service."""
    access_token = config.get(CONF_ACCESS_TOKEN )
    return DropboxNotificationService(access_token)
                                           
class DropboxNotificationService(BaseNotificationService):
    """Implementation of a notification service for the Line Messaging service."""

    def __init__(self, access_token):
        """Initialize the service."""
        self.access_token = access_token                                           
        
    def send_message(self, message="", **kwargs):
        """Send some message."""
        data = kwargs.get(ATTR_DATA, None) 
        file = data.get(ATTR_FILE) if data is not None and ATTR_FILE in data else None
        filename = data.get(ATTR_FILENAME) if data is not None and ATTR_FILENAME in data else None

        Dropbox = {
          "path": "/" + filename,
          "mode": "overwrite",
          "mute": True,
          "strict_conflict": False
        }
              
      
        file = {IMAGEFILE:open(data.get(ATTR_FILE),'rb')} if data is not None and ATTR_FILE in data else None      
        headers = {
                CONTENT_TYPE: "application/octet-stream",
                AUTHORIZATION:"Bearer "+ self.access_token,
                'Dropbox-API-Arg': json.dumps(Dropbox)
        }
       
        if file is not none or filename is not none:
          with open(filename, 'rb') as f:
            r=requests.Session().post(BASE_URL, headers=headers, data=f)
          if r.ok  != True
            _LOGGER.error(r.text)
        elif file is none:
          _LOGGER.error("Missing file")
        elif filename is none:
          _LOGGER.error("Missing filename")
