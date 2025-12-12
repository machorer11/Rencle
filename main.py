from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PayRequest(BaseModel):
    method: str
    distance_km: int
    amount: int
    details: dict = {}

class PayResponse(BaseModel):
    success: bool
    message: str

@app.post("/pay", response_model=PayResponse)
async def pay(req: PayRequest):
    # デモ: 実際の決済処理はここに実装
    print("受信:", req.dict())
    if req.amount <= 0:
        return PayResponse(success=False, message="金額が不正です")
    return PayResponse(success=True, message="支払いシミュレーション成功")