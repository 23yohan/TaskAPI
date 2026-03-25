from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime
from datetime import datetime as dt
from datetime import timezone as tz
from app import db

# TODO: Could look to make email a primary key since i dont want duplicate emails in table
class Users(db.Model):
    __tablename__ = "users"
    
    userId : Mapped[int]    = mapped_column("user_id", Integer, primary_key=True)
    firstName : Mapped[str] = mapped_column("first_name", String, nullable=True)
    lastName : Mapped[str]  = mapped_column("last_name", String, nullable=True)
    email : Mapped[str]     = mapped_column("email", String, nullable=True, unique=True)
    password : Mapped[str]  = mapped_column("password", String, nullable=True)
    active : Mapped[bool]   = mapped_column("active", Boolean, nullable=False, default=True)
    createdAt: Mapped[dt]   = mapped_column("created_at", DateTime, nullable=False, default=lambda: dt.now(tz.utc))
    deleteDate : Mapped[dt] = mapped_column("delete_date", DateTime, nullable=True)

    def to_dict(self):
        return {
            "user_id"    : self.userId,
            "first_name" : self.firstName,
            "last_name"  : self.lastName,
            "email"      : self.email,
            "password"   : self.password,
            "active"     : self.active,
            "created_at" : self.createdAt,
            "deleteDate" : self.deleteDate
        }