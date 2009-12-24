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
""" seo configlet interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.seo')


class ISEO(interface.Interface):
    """ configlet interface """

    enabled = schema.Bool(
        title = _(u'Enabled'),
        description = _(u'Enable SEO for this site.'),
        default = False,
        required = False)

    robots = schema.Text(
        title = _(u'Robots'),
        description = _(u'Robots'),
        default = ur"""User-agent: *
Disallow: /
""",
        required = False)

    sitemap = schema.Text(
        title = _(u'Sitemap'),
        description = _(u'Robots'),
        default = u'',
        required = False)


class IHTMLTags(interface.Interface):
    """ custom html head tags """

    title = schema.TextLine(
        title = _('Title'),
        description = _('Content for title html head tag.'),
        default = u'',
        required = False)

    description = schema.TextLine(
        title = _('Description'),
        description = _('Content for html meta tag - description.'),
        default = u'',
        required = False)

    keywords = schema.TextLine(
        title = _('Keywords'),
        description = _('Content for html meta tag - keywords.'),
        default = u'',
        required = False)
