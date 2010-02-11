##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" geotargeting configlet interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.geotargeting')


class IGeotargetingProduct(interface.Interface):
    """ product interface """


class IGeotargeting(interface.Interface):
    """ geotargeting """

    zipCode = schema.TextLine(
        title = _('Zip code'),
        description = _('Content zip code.'),
        default = u'',
        required = False)