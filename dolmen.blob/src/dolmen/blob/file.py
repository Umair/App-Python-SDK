# -*- coding: utf-8 -*-

from ZODB.blob import Blob
from ZODB.interfaces import BlobError
from persistent import Persistent

from zope.interface import implements
from zope.location.interfaces import ILocation
from zope.contenttype import guess_content_type
from zope.component import queryMultiAdapter
from zope.schema.fieldproperty import FieldProperty

from dolmen.file import clean_filename
from dolmen.blob import IBlobFile, IFileStorage


class StorageError(Exception):
    """An error raised if the storage failed.
    """


class BlobValue(object):
    """A BlobValue is using a ZODB Blob to store data. It handles both
    the zope.app.file and zope.file features. It can be used as a blob
    attribute, for more complex object. It can also be used as a mixin
    with a Persistent class.
    """
    implements(IBlobFile)

    filename = FieldProperty(IBlobFile['filename'])
    mimeType = FieldProperty(IBlobFile['mimeType'])
    parameters = FieldProperty(IBlobFile['parameters'])

    def __init__(self, data='', contentType='',
                 filename=None, parameters=None):

        if filename:
            filename = clean_filename(filename)
            self.filename = filename

        if not contentType and filename:
            self.mimeType, enc = guess_content_type(name=filename)
        elif not contentType:
            self.mimeType = "application/octet-stream"
        else:
            self.mimeType = contentType

        if parameters is None:
            parameters = {}
        else:
            parameters = dict(parameters)
        self.parameters = parameters

        self._blob = Blob()
        self.data = data

    @property
    def contentType(self):
        return self.mimeType

    def open(self, mode="r"):
        return self._blob.open(mode)

    def openDetached(self):
        return file(self._blob.committed(), 'rb')

    def __len__(self):
        if self._blob == "":
            return 0
        reader = self._blob.open()
        reader.seek(0, 2)
        size = reader.tell()
        reader.close()
        return size

    @property
    def size(self):
        return int(self.__len__())

    @apply
    def data():
        """The blob property using a IFileStorage adapter
        to write down the value.
        """

        def get(self):
            blob = self._blob.open('r')
            data = blob.read()
            blob.close()
            return data

        def set(self, value):
            stored = queryMultiAdapter((self._blob, value), IFileStorage)
            if stored is not True:
                raise StorageError(
                    "An error occured during the blob storage. Check the "
                    "value type (%r). This value should implement IFile, "
                    "IString or IUnicode (see `dolmen.builtins`)."
                    % value.__class__)

        return property(get, set)

    @property
    def physical_path(self):
        try:
            filename = self._blob.committed()
        except BlobError:
            # We retry, the data has now been commited
            # if possible by the ZODB blob.
            try:
                filename = self._blob.committed()
            except BlobError:
                # The retry failed, we return None.
                return None
        return filename


class BlobFile(Persistent, BlobValue):
    """A INameFile component using a ZODB Blob to store the data.
    """
    implements(ILocation)

    __name__ = None
    __parent__ = None
