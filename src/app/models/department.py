from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func

from db import Base

class Department(Base):
    __tablename__ = 'department'

    id: Mapped[int] = mapped_column(Integer, 
                                    primary_key=True,  
                                    nullable=False)
    name: Mapped[str] = mapped_column(String(200), 
                                      nullable=False)
    parent_id: Mapped[int | None] = mapped_column(Integer, 
                                           ForeignKey('department.id'), 
                                           nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, 
                                                server_default=func.now(),
                                                nullable=False)

    employees: Mapped[list["Employee"]] = relationship("Employee", 
                                                       back_populates='department',
                                                       cascade='all, delete-orphan')
    children: Mapped[list['Department']] = relationship('Department', 
                                                        back_populates='parent',
                                                        cascade='all, delete-orphan')
    parent: Mapped['Department | None'] = relationship('Department', 
                                                        back_populates='children',
                                                        cascade='all, delete-orphan')
    