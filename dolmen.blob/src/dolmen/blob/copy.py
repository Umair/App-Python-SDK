# -*- coding: utf-8 -*-

import shutil
import grokcore.component as grok
from ZODB.interfaces import IBlob
from zope.copy.interfaces import ICopyHook, ResumeCopy


class BlobFileCopyHook(grok.Adapter):
    """A copy hook for IBlobFile objects.
    """
    grok.implements(ICopyHook)
    grok.context(IBlob)

    def __call__(self, toplevel, register):
        register(self._copyBlob)
        raise ResumeCopy

    def _copyBlob(self, translate):
        target = translate(self.context)

        # We init the blob to get a consistent state.
        target.__init__()

        fsrc = self.context.open('r')
        fdst = target.open('w')
        shutil.copyfileobj(fsrc, fdst)
        fdst.close()
        fsrc.close()
