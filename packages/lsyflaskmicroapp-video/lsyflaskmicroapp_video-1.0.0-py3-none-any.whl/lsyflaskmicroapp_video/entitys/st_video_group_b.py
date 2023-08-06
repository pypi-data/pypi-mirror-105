# -*- coding: utf-8 -*-

from lsyflasksdkcore import AutoClass, PagerQuery


class StVideoGroupBBase(AutoClass):
    """视频分组表"""

    def __init__(self):
        # ID
        self.id = ""
        # 分组名
        self.group_name = ""
        # 排序号
        self.order_number = None


class StVideoGroupBEdit(StVideoGroupBBase):
    pass


class StVideoGroupBDetail(StVideoGroupBBase):
    pass


class StVideoGroupBPagerQuery(PagerQuery):
    def __init__(self):
        super().__init__()
        self.group_name = ""
