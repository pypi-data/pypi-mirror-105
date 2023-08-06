# -*- coding: utf-8 -*-

"""
St_Video_Group_B
~~~~~~~~~~~~~
视频分组表
"""

import logging

from lsyflasksdkcore import RequestQuery, eresponse, sresponse, PkQuerySchema
from lsyflasksdkcore.blueprints import Blueprint
from lsyflasksdkcore.schema import PksQuerySchema, PksQuery, PkQuery
from werkzeug.exceptions import InternalServerError

from ..entitys.st_video_group_b import StVideoGroupBPagerQuery, StVideoGroupBEdit
from ..models import create_video_group_b_model
from ..schemas.st_video_group_b import StVideoGroupBPagerQuerySchema, StVideoGroupBEditSchema

logger = logging.getLogger(__name__)

bp = Blueprint('st_video_group_b', __name__)


@bp.route('/page', methods=['GET', 'POST'])
@bp.auth.grant_view
def page():
    try:
        query = RequestQuery(StVideoGroupBPagerQuerySchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        qd: StVideoGroupBPagerQuery = query.data

        model = create_video_group_b_model()
        dbr, count = model.get_page_query(qd.group_name, qd.rows, qd.offset)
        return sresponse(dbr.json, total=count)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/add', methods=['POST'])
@bp.auth.grant_add
def add():
    try:
        query = RequestQuery(StVideoGroupBEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: StVideoGroupBEdit = query.data
        model = create_video_group_b_model()
        model.add(entity)
        return sresponse()
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/modify', methods=['POST'])
@bp.auth.grant_edit
def modify():
    try:
        query = RequestQuery(StVideoGroupBEditSchema)
        if not query.is_valid():
            return eresponse(query.valid_message)

        entity: StVideoGroupBEdit = query.data
        model = create_video_group_b_model()
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
        model = create_video_group_b_model()
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
        model = create_video_group_b_model()
        data = model.get_detail(qd.id).json
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()


@bp.route('/all', methods=['GET', 'POST'])
@bp.auth.grant_view
def all():
    try:
        model = create_video_group_b_model()
        data = model.get_all("order_number", "asc").json
        return sresponse(data)
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError()
