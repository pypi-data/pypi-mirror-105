# -*- coding: utf-8 -*-

from typing import List, Tuple

import sqlalchemy as sa
from lsyflasksdkcore.exceptions import DBError, DBRefError
from lsyflasksdkcore.model import DBResult, DBRef
from lsyflasksdkcore.schema import DBRefSchema
from marshmallow import ValidationError
from sqlalchemy import orm
from sqlalchemy.exc import SQLAlchemyError

from ..entitys.st_video_group_b import StVideoGroupBBase, StVideoGroupBEdit
from ..orm import db, model, StVideoGroupB, StVideoB
from ..schemas.st_video_group_b import StVideoGroupBSchema


class StVideoGroupBModel(object):
    """ 视频分组表 Model
    """

    def __init__(self):
        self.session = db.session
        """:type: sqlalchemy.orm.Session"""
        # self.columns = [VideoGroupB.id, VideoGroupB.group_name, VideoGroupB.order_number]

    @staticmethod
    def _get_sorted(sort: str, order: str):
        if sort and order:
            return getattr(getattr(StVideoGroupB, sort), order)()
        return None

    @model.entity(StVideoGroupBSchema)
    def get_one(self, _id: str) -> DBResult[StVideoGroupBBase]:
        try:
            return self.session.query(StVideoGroupB).filter(StVideoGroupB.id == _id).first()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_one error,error:{ex}")

    @model.list(StVideoGroupBSchema)
    def get_all(self, sort: str = None, order: str = None) -> DBResult[StVideoGroupBBase]:
        try:
            q = self.session.query(StVideoGroupB)
            _sorted = self._get_sorted(sort, order)
            if _sorted is not None:
                q = q.order_by(_sorted)
            return q.all()
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_all error,error:{ex}")

    @model.list(DBRefSchema)
    def get_refer(self, _id: str) -> DBResult[DBRef]:
        try:
            q_stvideob = self.session.query(sa.literal('StVideoB').label('ref_code'),
                                            sa.literal(u'视频基本信息表').label('ref_desc'),
                                            sa.func.count('*').label('ref_count')).select_from(StVideoB).filter(
                StVideoB.group_id == _id)
            q = sa.union_all(q_stvideob)
            t = orm.aliased(q)
            rows = self.session.query(t).filter(t.c.ref_count > 0).all()
            return rows
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_refer error,error:{ex}")

    def add(self, entity: StVideoGroupBEdit):
        try:
            schema = StVideoGroupBSchema()
            d = schema.dump(entity)
            row = StVideoGroupB(**d)
            self.session.add(row)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"add validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"add error,error:{ex}")

    def modify(self, _id: str, entity: StVideoGroupBEdit):
        try:
            schema = StVideoGroupBSchema()
            d = schema.dump(entity)
            self.session.query(StVideoGroupB).filter(StVideoGroupB.id == _id).update(d)
            self.session.commit()
        except ValidationError as ex:
            raise DBError(f"modify validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"modify error,error:{ex}")

    def delete(self, _id: str):
        refs = self.get_refer(_id).to_list()
        if refs:
            raise DBRefError(refs.pop())
        try:
            self.session.query(StVideoGroupB).filter(StVideoGroupB.id == _id).delete()
            self.session.commit()
        except ValidationError as ex:
            self.session.rollback()
            raise DBError(f"delete validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"delete error,error:{ex}")

    def tran_import(self, lst: List[StVideoGroupBBase]):
        try:
            for entity in lst:
                schema = StVideoGroupBSchema()
                d = schema.dump(entity)
                row = StVideoGroupB(**d)
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
            self.session.query(StVideoGroupB).filter(
                StVideoGroupB.id.in_(pks)).delete(synchronize_session=False)
            self.session.commit()
        except ValidationError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete validation,error:{ex}")
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"tran_delete error,error:{ex}")

    @model.pager(StVideoGroupBSchema)
    def get_page_query(self, group_name, limit: int, offset: int) -> Tuple[List[StVideoGroupBBase], int]:
        try:
            q = self.session.query(StVideoGroupB).filter(StVideoGroupB.group_name.contains(group_name))

            rows = None
            count = q.count()
            if count > 0:
                q = q.order_by(StVideoGroupB.order_number.asc())
                rows = q.limit(limit).offset(offset).all()
            return rows, count
        except SQLAlchemyError as ex:
            self.session.rollback()
            raise DBError(f"get_page_query error,error:{ex}")
