# -*- coding: utf-8 -*-

from lsyflasksdkcore import AutoClass, PagerQuery


class StVideoBBase(AutoClass):
    """视频基本信息表"""

    def __init__(self):
        # ID
        self.id = ""
        # 视频编码
        self.video_code = ""
        # 视频名称
        self.video_name = ""
        # 组id
        self.group_id = ""
        # 播放地址
        self.video_url = ""
        # 视频类型
        self.video_type = ""
        # 控制标志
        self.is_controllable = None
        # 控制接口地址
        self.control_api_url = ""
        # 设备编码
        self.device_serial = ""
        # 信道
        self.channel_no = ""
        # 码流类型
        self.bit_type = None
        # 登入key
        self.ys_app_key = ""
        # 登入密码
        self.ys_app_secret = ""
        # 主节点
        self.nvr_app = ""
        # 子节点
        self.nvr_name = ""
        # 拉流类型
        self.nvr_mode = ""
        # 拉流地址
        self.nvr_edge = ""
        # 排序号
        self.order_number = None


class StVideoBEdit(StVideoBBase):
    pass


class StVideoBDetail(StVideoBBase):
    def __init__(self):
        super().__init__()
        self.group_name = ""


class StVideoBVideoList(StVideoBBase):
    def __init__(self):
        super().__init__()
        self.video_name = ""
        self.tm = ""
        self.image_name = ""
        self.file_name = ""
        self.file_dir = ""


class StVideoBPagerQuery(PagerQuery):
    def __init__(self):
        super().__init__()
        self.video_name = ""
        self.group_id = ""


class StVideoBVideoListQuery(AutoClass):
    def __init__(self):
        super().__init__()
        self.video_name = ""
        self.group_id = ""
