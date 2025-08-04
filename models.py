from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    answers = relationship("Answer", back_populates="user")
    annotations = relationship("Annotation", back_populates="user")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, nullable=False)
    path = Column(String, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    exif_datetime = Column(String)
    exif_gps_lat = Column(Float)
    exif_gps_lon = Column(Float)
    exif_gps_alt = Column(Float)
    exif_camera_make = Column(String)
    exif_camera_model = Column(String)
    exif_lens_model = Column(String)
    exif_focal_length = Column(Float)
    exif_aperture = Column(Float)
    exif_iso = Column(Integer)
    exif_shutter_speed = Column(String)
    exif_orientation = Column(String)
    exif_image_width = Column(Integer)
    exif_image_height = Column(Integer)
    exif_drone_model = Column(String)
    exif_flight_id = Column(String)
    exif_pitch = Column(Float)
    exif_roll = Column(Float)
    exif_yaw = Column(Float)

    answers = relationship("Answer", back_populates="image")
    annotations = relationship("Annotation", back_populates="image")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)

    options = relationship("Option", back_populates="question")
    answers = relationship("Answer", back_populates="question")


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    option_text = Column(Text, nullable=False)

    question = relationship("Question", back_populates="options")
    answers = relationship("Answer", back_populates="selected_option")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("options.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    image = relationship("Image", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    selected_option = relationship("Option", back_populates="answers")
    user = relationship("User", back_populates="answers")


class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    label = Column(String, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    annotated_at = Column(DateTime(timezone=True), server_default=func.now())

    image = relationship("Image", back_populates="annotations")
    user = relationship("User", back_populates="annotations")
