# -*- coding: utf-8 -*-
"""Tests for enable_member action."""

from DateTime import DateTime
from plone import api
from niteoweb.ipn.core.interfaces import IIPN
from niteoweb.ipn.core.testing import IntegrationTestCase
from zope.component import queryAdapter
from zope.testing.loggingsupport import InstalledHandler

import mock


class TestEnableMember(IntegrationTestCase):
    """Test runtime flow through the enable_member() action."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.ipn = queryAdapter(self.portal, IIPN)
        self.log = InstalledHandler('niteoweb.ipn.core')

        # create a test product group and set it's validity
        api.group.create(groupname='1')
        group = api.group.get(groupname='1')
        group.setGroupProperties(mapping={'validity': 10})

    def tearDown(self):
        """Clean up after yourself."""
        self.log.clear()
        self.log.uninstall()

    @mock.patch('niteoweb.ipn.core.ipn.DateTime')
    def test_create_member(self, DT):
        """Test creating a new member with enable_member() action."""
        # mock current date
        DT.return_value = DateTime('2012/01/01')

        self.ipn.enable_member(
            email='new@email.com',
            product_id='1',
            trans_type='SALE',
            fullname='New Member',
            affiliate='aff@email.com'
        )

        # test member exists
        self.assertTrue(api.user.get(username='new@email.com'))

        # test member is in product group

        # test member valid_to

        # # TODO: test member history

        # test log output
        self.assertEqual(len(self.log.records), 4)
        self.assert_log_record(
            'INFO',
            "Creating a new member: new@email.com",
        )
        self.assert_log_record(
            'INFO',
            "Added member 'new@email.com' to product group '1'.",
        )
        self.assert_log_record(
            'INFO',
            "Member's (new@email.com) valid_to date set to 2012/01/11.",
        )
        self.assert_log_record(
            'INFO',
            "Enabled member 'new@email.com'.",
        )