from model.user import User
from model.purchase import Purchase
from model.monthlybill import MonthlyBill
from sqlmodel import select, Session, func
from database.database import engine
from fastapi import APIRouter, Depends, HTTPException
from auth_helpers import get_current_user

router = APIRouter(prefix= "/settlement", tags=["settlement"])

@router.get("")
def get_settlement(current_user :User = Depends(get_current_user)):
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        purchases = session.exec(select(Purchase)).all()
        bills = session.exec(select(MonthlyBill)).all()

        user_total = len(users)
        
        purchase_total = sum(p.amount for p in purchases)

        bill_total = sum(
            b.rent_amount + b.electricity_quantity * b.electricity_price
            + b.water_quantity * b.water_price + b.other_amount
            + b.wifi_amount + b.parking_amount
            for b in bills
        )       

        total = purchase_total + bill_total
        if len(users) == 0:
            return {"message": "Chưa có người dùng nào"}
        moi_nguoi_phai_tra = total / user_total

        ket_qua = []
        for u in users:
            da_tra = sum(p.amount for p in purchases if p.buyer_id == u.id)
            so_du = da_tra - moi_nguoi_phai_tra
            ket_qua.append({
                "username": u.username,
                "da_tra": da_tra,
                "phai_tra": moi_nguoi_phai_tra,
                "so_du": so_du,
            })
        return {
            "tong_chi_tieu": total,
            "moi_nguoi_phai_tra": moi_nguoi_phai_tra,
            "chi_tiet": ket_qua,
        }
