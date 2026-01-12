from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.account_manager import account_manager
from services.instagram_client import InstagramClient

router = APIRouter()


class AccountCreateRequest(BaseModel):
    """계정 생성 요청 모델"""
    name: str
    access_token: str


class AccountResponse(BaseModel):
    """계정 응답 모델"""
    id: str
    name: str
    user_id: Optional[str] = None
    username: Optional[str] = None
    created_at: str
    is_active: bool


@router.get("/accounts", response_model=List[AccountResponse])
async def get_accounts():
    """모든 계정 조회"""
    accounts = account_manager.get_all_accounts()
    # Access Token은 보안상 제외
    for account in accounts:
        account.pop("access_token", None)
    return accounts


@router.get("/accounts/{account_id}", response_model=AccountResponse)
async def get_account(account_id: str):
    """특정 계정 조회"""
    account = account_manager.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Access Token은 보안상 제외
    account.pop("access_token", None)
    return account


@router.post("/accounts")
async def create_account(account_request: AccountCreateRequest):
    """새 계정 추가"""
    try:
        # Access Token으로 사용자 정보 확인
        client = InstagramClient(account_request.access_token)
        user_info = client._make_request("GET", "me", {"fields": "id,username"})
        
        account = account_manager.add_account(
            name=account_request.name,
            access_token=account_request.access_token,
            user_id=user_info.get("id"),
            username=user_info.get("username")
        )
        
        # Access Token은 보안상 제외
        account.pop("access_token", None)
        return account
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid access token or failed to verify account: {str(e)}"
        )


@router.delete("/accounts/{account_id}")
async def delete_account(account_id: str):
    """계정 삭제"""
    if account_id == "default":
        raise HTTPException(
            status_code=400,
            detail="Cannot delete default account"
        )
    
    deleted = account_manager.delete_account(account_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return {"success": True, "message": "Account deleted"}
