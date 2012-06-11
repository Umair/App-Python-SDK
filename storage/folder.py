from common.product import Product
from common.utils import Utils

class Folder:
	strURIFolder = "";
	strURIFile = "";
	strURIExist = "";
	strURIDisc = "";
	
	def __init__(self):
		self.strURIFolder = Product.BaseProductUri + "/storage/folder";
		self.strURIFile = Product.BaseProductUri + "/storage/file/";
		self.strURIExist = Product.BaseProductUri + "/storage/exist/";
		self.strURIDisc = Product.BaseProductUri + "/storage/disc";
	
	def getFolders(self):
		try:
			#build URI
			strURIRequest = self.strURIFolder
			signedURI = Utils.Sign(Utils(),strURIRequest)

			responseStream = Utils.processCommand(Utils(),signedURI, "GET", "JSON", "")
			
			if (responseStream.status_code != 200):
				return False
			else:
				return responseStream
					
		except:
			raise "exception"
		
	def createFolder(self,strFolder):
		try:
			#build URI
			strURIRequest = self.strURIFolder +'/' +strFolder
			signedURI = Utils.Sign(Utils(),strURIRequest)

			responseStream = Utils.processCommand(Utils(),signedURI, "PUT", "", "")
			
			return responseStream
					
		except:
			raise "exception"
		
	def getSpaceInfo(self):
		try:
					#build URI
			strURI = self.strURIDisc
                
            #sign URI
			signedURI = Utils.Sign(Utils(),strURI);
             
			responseStream = Utils.processCommand(Utils(),signedURI, "GET", "JSON", "")
			
			return responseStream
			
            
		except:
			raise "exception"
    
	def UploadFile(self, strfileName, strFile, strFolder):
		try:
			strRemoteFileName = strfileName;
			strURIRequest = self.strURIFile;
				
			if strFolder == "":
				strURIRequest += strRemoteFileName;
			else:
				strURIRequest += strFolder + "/" + strRemoteFileName;
	
			signedURI = Utils.Sign(strURIRequest);
	
			Utils.uploadFileBinary(signedURI, strFile);
		
		except:
			raise "exception"
		
	def FileExists(self,fileName):
		try:
			if fileName == "":
				raise Exception("No file name specified")
                
            #build URI
			strURI = self.strURIExist + fileName
                
            #sign URI
			signedURI = Utils.Sign(Utils(),strURI);
             
			responseStream = Utils.processCommand(Utils(),signedURI, "GET", "JSON", "")
			
			return responseStream
			
            
		except:
			raise "exception"
        
    
    
   
# Deletes a file from remote storage
#
# @param string $fileName
#
	def DeleteFile(self,fileName):
    
		try:
        
            #//check whether file is set or not
			if (fileName == ""):
				raise Exception("No file name specified");
             
            #build URI
			strURI = self.strURIFile + fileName
             
            #sign URI
			signedURI = Utils.Sign(strURI);
             
			responseStream = json_decode(Utils.processCommand(signedURI, "DELETE", "", ""));
			if (responseStream.code != 200):
				return False;
			else:
				return True
             
		except:
			raise "exception"
        
    