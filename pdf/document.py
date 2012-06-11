from common.product import Product
from common.utils import Utils
import json
class Document:

        FileName = ""

        def __init__(self,filename):
            self.FileName = filename
        
       
        def GetPageCount(self):
            strURI = Product.BaseProductUri + "/pdf/" + self.FileName + "/pages"
            signedURI = Utils.Sign(strURI);
            responseStream = Utils.processCommand(signedURI, "GET", "");
            _json = json.loads(responseStream)
            return len(_json)
        