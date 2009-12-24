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
"""

$Id$
"""
from zope import interface
from zope.component import getUtility
from zope.publisher.interfaces import NotFound

from interfaces import ISEO


class SEOAttributeView(object):

    attr = None

    contentType = 'text/plain'

    def __call__(self):
        configlet = getUtility(ISEO)
        value = getattr(configlet, self.attr)
        if not configlet.enabled or not value:
            raise NotFound(self.context, self.__name__, self.request)
        self.request.response.setHeader('Content-Type', self.contentType)
        return value


class RobotsView(SEOAttributeView):

    attr = 'robots'

    contentType = 'text/plain'


class SitemapView(SEOAttributeView):

    attr = 'sitemap'

    contentType = 'text/xml'
