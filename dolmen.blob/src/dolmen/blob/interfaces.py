# -*- coding: utf-8 -*-

from dolmen import builtins
from dolmen.file import INamedFile
from zope.file.interfaces import IFile
from zope.publisher.browser import FileUpload
from zope.interface import Interface, Attribute, classImplements


class IBlobFile(INamedFile, IFile):
    """A marker interface for file using ZODB blobs.
    """
    physical_path = Attribute("Physical path of the stored file.")


class IFileStorage(Interface):
    """A component dedicated to store items.
    """

    def __call__(file, data):
        """Persists the data in the file element.
        """


class IFileUpload(builtins.IFile):
    """Defines an Upload object created by zope.publisher
    for data elements in forms.
    """

classImplements(FileUpload, IFileUpload)
