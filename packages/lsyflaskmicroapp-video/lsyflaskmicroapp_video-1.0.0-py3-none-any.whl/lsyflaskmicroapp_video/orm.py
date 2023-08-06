from flask_sqlalchemy import SQLAlchemy
from lsyflasksdkcore.model import Model
from sqlalchemy import Column, String, ForeignKey, DateTime, SmallInteger, Text, Integer, Numeric
from sqlalchemy.orm import relationship

db = SQLAlchemy()
model = Model()


def init_db(app):
    db.init_app(app)
    model.init_app(app)


class StVideoB(db.Model):
    __tablename__ = 'st_video_b'

    id = Column(String, primary_key=True)
    video_code = Column(String(20), nullable=False)
    video_name = Column(String(20), nullable=False)
    group_id = Column(ForeignKey('st_video_group_b.id', ondelete='RESTRICT', onupdate='RESTRICT'))
    video_url = Column(Text, nullable=False)
    video_type = Column(String(10), nullable=False)
    is_controllable = Column(SmallInteger, nullable=False)
    control_api_url = Column(Text)
    device_serial = Column(Text)
    channel_no = Column(String(50))
    bit_type = Column(SmallInteger)
    ys_app_key = Column(Text)
    ys_app_secret = Column(Text)
    nvr_app = Column(String(20), nullable=False)
    nvr_name = Column(String(20), nullable=False)
    nvr_mode = Column(String(20), nullable=False)
    nvr_edge = Column(Text)
    order_number = Column(Integer)
    lgtd = Column(Numeric)
    lttd = Column(Numeric)

    group = relationship('StVideoGroupB')


class StVideoImageR(db.Model):
    __tablename__ = 'st_video_image_r'

    id = Column(String, primary_key=True)
    video_id = Column(ForeignKey('st_video_b.id', ondelete='RESTRICT', onupdate='RESTRICT'))
    tm = Column(DateTime, nullable=False)
    file_dir = Column(Text, nullable=False)
    file_name = Column(Text, nullable=False)
    image_name = Column(Text, nullable=False)
    remark = Column(Text)

    video = relationship('StVideoB')


class StVideoGroupB(db.Model):
    __tablename__ = 'st_video_group_b'

    id = Column(String, primary_key=True)
    group_name = Column(String(20), nullable=False)
    order_number = Column(Integer)
