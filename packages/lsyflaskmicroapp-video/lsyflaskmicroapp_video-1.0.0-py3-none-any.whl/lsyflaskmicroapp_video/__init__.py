# -*- coding: utf-8 -*-

from . import orm
from .apis import st_video_b
from .apis import st_video_group_b
from .apis import st_video_image_r


def init_app(app):
    orm.init_db(app)

    # 视频分组表
    app.register_blueprint(st_video_group_b.bp, url_prefix='/api/video/st_video_group_b')
    # 视频基本信息表
    app.register_blueprint(st_video_b.bp, url_prefix='/api/video/st_video_b')
    # 视频截图表
    app.register_blueprint(st_video_image_r.bp, url_prefix='/api/video/st_video_image_r')


__all__ = ['init_app']
