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
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.geotargeting.interfaces import IGeotargetingProduct
"""Indexes for Job Profiles

$Id$
"""
from zope import interface
from zope.schema import getFieldsInOrder
from zc.catalog.catalogindex import ValueIndex
from zope.app.catalog.attribute import AttributeIndex
from zope.app.catalog.text import TextIndex
from zope.component import getUtility
from z3c.multifieldindex.index import MultiFieldIndexBase
from zojax.authentication.utils import getPrincipal
from zojax.catalog.utils import Indexable
from zojax.catalog.interfaces import ICatalogQueryPlugin

from interfaces import IGeotargeting, IGeotargetingPreference


def geotargeting():
    return GeotargetingIndex(
        'value', Indexable('zojax.geotargeting.indexes.Geotargeting'))


class Geotargeting(object):

    def __init__(self, content, default=None):
        self.value = default
        extension = IGeotargeting(content, None)
        if extension is not None:
            self.value = extension


class GeotargetingIndex(AttributeIndex, MultiFieldIndexBase):

    def _fields(self):
        return getFieldsInOrder(IGeotargeting)

    def _getData(self, object):
        res = dict(map(lambda (name, field): (name, getattr(object, name)),
                        self._fields()))
        if res.get('location') is not None:
            res['location'] = res['location'].geocode
        return res
        

class GeotargetingQueryPlugin(object):
    
    interface.implements(ICatalogQueryPlugin)
    
    weight = 1
    
    def __call__(self):
        preference = IGeotargetingPreference(getPrincipal(), None)
        if preference is not None and preference.enabled \
            and preference.location is not None \
            and preference.location \
            and preference.location.geocode is not None \
            and preference.location.geocode:
            return {'geotargeting': {'location': {'any_of': (preference.location.geocode,)}}}
        return {}
    
    def isAvailable(self):
        return getUtility(IGeotargetingProduct).applyOnEachQuery