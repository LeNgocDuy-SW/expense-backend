from fastapi import APIRouter, Depends, HTTPException
from database.database import engine
from auth_helpers import get_current_user 
from model.monthlybill import MonthlyBillCreate, MonthlyBill, MonthlyBillRead
from model.user import User
from datetime import datetime, timezone
from sqlmodel import Session, select

router = APIRouter(prefix = "/bills", tags=["bill"])

@router.post("", response_model = MonthlyBillRead)
def create_bill(data: MonthlyBillCreate, current_user : User = Depends(get_current_user)):
    if not current_user.room_id:
        raise HTTPException(status_code=400, detail="Bạn chưa tham gia phòng nào")
    bill = MonthlyBill.model_validate(data)
    now = datetime.now(timezone.utc)
    bill.month = now.month
    bill.year = now.year
    bill.room_id = current_user.room_id
    with Session(engine) as session:
        session.add(bill)
        session.commit()
        session.refresh(bill)
        return bill

@router.get("", response_model = list[MonthlyBillRead])
def get_bills(current_user : User = Depends(get_current_user)):
    if not current_user.room_id:
        return []
    with Session(engine) as session:
        return session.exec(select(MonthlyBill).where(MonthlyBill.room_id == current_user.room_id)).all()

@router.get("/{id}",  response_model = MonthlyBillRead)
def get_bill(id: int, current_user : User = Depends(get_current_user)):
    with Session(engine) as session:
        bill = session.get(MonthlyBill, id)
        if not bill or bill.room_id != current_user.room_id: 
                    raise HTTPException(status_code = 404, detail = "Không tìm thấy")
        return bill
        
@router.put("/{id}", response_model = MonthlyBillRead)
def update_bill(id: int, data: MonthlyBillCreate, current_user : User = Depends(get_current_user)):
    with Session(engine) as session:
        bill = session.get(MonthlyBill, id)
        if not bill or bill.room_id != current_user.room_id: 
            raise HTTPException(status_code = 404, detail = "Không tìm thấy")
        now = datetime.now(timezone.utc)
        if (bill.month != now.month or bill.year != now.year) and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Chỉ được sửa/xóa hóa đơn của tháng hiện tại")
        bill.electricity_quantity = data.electricity_quantity
        bill.water_quantity = data.water_quantity
        bill.rent_amount = data.rent_amount
        bill.other_amount = data.other_amount
        bill.wifi_amount = data.wifi_amount
        bill.parking_amount = data.parking_amount
        bill.electricity_price = data.electricity_price
        bill.water_price = data.water_price
        session.add(bill)
        session.commit()
        session.refresh(bill)
        return bill

@router.delete("/{id}")
def delete_bill(id: int, current_user : User = Depends(get_current_user)):
    with Session(engine) as session:
        bill = session.get(MonthlyBill, id)

        if not bill or bill.room_id != current_user.room_id:
            raise HTTPException(status_code = 404, detail = "Không tìm thấy")
        now = datetime.now(timezone.utc)
        if (bill.month != now.month or bill.year != now.year) and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Chỉ được sửa/xóa hóa đơn của tháng hiện tại")
        session.delete(bill)
        session.commit()
        return {"message": "Đã xóa"}

    