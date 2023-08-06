# -*- coding: utf-8 -*-

from lsyflasksdkcore.schema import Schema, PagerQuerySchema
from lsyflasksdkcore.utils.unique import get_uuid_str
from marshmallow import fields, post_load, validate

from ..entitys.st_video_group_b import StVideoGroupBBase, StVideoGroupBEdit, StVideoGroupBDetail, \
    StVideoGroupBPagerQuery


class StVideoGroupBSchema(Schema):
    """ 视频分组表 Schema """
    # ID
    id = fields.Str(missing=get_uuid_str, validate=validate.Length(max=36))
    # 分组名
    group_name = fields.Str(required=True, validate=validate.Length(max=20))
    # 排序号
    order_number = fields.Int(required=False, validate=validate.Range(min=0, max=9999), allow_none=True)

    @post_load
    def make(self, data, **kwargs):
        return StVideoGroupBBase().__fill__(**data)


class StVideoGroupBEditSchema(StVideoGroupBSchema):

    @post_load
    def make(self, data, **kwargs):
        return StVideoGroupBEdit().__fill__(**data)


class StVideoGroupBDetailSchema(StVideoGroupBSchema):

    @post_load
    def make(self, data, **kwargs):
        return StVideoGroupBDetail().__fill__(**data)


class StVideoGroupBPagerQuerySchema(PagerQuerySchema):
    group_name = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return StVideoGroupBPagerQuery().__fill__(**data)
