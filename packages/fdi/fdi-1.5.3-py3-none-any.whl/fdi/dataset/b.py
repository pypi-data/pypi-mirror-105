# -*- coding: utf-8 -*-

# Automatically generated from fdi/dataset/resources/BaseProduct.yml. Do not edit.

from collections import OrderedDict
from fdi.dataset.finetime import FineTime

from .attributable import addMetaDataProperty
from .readonlydict import ReadOnlyDict
from .serializable import Serializable
from .abstractcomposite import AbstractComposite
from .listener import EventSender, EventType
from .eq import deepcmp
from .copyable import Copyable
from .history import History

import copy
from functools import lru_cache
from collections import OrderedDict

import logging
# create logger
logger = logging.getLogger(__name__)


_Model_Spec = {
    'name': 'BaseProduct',
    'description': 'FDI base class',
    'parents': [
        None,
    ],
    'level': 'ALL',
    'schema': '1.4',
    'metadata': {
        'description': {
            'id_zh_cn': '描述',
            'data_type': 'string',
            'description': 'Description of this product',
            'description_zh_cn': '对本产品的描述。',
            'default': 'UNKNOWN',
            'valid': '',
            'typecode': 'B',
        },
        'type': {
            'id_zh_cn': '产品类型',
            'data_type': 'string',
            'description': 'Product Type identification. Name of class or CARD.',
            'description_zh_cn': '产品类型。完整Python类名或卡片名。',
            'default': 'BaseProduct',
            'valid': '',
            'typecode': 'B',
        },
        'creator': {
            'id_zh_cn': '本产品生成者',
            'data_type': 'string',
            'description': 'Generator of this product.',
            'description_zh_cn': '本产品生成方的标识，例如可以是单位、组织、姓名、软件、或特别算法等。',
            'default': 'UNKNOWN',
            'valid': '',
            'typecode': 'B',
        },
        'creationDate': {
            'id_zh_cn': '产品生成时间',
            'fits_keyword': 'DATE',
            'data_type': 'finetime',
            'description': 'Creation date of this product',
            'description_zh_cn': '本产品生成时间',
            'default': 0,
            'valid': '',
            'typecode': None,
        },
        'rootCause': {
            'id_zh_cn': '数据来源',
            'data_type': 'string',
            'description': 'Reason of this run of pipeline.',
            'description_zh_cn': '数据来源（此例来自鉴定件热真空罐）',
            'default': 'UNKNOWN',
            'valid': '',
            'typecode': 'B',
        },
        'version': {
            'id_zh_cn': '版本',
            'data_type': 'string',
            'description': 'Version of product',
            'description_zh_cn': '产品版本',
            'default': '0.8',
            'valid': '',
            'typecode': 'B',
        },
        'FORMATV': {
            'id_zh_cn': '格式版本',
            'data_type': 'string',
            'description': 'Version of product schema and revision',
            'description_zh_cn': '产品格式版本',
            'default': '1.4.0.8',
            'valid': '',
            'typecode': 'B',
        },
    },
    'datasets': {
    },
}

ProductInfo = ReadOnlyDict(_Model_Spec)

MdpInfo = ProductInfo['metadata']


@addMetaDataProperty
class BaseProduct(AbstractComposite, Copyable, Serializable,  EventSender):
    """ A BaseProduct is a generic result that can be passed on between
    (standalone) processes.

    In general a Product contains zero or more datasets, history,
    optional metadata as well as some required metadata fields.
    Its intent is that it can fully describe itself; this includes
    the way how this product was achieved (its history). As it is
    the result of a process, it should be able to save to and restore
    from an Archive device.

    Many times a Product may contain a single dataset and for this
    purpose the first dataset entry can be accessed by the getDefault()
    method. Note that the datasets may be a composite of datasets
    by themselves.

    mh: Built-in Attributes in productInfo['metadata'] can be accessed with e.g. p.creator
    or p.meta['description'].value:
    p.creator='foo'
    assert p.creatur=='foo'
    assert p.meta['creator']=='foo'
    p.meta['creator']=Parameter('bar')
    assert p.meta['creator']==Parameter('bar')

    BaseProduct class (level ALL) schema 1.4 inheriting [None].

Automatically generated from fdi/dataset/resources/BaseProduct.yml on 2021-04-28 14:20:36.012495.

Description:
FDI base class

    """

    def __init__(self,
                 description='UNKNOWN',
                 typ_='BaseProduct',
                 creator='UNKNOWN',
                 creationDate=FineTime(0),
                 rootCause='UNKNOWN',
                 version='0.8',
                 FORMATV='1.4.0.8',
                 zInfo=None,
                 **kwds):

        if 0 and 'metasToBeInstalled' in kwds:
            # This class is being called probably from super() in a subclass
            metasToBeInstalled = kwds['metasToBeInstalled']
            del kwds['metasToBeInstalled']

            # 'description' is consumed in annotatable super class so it is not in.
            description = metasToBeInstalled.pop(
                'description') if 'description' in metasToBeInstalled else 'UNKNOWN'
            super().__init__(description=description, **kwds)
            self.history = History()
            return
        # this class is being called directly

        # list of local variables.
        metasToBeInstalled = copy.copy(locals())
        for x in ('self', '__class__', 'zInfo', 'kwds'):
            metasToBeInstalled.pop(x)

        global ProductInfo
        if zInfo is None:
            zInfo = ProductInfo

        # 'description' is consumed in annotatable super class so it is not in.

        description = metasToBeInstalled['description']
        # description = metasToBeInstalled.pop('description')
        # must be the first line to initiate meta and get description
        super().__init__(description=description, zInfo=zInfo, **kwds)

        self.installMetas(metasToBeInstalled)

        self._history = History()

    def installMetas(self, mtbi):
        """ put parameters in group in product metadata, and updates productInfo. values in mtbi override those default ones in group.
        """

        for met, value in mtbi.items():
            #  typ_ in mtbi (from __init__) changed to type
            name = 'type' if met == 'typ_' else met
            # set to input if given or to default.
            self.__setattr__(name, value)
            print('@@@@', name, value, id(self))

    @property
    def history(self):
        """ xx must be a property for ``self.xx = yy`` to work in super class after xx is set as a property also by a subclass.
        """
        return self._history

    @history.setter
    def history(self, history):
        self._history = history

    def accept(self, visitor):
        """ Hook for adding functionality to meta data object
        through visitor pattern."""
        visitor.visit(self)

    def getDefault(self):
        """ Convenience method that returns the first dataset \
        belonging to this product. """
        return list(self._sets.values())[0] if len(self._sets) > 0 else None

    def targetChanged(self, event):
        pass
        if event.source == self.meta:
            if event.type_ == EventType.PARAMETER_ADDED or \
               event.type_ == EventType.PARAMETER_CHANGED:
                # logger.debug(event.source.__class__.__name__ +   ' ' + str(event.change))
                pass

    def toString(self, level=0,
                 tablefmt='rst', tablefmt1='simple', tablefmt2='simple',
                 matprint=None, trans=True, beforedata='', **kwds):
        """ like AbstractComposite but with history
        """
        h = self.history.toString(
            level=level,
            tablefmt=tablefmt, tablefmt1=tablefmt1, tablefmt2=tablefmt2,
            matprint=matprint, trans=trans, **kwds)
        s = super(BaseProduct, self).toString(
            level=level,
            tablefmt=tablefmt, tablefmt1=tablefmt1, tablefmt2=tablefmt2,
            matprint=matprint, trans=trans, beforedata=h, **kwds)
        return s

    def __getstate__(self):
        """ Can be encoded with serializableEncoder """
        if 0:
            # remove self from meta's listeners because the deserialzed product will add itself during instanciation.
            print('1###' + self.meta.toString())
            metac = self.meta.copy()
            print('***' + metac.toString())
            print(deepcmp(self, metac.listeners[0]))
            metac.removeListener(self)

        ls = [
            ("meta", self.meta),
            ("_sets", self._sets if hasattr(self, '_sets') else None),
            ("history", self._history if hasattr(self, '_history') else None),
            ("listeners", self._listeners if hasattr(self, '_history') else None),
            ("_STID", self._STID if hasattr(self, '_STID') else None),
        ]

        return OrderedDict(ls)


"""
    @property
    def description(self): pass

    @description.setter
    def description(self, p): pass

    @property
    def type(self): pass

    @type.setter
    def type(self, p): pass

    @property
    def creator(self): pass

    @creator.setter
    def creator(self, p): pass

    @property
    def creationDate(self): pass

    @creationDate.setter
    def creationDate(self, p): pass

    @property
    def rootCause(self): pass

    @rootCause.setter
    def rootCause(self, p): pass

    @property
    def version(self): pass

    @version.setter
    def version(self, p): pass

    @property
    def FORMATV(self): pass

    @FORMATV.setter
    def FORMATV(self, p): pass
"""


# Product = addMetaDataProperty(Product)
