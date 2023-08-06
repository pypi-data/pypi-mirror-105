# -*- coding: utf-8 -*-


from typing import List

import sqlalchemy as sa
from lsyflasksdkcore.exceptions import DBError
from lsyflasksdkcore.model import DBResult
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from ..entitys.st_video_image_r import StVideoImageRBase, StVideoImageREdit
from ..orm import db, model, StVideoImageR
from ..schemas.st_video_image_r import StVideoImageRSchema


class StVideoImageRModel(object):
    """ 视频截图表 Model
    """

    # columns
    columns = [StVideoImageR.id, StVideoImageR.video_id, StVideoImageR.tm, StVideoImageR.file_dir,
               StVideoImageR.file_name, StVideoImageR.image_name, StVideoImageR.remark]

    def __init__(self):
        self.session = db.session
        """:type: sqlalchemy.orm.Session"""
        # self.columns = [StVideoImageR.id, StVideoImageR.video_id, StVideoImageR.tm, StVideoImageR.file_dir, StVideoImageR.file_name, StVideoImageR.image_name, StVideoImageR.remark]

    @staticmethod
    def _get_sorted(sort: str, order: str):
        if sort and order:
            return getattr(getattr(StVideoImageR, sort), order)()
        return None

    @staticmethod
    def subquery_latest(session):
        ph_query = session.query(StVideoImageR.video_id, sa.func.max(StVideoImageR.tm).label('max_tm')). \
            select_from(StVideoImageR). \
            group_by(StVideoImageR.video_id). \
            subquery()

        ph_group = session.query(StVideoImageR.tm, StVideoImageR.image_name, StVideoImageR.file_name,
                                 StVideoImageR.file_dir, StVideoImageR.video_id.label('ph_id')). \
            select_from(StVideoImageR). \
            join(ph_query,
                 sa.and_(StVideoImageR.video_id == ph_query.c.video_id, StVideoImageR.tm == ph_query.c.max_tm)). \
            subquery()
        return ph_group

    @model.entity(StVideoImageRSchema)
    def get_one(self, _id: str) -> DBResult[StVideoImageRBase]:
        try:
            return self.session.query(StVideoImageR).filter(StVideoImageR.id == _id).first()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_one error,error:{ex}")

    @model.list(StVideoImageRSchema)
    def get_all(self, sort: str = None, order: str = None) -> DBResult[StVideoImageRBase]:
        try:
            q = self.session.query(StVideoImageR)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_all error,error:{ex}")

    @model.list(StVideoImageRSchema)
    def get_list_video_id(self, video_id: str, sort=None, order=None) -> DBResult[StVideoImageRBase]:
        try:
            query = self.session.query(StVideoImageR).filter(StVideoImageR.video_id == video_id)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                query = query.order_by(_sorted)
            return query.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_list_video_id error,error:{ex}")

    def add(self, entity: StVideoImageREdit):
        try:
            schema = StVideoImageRSchema()
            d = schema.dump(entity)
            row = StVideoImageR(**d)
            self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"add validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"add error,error:{ex}")

    def modify(self, _id: str, entity: StVideoImageREdit):
        try:
            schema = StVideoImageRSchema()
            d = schema.dump(entity)
            self.session.query(StVideoImageR).filter(StVideoImageR.id == _id).update(d)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"modify validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"modify error,error:{ex}")

    def delete(self, _id: str):
        try:
            self.session.query(StVideoImageR).filter(StVideoImageR.id == _id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete error,error:{ex}")

    def delete_video_id(self, video_id: str):
        try:
            self.session.query(StVideoImageR).filter(StVideoImageR.video_id == video_id).delete()
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete_video_id error,error:{ex}")

    def tran_delete(self, pks: List[str]):
        try:
            self.session.query(StVideoImageR).filter(
                StVideoImageR.id.in_(pks)).delete(synchronize_session=False)
            self.session.commit()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")
