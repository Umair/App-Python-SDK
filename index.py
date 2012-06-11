from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from pdf  import _SaveFormat
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import os
from common.saasposeapp import SaasposeApp
from common.product import Product
from storage.folder import Folder
from xml.dom.minidom import parse, parseString
from xml.etree.ElementTree import fromstring , XML , tostring
def get_folders():
    folders = Folder.getFolders(Folder())
    return folders
class Folders(webapp.RequestHandler):
    
    
    def get(self):
        
        
        template_values = {
            'saveformat': _SaveFormat.PDFSaveFormat,
            }
        folders = get_folders()
        if folders.status_code==200:
            try:
                output = parseString(folders.content).toxml
                
                self.response.headers['Content-Type'] = 'application/xml'
                return self.response.out.write(output)
            except:
                self.response.headers['Content-Type'] = 'aplication/json'
                return self.response.out.write(folders)
            
        else:
            self.response.headers['Content-Type'] = 'text/html'
            path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
            self.response.out.write(template.render(path, template_values))
            
      
          
            

class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        template_values = {
            'saveformat': _SaveFormat.PDFSaveFormat,
            }
        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        
        if int(self.request.get("convert")) == 1:
            if len(self.request.get("file")) > 0:
                filename = self.request.get("hiddenfilename")
                file = self.request.get("file")
               
                SaasposeApp.AppSID =  self.request.get('AppSID');
                SaasposeApp.AppKey =  self.request.get('AppKey');
                #Product.BaseProductUri = "http://api.saaspose.com/v1.0";
               
#               Upload file to Sasspose server
                #folder = Folder.createFolder(Folder(),"testsampleapp");
                Folder.UploadFile(Folder(),os.path.realpath("") + "/test/" + filename, "");  
                        
class createFolder(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'templates/create_folder.html')
        self.response.out.write(template.render(path, ''))
    
    def post(self):
        folder_name = self.request.get('folder_name')
        folder = Folder.createFolder(Folder(),str(folder_name))
        self.response.headers['Content-Type'] = 'aplication/json'
        return self.response.out.write(folder.content)   
     

class uploadFile(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'templates/upload_file.html')
        self.response.out.write(template.render(path, ''))
        
    def post(self):
        upload_file = self.request.get('db_file')
        file=db.Blob(upload_file)
        #folder = Folder.UploadFile(Folder(), strfileName, strFile, strFolder)
        self.response.headers['Content-Type'] = 'text/json'
        return self.response.out.write("")
        
class fileExist(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'templates/file_exists.html')
        self.response.out.write(template.render(path, ''))
    
    def post(self):
        file_name = self.request.get('file_name')
        folder = Folder.FileExists(Folder(),str(file_name))
        self.response.headers['Content-Type'] = 'aplication/json'
        return self.response.out.write(folder.content)   
class discSpace(webapp.RequestHandler):
    def get(self):
        folder = Folder.getSpaceInfo(Folder())
        self.response.headers['Content-Type'] = 'aplication/json'
        return self.response.out.write(folder.content)
    
application = webapp.WSGIApplication([('/', MainPage),
                                      ('/folders', Folders),
                                      ('/createFolder', createFolder),
                                      ('/uploadFile', uploadFile),
                                      ('/fileExist', fileExist),
                                      ('/discSpace', discSpace),
                                      ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
