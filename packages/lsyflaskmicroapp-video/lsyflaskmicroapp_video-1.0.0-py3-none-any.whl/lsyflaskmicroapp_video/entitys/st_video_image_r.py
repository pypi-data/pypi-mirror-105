# -*- coding: utf-8 -*-

from lsyflasksdkcore import AutoClass, PagerQuery


class StVideoImageRBase(AutoClass):
    """视频截图表"""

    def __init__(self):
        # id
        self.id = ""
        # 视频id
        self.video_id = ""
        # 时间
        self.tm = None
        # 图像地址
        self.file_dir = ""
        # 地址名称
        self.file_name = ""
        # 图像名称
        self.image_name = ""
        # 备注
        self.remark = ""


class StVideoImageREdit(StVideoImageRBase):
    pass


class StVideoImageRDetail(StVideoImageRBase):
    pass


class StVideoImageRPagerQuery(PagerQuery):
    pass
