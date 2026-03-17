from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime
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

    def to_dict(self):
        """
        @Brief: Function returns the values from the db in a dict format
        @Param: self - Instance of the class
        @Return: res - A dictionary of the request
        """
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "completed" : self.completed,
            "created_at" : self.created_at.isoformat(),
            "updated_at" : self.updated_at.isoformat() if self.updated_at else None
        }

