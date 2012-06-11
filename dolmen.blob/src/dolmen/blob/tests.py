# -*- coding: utf-8 -*-

import os.path
import unittest
from zope.testing import doctest, module
from zope.app.testing import functional

ftesting_zcml = os.path.join(os.path.dirname(__file__), 'ftesting.zcml')
FunctionalLayer = functional.ZCMLLayer(
    ftesting_zcml, __name__, 'FunctionalLayer', allow_teardown=True)


def setUp(test):
    module.setUp(test, 'dolmen.blob.ftests')


def test_suite():
    """Testing suite.
    """
    readme = functional.FunctionalDocFileSuite(
        'README.txt', setUp=setUp, tearDown=module.tearDown,
        optionflags=(doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE),
        )

    readme.layer = FunctionalLayer
    suite = unittest.TestSuite()
    suite.addTest(readme)
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
