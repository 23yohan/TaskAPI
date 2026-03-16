from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Boolean, PrimaryKeyConstraint, Column, DateTime
from datetime import datetime as dt
from datetime import timezone as tz
from app import db

class Tasks(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int]           = mapped_column(Integer, primary_key=True)
    title: Mapped[str]        = mapped_column(String, nullable=False)
    description: Mapped[str]  = mapped_column(String, nullable=True)
    completed: Mapped[bool]   = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[dt]    = mapped_column(DateTime(timezone=True), 
                                            default=lambda: dt.now(tz.utc), 
                                            nullable=False)
    updated_at: Mapped[dt]    = mapped_column(DateTime(timezone=True), 
                                            onupdate=lambda: dt.now(tz.utc), 
                                            nullable=True)

