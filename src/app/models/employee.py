from datetime import datetime, date
from sqlalchemy import String, Integer, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from db import Base
from .department import Department

class Employee(Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(Integer, 
                                    primary_key=True,  
                                    nullable=False)
    department_id: Mapped[int] = mapped_column(Integer, 
                                                ForeignKey('department.id'),
                                                nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), 
                                           nullable=False)
    position: Mapped[str] = mapped_column(String(200),
                                          nullable=False)
    hired_at: Mapped[date | None] = mapped_column(Date, 
                                                    nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, 
                                                 server_default=func.now(),
                                                 nullable=False)

    departmen: Mapped['Department'] = relationship('Department', 
                                                   back_populates="employees")
