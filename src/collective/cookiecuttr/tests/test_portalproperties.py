# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.cookiecuttr.testing import \
                        COLLECTIVE_COOKIECUTTR_INTEGRATION_TESTING

PROJECTNAME = 'collective.cookiecuttr'


class PortalPropertiesTestCase(unittest.TestCase):

    layer = COLLECTIVE_COOKIECUTTR_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.settings = None
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_settings_in_properties(self):
        self.assertTrue(hasattr(self.settings, 'cookiecuttr_enabled'))
        self.assertTrue(hasattr(self.settings, 'text_page_path'))
        self.assertTrue(hasattr(self.settings, 'accept_button'))
        # check default
        self.assertEqual(self.settings.accept_button, 'Accept cookies')

    def test_records_removed_on_uninstall(self):
        # XXX: I haven't found a better way to test this; anyone?
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        self.assertRaises(KeyError, self.settings, 'cookiecuttr_enabled')
