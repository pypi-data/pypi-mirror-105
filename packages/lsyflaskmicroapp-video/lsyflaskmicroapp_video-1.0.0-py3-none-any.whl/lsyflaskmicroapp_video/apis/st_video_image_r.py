# -*- coding: utf-8 -*-

"""
St_Video_Image_R
~~~~~~~~~~~~~
视频截图表
"""

import logging

from lsyflasksdkcore import RequestQuery, eresponse, sresponse, PkQuerySchema
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.schema import PksQuerySchema, PksQuery, PkQuery
from lsyflasksdkcore.utils.unique import get_uuid_str
from werkzeug.exceptions import InternalServerError

from ..entitys.st_video_image_r import StVideoImageRPagerQuery, StVideoImageREdit
from ..models import create_st_video_image_r_model
from ..schemas.st_video_image_r import StVideoImageRPagerQuerySchema, StVideoImageREditSchema

logger = logging.getLogger(__name__)

bp = Blueprint('st_video_image_r', __name__)


@bp.route('/page', methods=['GET', 'POST'])
@bp.auth.grant_view
def page():
    try:
        query = RequestQuery(StVideoImageRPagerQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: StVideoImageRPagerQuery = query.data

        model = create_st_video_image_r_model()
        dbr, count = model.get_page_query("", qd.rows, qd.offset)
        return sresponse(dbr.json, total=count)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/add', methods=['POST'])
@bp.auth.grant_add
def add():
    try:
        query = RequestQuery(StVideoImageREditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: StVideoImageREdit = query.data
        entity.id = get_uuid_str()
        model = create_st_video_image_r_model()
        model.add(entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/modify', methods=['POST'])
@bp.auth.grant_edit
def modify():
    try:
        query = RequestQuery(StVideoImageREditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: StVideoImageREdit = query.data
        model = create_st_video_image_r_model()
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
        model = create_st_video_image_r_model()
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
        model = create_st_video_image_r_model()
        data = model.get_detail(qd.id).json
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()
