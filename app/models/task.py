from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
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
    created_by : Mapped[int]  = mapped_column("created_by", Integer, ForeignKey("users.user_id"), nullable=False)
    assigned_to : Mapped[int]  = mapped_column("assigned_to", Integer, ForeignKey("users.user_id"), nullable=True)

    creator = relationship("Users", foreign_keys=[created_by], backref="created_tasks")
    assignee = relationship("Users", foreign_keys=[assigned_to], backref="assigned_tasks")

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
            "updated_at" : self.updated_at.isoformat() if self.updated_at else None,
            "created_by" : self.created_by,
            "assigned_to": self.assigned_to if self.assigned_to else None
        }

