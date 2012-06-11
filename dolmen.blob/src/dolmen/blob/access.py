# -*- coding: utf-8 -*-

import grokcore.view as grok
from dolmen.blob import IBlobFile
from zope.file.download import DownloadResult, getHeaders


class FilePublisher(grok.View):
    grok.name('file_publish')
    grok.context(IBlobFile)

    def update(self):
        for k, v in getHeaders(self.context,
                               downloadName=self.context.filename,
                               contentDisposition="attachment"):
            self.request.response.setHeader(k, v)

    def render(self):
        return DownloadResult(self.context)
