# -*- coding: utf-8 -*-

"""
St_Video_B
~~~~~~~~~~~~~
视频基本信息表
"""
import logging

from flask import current_app
from flask_login import current_user
from lsyflasksdkcore import RequestQuery, eresponse, sresponse, PkQuerySchema
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.schema import PksQuerySchema, PksQuery, PkQuery
from lsyflasksdkcore.swagger import doc
from lsyflasksdkcore.utils.unique import get_uuid_str
from werkzeug.exceptions import InternalServerError

from ..entitys.st_video_b import StVideoBPagerQuery, StVideoBEdit, StVideoBVideoListQuery
from ..models import create_st_video_b_model, create_video_group_b_model
from ..schemas.st_video_b import StVideoBPagerQuerySchema, StVideoBEditSchema, \
    StVideoBDetailSchema, StVideoBVideoListQuerySchema, StVideoBVideoListSchema

logger = logging.getLogger(__name__)

bp = Blueprint('st_video_b', __name__)


@bp.route('/page', methods=['GET', 'POST'])
@bp.auth.grant_view
def page():
    try:
        query = RequestQuery(StVideoBPagerQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: StVideoBPagerQuery = query.data

        model = create_st_video_b_model()
        dbr, count = model.get_page_query(qd.video_name, qd.group_id, qd.rows, qd.offset)
        return sresponse(dbr.json, total=count)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/add', methods=['POST'])
@bp.auth.grant_add
def add():
    try:
        query = RequestQuery(StVideoBEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: StVideoBEdit = query.data
        entity.id = get_uuid_str()
        model = create_st_video_b_model()
        model.add(entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/modify', methods=['POST'])
@bp.auth.grant_edit
def modify():
    try:
        query = RequestQuery(StVideoBEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: StVideoBEdit = query.data
        model = create_st_video_b_model()
        model.modify(entity.id, entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/delete', methods=['POST'])
@bp.auth.grant_delete
def delete():
    try:
        query = RequestQuery(PksQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: PksQuery = query.data
        model = create_st_video_b_model()
        model.tran_delete(qd.ids)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/detail', methods=['POST'])
@bp.auth.grant_view
def detail():
    try:
        query = RequestQuery(PkQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: PkQuery = query.data
        model = create_st_video_b_model()
        data = model.get_detail(qd.id).json
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('tasks', methods=['GET', 'POST'])
@bp.auth.grant_view
def tasks():
    """用于在nodemedia后台中掉用"""
    try:
        model = create_st_video_b_model()
        lst = model.get_all().to_list()
        lst = [item for item in lst if item.nvr_mode == "enable"]

        data = []
        for item in lst:
            if item.video_type == "hk":
                # temp = item.nvr_edge + str(item.bit_type) + '0' + item.channel_no + '/'
                temp = "rtsp://%s:%s@%s/Streaming/Channels/%s0%s/" % (
                    item.ys_app_key, item.ys_app_secret, item.nvr_edge, item.bit_type, item.channel_no)
                data.append({"app": item.nvr_app, "name": item.nvr_name, "mode": item.nvr_mode, "edge": temp})
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/group_video', methods=['POST'])
@bp.auth.grant_view
def group_video():
    try:
        query = RequestQuery(StVideoBVideoListQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: StVideoBVideoListQuery = query.data

        model = create_st_video_b_model()
        lst = model.get_video_list_query(qd.video_name, qd.group_id, current_user.content_role.video_ids).to_list()
        lst = [item for item in lst if item.nvr_mode == "enable"]

        group_model = create_video_group_b_model()
        groups = group_model.get_all("order_number", "asc").data

        config = current_app.config
        photo_url = config.get('PHOTO_URL', '')
        result = []
        for g in groups:
            videos = []
            for item in lst:
                if item.group_id == g.id:
                    if item.file_name:
                        item.file_name = photo_url + item.file_name
                    # 用户选择子码流后用子码流播放
                    if item.bit_type == 2 and item.ys_app_key:
                        item.video_url = item.ys_app_key
                    videos.append(StVideoBVideoListSchema().dump(item))
            if videos:
                result.append({"id": g.id, "group_name": g.group_name, "videos": videos})
        return sresponse(result)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/group_tree', methods=['POST'])
@bp.auth.grant_view
def group_tree():
    try:
        model = create_st_video_b_model()
        video_lst = model.get_all().to_list()
        video_lst = [item for item in video_lst if item.nvr_mode == "enable"]

        group_model = create_video_group_b_model()
        group_lst = group_model.get_all("order_number", "asc").to_list()

        root_node = {"id": "root", "name": "所有监测站点", "parent_id": None, "type": "root", "childs": []}
        for g in group_lst:
            _node = {"id": g.id, "name": g.group_name, "parent_id": "root", "type": "dept", "childs": []}
            for st in video_lst:
                if st.group_id == g.id:
                    _node["childs"].append({"id": st.id, "name": st.video_name, "parent_id": g.id, "type": "st"})

            if _node["childs"]:
                root_node["childs"].append(_node)
        return sresponse([root_node])
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/video', methods=['POST'])
@bp.auth.grant_view
def video():
    try:
        query = RequestQuery(StVideoBVideoListQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: StVideoBVideoListQuery = query.data

        model = create_st_video_b_model()
        lst = model.get_video_list_query(qd.video_name, qd.group_id).to_list()
        lst = [item for item in lst if item.nvr_mode == "enable"]

        config = current_app.config
        photo_url = config.get('PHOTO_URL', '')
        for item in lst:
            if item.file_name:
                item.file_name = photo_url + item.file_name
        data = StVideoBDetailSchema().dump(lst, many=True)
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/video_transfer', methods=['POST'])
@bp.auth.grant_view
def video_transfer():
    try:
        model = create_st_video_b_model()
        lst = model.get_all().to_list()
        data = []
        for item in lst:
            data.append({"key": item.id, "label": item.video_name, "disabled": False})
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/dp/dp_video_list', methods=['POST'])
@doc.post("dp", "string", [StVideoBVideoListSchema.__name__])
def dp_video_list():
    """视频列表（带经纬度）"""
    try:
        model = create_st_video_b_model()
        lst = model.get_video_list_query("", "*", "*").to_json()
        lst = [item for item in lst if item["nvr_mode"] == "enable"]

        config = current_app.config
        photo_url = config.get('PHOTO_URL', '')
        for item in lst:
            if item.get('file_name', None):
                item['file_name'] = photo_url + item['file_name']
        return sresponse(lst)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()
