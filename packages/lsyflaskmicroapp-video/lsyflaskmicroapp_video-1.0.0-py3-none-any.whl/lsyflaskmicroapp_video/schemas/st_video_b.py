# -*- coding: utf-8 -*-

from lsyflasksdkcore.schema import Schema, PagerQuerySchema
from lsyflasksdkcore.utils.unique import get_uuid_str
from marshmallow import fields, post_load, validate

from ..entitys.st_video_b import StVideoBBase, StVideoBEdit, StVideoBDetail, StVideoBPagerQuery, \
    StVideoBVideoListQuery, StVideoBVideoList


class StVideoBSchema(Schema):
    """ 视频基本信息表 Schema """
    # ID
    id = fields.Str(description=u'ID', missing=get_uuid_str, validate=validate.Length(max=36))
    # 视频编码
    video_code = fields.Str(description=u'视频编码', required=True, validate=validate.Length(max=20))
    # 视频名称
    video_name = fields.Str(description=u'视频名称', required=True, validate=validate.Length(max=20))
    # 组id
    group_id = fields.Str(description=u'组id', required=True, validate=validate.Length(max=36))
    # 播放地址
    video_url = fields.Str(description=u'播放地址', required=True)
    # 视频类型
    video_type = fields.Str(description=u'视频类型', required=True, validate=validate.Length(max=10))
    # 控制标志
    is_controllable = fields.Int(description=u'控制标志', required=True, validate=validate.Range(min=0, max=99))
    # 控制接口地址
    control_api_url = fields.Str(description=u'控制接口地址', required=False, allow_none=True)
    # 设备编码
    device_serial = fields.Str(description=u'设备编码', required=False, allow_none=True)
    # 信道
    channel_no = fields.Str(description=u'信道', required=False, validate=validate.Length(max=50), allow_none=True)
    # 码流类型
    bit_type = fields.Int(description=u'码流类型', required=False, validate=validate.Range(min=0, max=99), allow_none=True)
    # 登入key
    ys_app_key = fields.Str(description=u'登入key', required=False, allow_none=True)
    # 登入密码
    ys_app_secret = fields.Str(description=u'登入密码', required=False, allow_none=True)
    # 主节点
    nvr_app = fields.Str(description=u'主节点', required=False, validate=validate.Length(max=20), allow_none=True)
    # 子节点
    nvr_name = fields.Str(description=u'子节点', required=False, validate=validate.Length(max=20), allow_none=True)
    # 拉流类型
    nvr_mode = fields.Str(description=u'拉流类型', required=False, validate=validate.Length(max=20), allow_none=True)
    # 拉流地址
    nvr_edge = fields.Str(description=u'拉流地址', required=False, allow_none=True)
    # 排序号
    order_number = fields.Int(description=u'排序号', required=False, validate=validate.Range(min=0, max=9999),
                              allow_none=True)
    lgtd = fields.Float(description=u'经度', required=False, allow_none=True)
    lttd = fields.Float(description=u'纬度', required=False, allow_none=True)

    @post_load
    def make(self, data, **kwargs):
        return StVideoBBase().__fill__(**data)


class StVideoBEditSchema(StVideoBSchema):

    @post_load
    def make(self, data, **kwargs):
        return StVideoBEdit().__fill__(**data)


class StVideoBDetailSchema(StVideoBSchema):
    group_name = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return StVideoBDetail().__fill__(**data)


class StVideoBVideoListSchema(StVideoBSchema):
    video_name = fields.Str()
    tm = fields.DateTime(allow_none=True)
    image_name = fields.Str(allow_none=True)
    file_name = fields.Str(allow_none=True)
    file_dir = fields.Str(allow_none=True)

    @post_load
    def make(self, data, **kwargs):
        return StVideoBVideoList().__fill__(**data)


class StVideoBPagerQuerySchema(PagerQuerySchema):
    video_name = fields.Str()
    group_id = fields.Str(missing="*")

    @post_load
    def make(self, data, **kwargs):
        return StVideoBPagerQuery().__fill__(**data)


class StVideoBVideoListQuerySchema(Schema):
    video_name = fields.Str()
    group_id = fields.Str(missing="*")

    @post_load
    def make(self, data, **kwargs):
        return StVideoBVideoListQuery().__fill__(**data)
