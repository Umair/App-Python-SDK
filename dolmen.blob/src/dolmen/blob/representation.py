# -*- coding: utf-8 -*-

import grokcore.component as grok
from dolmen.blob import IBlobFile
from zope.filerepresentation.interfaces import IReadFile, IWriteFile


class ReadFileAdapter(grok.Adapter):
    grok.context(IBlobFile)
    grok.implements(IReadFile)

    def size(self):
        return self.context.size

    def read(self):
        # We use the natural getter.
        return self.context.data


class WriteFileAdapter(grok.Adapter):
    grok.context(IBlobFile)
    grok.implements(IWriteFile)

    def write(self, data):
        # We use the natural setter to get the Storage capabilities.
        self.context.data = data
