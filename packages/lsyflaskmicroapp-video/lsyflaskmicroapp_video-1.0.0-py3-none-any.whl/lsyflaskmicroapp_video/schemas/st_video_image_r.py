# -*- coding: utf-8 -*-

from lsyflasksdkcore.schema import Schema, PagerQuerySchema
from lsyflasksdkcore.utils.unique import get_uuid_str
from marshmallow import fields, post_load, validate

from ..entitys.st_video_image_r import StVideoImageRBase, StVideoImageREdit, StVideoImageRDetail, \
    StVideoImageRPagerQuery


class StVideoImageRSchema(Schema):
    """ 视频截图表 Schema """
    # id
    id = fields.Str(missing=get_uuid_str, validate=validate.Length(max=36))
    # 视频id
    video_id = fields.Str(required=True, validate=validate.Length(max=36))
    # 时间
    tm = fields.DateTime(required=True)
    # 图像地址
    file_dir = fields.Str(required=True)
    # 地址名称
    file_name = fields.Str(required=True)
    # 图像名称
    image_name = fields.Str(required=True)
    # 备注
    remark = fields.Str(required=False, allow_none=True)

    @post_load
    def make(self, data, **kwargs):
        return StVideoImageRBase().__fill__(**data)


class StVideoImageREditSchema(StVideoImageRSchema):

    @post_load
    def make(self, data, **kwargs):
        return StVideoImageREdit().__fill__(**data)


class StVideoImageRDetailSchema(StVideoImageRSchema):

    @post_load
    def make(self, data, **kwargs):
        return StVideoImageRDetail().__fill__(**data)


class StVideoImageRPagerQuerySchema(PagerQuerySchema):

    @post_load
    def make(self, data, **kwargs):
        return StVideoImageRPagerQuery().__fill__(**data)
