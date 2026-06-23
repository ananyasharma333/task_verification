from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class LeaveStatusEnum(str, Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"

class LeaveBase(BaseModel):
    employee_id: str
    employee_name: str
    start_date: str
    end_date: str
    reason: str
    status: LeaveStatusEnum = LeaveStatusEnum.pending
    admin_remarks: Optional[str] = ""

class LeaveCreate(BaseModel):
    start_date: str
    end_date: str
    reason: str

class LeaveReview(BaseModel):
    status: LeaveStatusEnum
    admin_remarks: Optional[str] = ""

class LeaveResponse(LeaveBase):
    id: str = Field(alias="_id")
    created_at: datetime
    
    class Config:
        populate_by_name = True
