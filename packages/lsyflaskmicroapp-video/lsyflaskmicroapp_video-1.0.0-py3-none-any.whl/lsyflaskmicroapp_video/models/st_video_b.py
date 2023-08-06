# -*- coding: utf-8 -*-

from typing import List, Tuple

import sqlalchemy as sa
from lsyflasksdkcore.exceptions import DBError, DBRefError
from lsyflasksdkcore.model import DBResult, DBRef
from lsyflasksdkcore.schema import DBRefSchema
from marshmallow import ValidationError
from sqlalchemy import orm
from sqlalchemy.exc import SQLAlchemyError

from ..entitys.st_video_b import StVideoBBase, StVideoBEdit, StVideoBDetail, StVideoBVideoList
from ..models.st_video_image_r import StVideoImageRModel
from ..orm import db, model, StVideoB, StVideoImageR, StVideoGroupB
from ..schemas.st_video_b import StVideoBSchema, StVideoBDetailSchema, StVideoBVideoListSchema


class StVideoBModel(object):
    """ 视频基本信息表 Model
    """

    columns = [StVideoB.id, StVideoB.video_code, StVideoB.video_name, StVideoB.group_id, StVideoB.video_url,
               StVideoB.video_type, StVideoB.is_controllable, StVideoB.control_api_url, StVideoB.device_serial,
               StVideoB.channel_no, StVideoB.bit_type, StVideoB.ys_app_key, StVideoB.ys_app_secret,
               StVideoB.nvr_app, StVideoB.nvr_name, StVideoB.nvr_mode, StVideoB.nvr_edge,
               StVideoB.order_number, StVideoB.lgtd, StVideoB.lttd]

    def __init__(self):
        self.session = db.session
        """:type: sqlalchemy.orm.Session"""

    @staticmethod
    def _get_sorted(sort: str, order: str):
        if sort and order:
            return getattr(getattr(StVideoB, sort), order)()
        return None

    @model.entity(StVideoBSchema)
    def get_one(self, _id: str) -> DBResult[StVideoBBase]:
        try:
            return self.session.query(StVideoB).filter(StVideoB.id == _id).first()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_one error,error:{ex}")

    @model.list(StVideoBSchema)
    def get_all(self, sort: str = None, order: str = None) -> DBResult[StVideoBBase]:
        try:
            q = self.session.query(StVideoB)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_all error,error:{ex}")

    @model.list(StVideoBSchema)
    def get_list_group_id(self, group_id: str, sort=None, order=None) -> DBResult[StVideoBBase]:
        try:
            q = self.session.query(StVideoB).filter(StVideoB.group_id == group_id)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_list_group_id error,error:{ex}")

    @model.list(DBRefSchema)
    def get_refer(self, _id: str) -> DBResult[DBRef]:
        try:
            q_stvideoimager = self.session.query(sa.literal('StVideoImageR').label('ref_code'),
                                                 sa.literal(u'视频截图表').label('ref_desc'),
                                                 sa.func.count('*').label('ref_count')).select_from(
                StVideoImageR).filter(StVideoImageR.video_id == _id)

            q = sa.union_all(q_stvideoimager)
            t = orm.aliased(q)
            rows = self.session.query(t).filter(t.c.ref_count > 0).all()
            return rows
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_refer error,error:{ex}")

    def add(self, entity: StVideoBEdit):
        try:
            schema = StVideoBSchema()
            d = schema.dump(entity)
            row = StVideoB(**d)
            self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"add validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"add error,error:{ex}")

    def modify(self, _id: str, entity: StVideoBEdit):
        try:
            schema = StVideoBSchema()
            d = schema.dump(entity)
            self.session.query(StVideoB).filter(StVideoB.id == _id).update(d)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"modify validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_import error,error:{ex}")

    def delete(self, _id: str):
        refs = self.get_refer(_id).to_list()
        if refs:
            raise DBRefError(refs.pop())

        try:
            self.session.query(StVideoB).filter(StVideoB.id == _id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete error,error:{ex}")

    def delete_group_id(self, group_id: str):
        try:
            self.session.query(StVideoB).filter(StVideoB.group_id == group_id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete_group_id error,error:{ex}")

    def tran_import(self, lst: List[StVideoBBase]):
        try:
            for entity in lst:
                schema = StVideoBSchema()
                d = schema.dump(entity)
                row = StVideoB(**d)
                self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            self.session.rollback()
            raise DBError(f"tran_import validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_import error,error:{ex}")

    def tran_delete(self, pks: List[str]):
        for pk in pks:
            refs = self.get_refer(pk).to_list()
            if refs:
                raise DBRefError(refs.pop())

        try:
            self.session.query(StVideoB).filter(
                StVideoB.id.in_(pks)).delete(synchronize_session=False)

            self.session.commit()
        except ValidationError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")

    @model.pager(StVideoBDetailSchema)
    def get_page_query(self, video_name, group_id, limit: int, offset: int) -> Tuple[DBResult[StVideoBDetail], int]:
        try:
            columns = self.columns
            q = self.session.query(*columns, StVideoGroupB.group_name).select_from(StVideoB) \
                .outerjoin(StVideoGroupB, StVideoB.group_id == StVideoGroupB.id) \
                .filter(StVideoB.video_name.contains(video_name))

            if group_id != "*":
                q = q.filter(StVideoB.group_id == group_id)

            rows = None
            count = q.count()
            if count > 0:
                q = q.order_by(StVideoB.order_number.desc())
                rows = q.limit(limit).offset(offset).all()
            return rows, count
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_page_query error,error:{ex}")

    @model.list(StVideoBVideoListSchema)
    def get_video_list_query(self, video_name='*', group_id='*', domains='*') -> DBResult[StVideoBVideoList]:
        try:
            columns = self.columns
            q_latest = StVideoImageRModel.subquery_latest(session=self.session)

            q = self.session.query(*columns, StVideoGroupB.group_name, StVideoGroupB.id.label('group_id'),
                                   q_latest.c.tm, q_latest.c.image_name, q_latest.c.file_name,
                                   q_latest.c.file_dir, ) \
                .select_from(StVideoB) \
                .outerjoin(q_latest, StVideoB.id == q_latest.c.ph_id) \
                .outerjoin(StVideoGroupB, StVideoGroupB.id == StVideoB.group_id)
            if video_name != '*':
                q = q.filter(StVideoB.video_name.contains(video_name))

            if group_id != "*":
                q = q.filter(StVideoB.group_id == group_id)
            if domains != '*':
                q = q.filter(StVideoB.id.in_(domains))
            q = q.order_by(StVideoB.order_number.desc())
            rows = q.all()
            return rows
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_video_list_query error,error:{ex}")
