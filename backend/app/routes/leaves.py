from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List
from bson import ObjectId
from datetime import datetime
from app.models.leave import LeaveCreate, LeaveResponse, LeaveReview, LeaveStatusEnum
from app.models.user import UserInDB, RoleEnum
from app.dependencies import require_role
from app.database import get_database

router = APIRouter(prefix="/api/leaves", tags=["Leaves"])

@router.post("/", response_model=LeaveResponse, status_code=status.HTTP_201_CREATED)
async def create_leave(
    leave_in: LeaveCreate,
    current_user: UserInDB = Depends(require_role([RoleEnum.employee]))
) -> Any:
    db = get_database()
    
    leave_dict = {
        "employee_id": str(current_user.id),
        "employee_name": current_user.name,
        "start_date": leave_in.start_date,
        "end_date": leave_in.end_date,
        "reason": leave_in.reason,
        "status": LeaveStatusEnum.pending,
        "admin_remarks": "",
        "created_at": datetime.utcnow()
    }
    
    result = await db.leaves.insert_one(leave_dict)
    
    created_leave = await db.leaves.find_one({"_id": result.inserted_id})
    created_leave["id"] = str(created_leave.pop("_id"))
    return LeaveResponse(**created_leave)

@router.get("/employee", response_model=List[LeaveResponse])
async def get_my_leaves(
    current_user: UserInDB = Depends(require_role([RoleEnum.employee]))
) -> Any:
    db = get_database()
    cursor = db.leaves.find({"employee_id": str(current_user.id)}).sort("created_at", -1)
    
    leaves = []
    async for leave in cursor:
        leave["id"] = str(leave.pop("_id"))
        leaves.append(LeaveResponse(**leave))
        
    return leaves

@router.get("/admin", response_model=List[LeaveResponse])
async def get_all_leaves(
    current_user: UserInDB = Depends(require_role([RoleEnum.admin]))
) -> Any:
    db = get_database()
    cursor = db.leaves.find().sort("created_at", -1)
    
    leaves = []
    async for leave in cursor:
        leave["id"] = str(leave.pop("_id"))
        leaves.append(LeaveResponse(**leave))
        
    return leaves

@router.put("/{leave_id}/review", response_model=LeaveResponse)
async def review_leave(
    leave_id: str,
    review_data: LeaveReview,
    current_user: UserInDB = Depends(require_role([RoleEnum.admin]))
) -> Any:
    db = get_database()
    
    try:
        leave_obj_id = ObjectId(leave_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Leave ID format")
        
    leave_doc = await db.leaves.find_one({"_id": leave_obj_id})
    if not leave_doc:
        raise HTTPException(status_code=404, detail="Leave request not found")
        
    if review_data.status not in [LeaveStatusEnum.approved, LeaveStatusEnum.rejected]:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    update_data = {
        "status": review_data.status,
        "admin_remarks": review_data.admin_remarks
    }
    
    await db.leaves.update_one({"_id": leave_obj_id}, {"$set": update_data})
    
    updated_leave = await db.leaves.find_one({"_id": leave_obj_id})
    updated_leave["id"] = str(updated_leave.pop("_id"))
    return LeaveResponse(**updated_leave)
