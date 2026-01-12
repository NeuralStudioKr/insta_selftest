import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from config import settings


class AccountManager:
    """Instagram 계정 관리 서비스"""
    
    def __init__(self):
        self.data_dir = settings.data_dir
        self.accounts_file = os.path.join(self.data_dir, "accounts.json")
        self._ensure_accounts_file()
    
    def _ensure_accounts_file(self):
        """계정 파일이 없으면 생성"""
        if not os.path.exists(self.accounts_file):
            os.makedirs(self.data_dir, exist_ok=True)
            # 기본 계정 추가 (기존 .env의 토큰 사용)
            default_account = {
                "id": "default",
                "name": "기본 계정",
                "access_token": settings.instagram_access_token,
                "user_id": None,
                "username": None,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "is_active": True
            }
            with open(self.accounts_file, 'w', encoding='utf-8') as f:
                json.dump({"accounts": [default_account]}, f, ensure_ascii=False, indent=2)
    
    def _load_accounts(self) -> Dict:
        """계정 데이터 로드"""
        try:
            with open(self.accounts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"accounts": []}
    
    def _save_accounts(self, data: Dict):
        """계정 데이터 저장"""
        with open(self.accounts_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_all_accounts(self) -> List[Dict]:
        """모든 계정 조회"""
        data = self._load_accounts()
        return data.get("accounts", [])
    
    def get_account(self, account_id: str) -> Optional[Dict]:
        """특정 계정 조회"""
        accounts = self.get_all_accounts()
        for account in accounts:
            if account.get("id") == account_id:
                return account
        return None
    
    def add_account(self, name: str, access_token: str, user_id: Optional[str] = None, username: Optional[str] = None) -> Dict:
        """새 계정 추가"""
        data = self._load_accounts()
        accounts = data.get("accounts", [])
        
        # 계정 ID 생성
        account_id = f"account_{len(accounts) + 1}"
        
        new_account = {
            "id": account_id,
            "name": name,
            "access_token": access_token,
            "user_id": user_id,
            "username": username,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "is_active": True
        }
        
        accounts.append(new_account)
        data["accounts"] = accounts
        self._save_accounts(data)
        
        return new_account
    
    def update_account(self, account_id: str, updates: Dict) -> Optional[Dict]:
        """계정 정보 업데이트"""
        data = self._load_accounts()
        accounts = data.get("accounts", [])
        
        for i, account in enumerate(accounts):
            if account.get("id") == account_id:
                accounts[i].update(updates)
                data["accounts"] = accounts
                self._save_accounts(data)
                return accounts[i]
        
        return None
    
    def delete_account(self, account_id: str) -> bool:
        """계정 삭제 (기본 계정은 삭제 불가)"""
        if account_id == "default":
            return False
        
        data = self._load_accounts()
        accounts = data.get("accounts", [])
        
        original_length = len(accounts)
        accounts = [a for a in accounts if a.get("id") != account_id]
        
        if len(accounts) < original_length:
            data["accounts"] = accounts
            self._save_accounts(data)
            return True
        
        return False
    
    def get_active_accounts(self) -> List[Dict]:
        """활성 계정만 조회"""
        accounts = self.get_all_accounts()
        return [a for a in accounts if a.get("is_active", True)]


# 싱글톤 인스턴스
account_manager = AccountManager()
