# -*- coding: utf-8 -*-

def create_video_group_b_model():
    """ 视频分组表 Model
    :return:
    """
    from .st_video_group_b import StVideoGroupBModel
    return StVideoGroupBModel()


def create_st_video_b_model():
    """ 视频基本信息表 Model
    :return:
    """
    from .st_video_b import StVideoBModel
    return StVideoBModel()


def create_st_video_image_r_model():
    """ 视频截图表 Model
    :return:
    """
    from .st_video_image_r import StVideoImageRModel
    return StVideoImageRModel()
