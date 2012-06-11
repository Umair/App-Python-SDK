from urllib import quote, urlencode
import base64 
from urlparse import urlparse
from saasposeapp import SaasposeApp
import hashlib
import hmac
from django.utils import simplejson
import collections
import cStringIO
import os.path
import urllib
from google.appengine.api import urlfetch
import re
from xml.etree.ElementTree import fromstring , XML , tostring
#import atom.client
#import atom.core
#import atom.http_core
#import gdata.gauth
#import gdata.data

class Utils:
    buf = cStringIO.StringIO();
    buf_uploadFile   = cStringIO.StringIO();

    def processCommand(self,url,method="GET",headerType="XML",src=""):
                
        method = method.upper()
        headerType = headerType.upper()
        
#        form_fields = {
#                       "first_name": "Umair",
#                       "last_name": "Ejaz",
#                       "email_address": "umair.ejaz@gmail.com"
#        }
        #form_data = urllib.urlencode(form_fields)

        
        if (method is "POST"):
            method = urlfetch.POST
        elif method is "PUT":
            method = urlfetch.PUT
            
            
        if (headerType == "JSON"):
            #headers={'Content-Type': 'application/json'}
            headers={'Content-Type': 'application/xml'}
            #c.setopt(c.HTTPHEADER, ['Accept: application/xml', 'Accept-Charset: application/xml'])
        else:
            headers={'Content-Type': 'application/xml'}
            
            #c.setopt(c.HTTPHEADER, ['Accept: application/json'])
            
        result = urlfetch.fetch(url=url,method=method,deadline = 4,headers=headers)
        print result
        return result;
    
    def uploadFileBinary(self, url, localfile, headerType="XML"):
        headerType = headerType.upper();
        fp = open(localfile, 'r');
#               
        c = pycurl.Curl();
        c.setopt(pycurl.URL, url);
        c.setopt(pycurl.VERBOSE, 1);
        c.setopt(pycurl.USERPWD, 'umair123');
        c.setopt(pycurl.PUT, 1);
#        c.setopt(pycurl.RETURNTRANSFER, 1)
        c.setopt(pycurl.HEADER, False);
                    
        if (headerType == "XML"):
            c.setopt(c.HTTPHEADER, ['Accept: application/xml', 'Content-Type: application/xml']);
        else:
            c.setopt(c.HTTPHEADER, ["Content-Type: application/json"]);
        
        c.setopt(pycurl.INFILE  , fp);
        c.setopt(pycurl.WRITEFUNCTION, self.buf_uploadFile.write);
        c.setopt(pycurl.INFILESIZE  , os.path.getsize(localfile));
        
        result =    c.perform();
        c.close();
        fp.close();
        result = ""
        return result;
              

    def Sign(self,UrlToSign):
                
        UrlToSign = UrlToSign.replace(" ", "%20");
                
        url = urlparse(UrlToSign);
             
        if (url.query == ""):
            urlPartToSign = url.scheme + "://" + url.netloc + url.path + "?appSID=" + SaasposeApp.AppSID
        else:
            urlPartToSign = url.scheme + "://" + url.netloc + url.path + "?" + url.query + "&appSID=" + SaasposeApp.AppSID
 
        # Decode the private key into its binary format
#        decodedKey = decodeBase64UrlSafe(SaasposeApp.AppKey)
#     
#        signature = hmac.new(decodedKey, urlPartToSign, hashlib.sha1).hexdigest();
#
#        encodedSignature = encodeBase64UrlSafe(signature)

        # return UrlToSign . "?appSID=" . this->APPSID . "&signature=" . encodedSignature;
        signature = hmac.new(SaasposeApp.AppKey, urlPartToSign, hashlib.sha1).digest().encode('base64')[:-1]
        signature = re.sub('[=_-]','',signature)
        #signature = re.sub('_','',signature)
        
        encodedSignature = "bFRma65WSEtLhdIrpGgbVcg2xvE"
        
        if (url.query == ""):
            return url.scheme + "://" + url.netloc + url.path + "?appSID=" + SaasposeApp.AppSID + "&signature=" + signature
        else:
            return url.scheme + "://" + url.netloc + url.path + "?" + url.query + "&appSID=" + SaasposeApp.AppSID + "&signature=" + signature
        
        
    def ValidateOutput(self,result):
        strResult = str(result);
        
        validate = ["Unknown file format.", "Unable to read beyond the end of the stream", 
        "Index was out of range", "Cannot read that as a ZipFile", "Not a Microsoft PowerPoint 2007 presentation",
        "Index was outside the bounds of the array", "An attempt was made to move the position before the beginning of the stream"
        ];

        invalid = 0;
        for key in validate:
            if key == strResult:
                invalid = 1
                 
        if invalid == 1:
           return strResult;
        else:
           return ""
    
        
    def getFieldValue(self,jsonResponse, fieldName):
        in_json = json.loads(jsonResponse);
        return in_json.get(fieldName);
        
    
     
    def getFieldCount(self,jsonResponse, fieldName):
        in_json = json.loads(jsonResponse);
        return len(in_json);

#    def recursiveCount(self,val, length = 0):
#        if isinstance(val, collections.Iterable):
#            length = length + len(val);
#            recursiveCount()
    
     #==========================================================================
     # * Copies the contents of input to output. Doesn't close either stream.
     # *
     # * @param string $input input stream.
     # *
     # * @return copyStream($input) - Outputs the converted input stream.
     #==========================================================================
     
#    public function copyStream($input){
#    return stream_get_contents($input);
#    }
    
   
    def saveFile(self,input, fileName):
        try:
            f=open(fileName, 'w');
            f.write(input);
            f.close();
        except:
            return "error"
              
    
    def getFileName(self,file):
        absolute_path = os.path.abspath(file);
        base = os.path.basename(absolute_path)
        fileName = os.path.splitext(base)[0]
        return fileName
    
    
    
#u = Utils();
#f = u.getFileName('C:\\test.txt');
#print f;
#strURI = "http://api.saaspose.com/v1.1/words/myfile.txt?format=PDF";
#newStr = u.Sign(strURI);
#u.processCommand(newStr);
#u.saveFile(u.buf.getvalue(),'D:\\test.txt');

