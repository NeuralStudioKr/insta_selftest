import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from config import settings


class StorageService:
    """JSON 파일 기반 저장소 서비스"""
    
    def __init__(self):
        self.data_dir = settings.data_dir
        self.comments_file = os.path.join(self.data_dir, settings.comments_file)
        self._ensure_data_file()
    
    def _get_comments_file(self, account_id: Optional[str] = None) -> str:
        """계정별 댓글 파일 경로 반환"""
        if account_id and account_id != "default":
            return os.path.join(self.data_dir, f"comments_{account_id}.json")
        return self.comments_file
    
    def _ensure_data_file(self, account_id: Optional[str] = None):
        """데이터 파일이 없으면 생성"""
        comments_file = self._get_comments_file(account_id)
        if not os.path.exists(comments_file):
            os.makedirs(self.data_dir, exist_ok=True)
            with open(comments_file, 'w', encoding='utf-8') as f:
                json.dump({"comments": []}, f, ensure_ascii=False, indent=2)
    
    def _load_data(self, account_id: Optional[str] = None) -> Dict:
        """JSON 파일에서 데이터 로드"""
        comments_file = self._get_comments_file(account_id)
        try:
            with open(comments_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"comments": []}
    
    def _save_data(self, data: Dict, account_id: Optional[str] = None):
        """데이터를 JSON 파일에 저장"""
        comments_file = self._get_comments_file(account_id)
        with open(comments_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_all_comments(self, account_id: Optional[str] = None) -> List[Dict]:
        """모든 댓글 조회"""
        data = self._load_data(account_id)
        return data.get("comments", [])
    
    def get_comment_by_id(self, comment_id: str, account_id: Optional[str] = None) -> Optional[Dict]:
        """ID로 댓글 조회"""
        comments = self.get_all_comments(account_id)
        for comment in comments:
            if comment.get("id") == comment_id:
                return comment
        return None
    
    def add_comment(self, comment: Dict, account_id: Optional[str] = None) -> Dict:
        """새 댓글 추가"""
        data = self._load_data(account_id)
        comments = data.get("comments", [])
        
        # 중복 체크
        comment_id = comment.get("id")
        if comment_id:
            existing = self.get_comment_by_id(comment_id, account_id)
            if existing:
                return existing
        
        # 타임스탬프 추가
        if "created_at" not in comment:
            comment["created_at"] = datetime.utcnow().isoformat() + "Z"
        
        if "replies" not in comment:
            comment["replies"] = []
        
        comments.append(comment)
        data["comments"] = comments
        self._save_data(data, account_id)
        return comment
    
    def update_comment(self, comment_id: str, updates: Dict, account_id: Optional[str] = None) -> Optional[Dict]:
        """댓글 업데이트"""
        data = self._load_data(account_id)
        comments = data.get("comments", [])
        
        for i, comment in enumerate(comments):
            if comment.get("id") == comment_id:
                comments[i].update(updates)
                data["comments"] = comments
                self._save_data(data, account_id)
                return comments[i]
        
        return None
    
    def add_reply(self, comment_id: str, reply: Dict, account_id: Optional[str] = None) -> Optional[Dict]:
        """댓글에 답글 추가"""
        comment = self.get_comment_by_id(comment_id, account_id)
        if not comment:
            return None
        
        if "replies" not in comment:
            comment["replies"] = []
        
        # 답글에 타임스탬프 추가
        if "created_at" not in reply:
            reply["created_at"] = datetime.utcnow().isoformat() + "Z"
        
        comment["replies"].append(reply)
        
        # 업데이트 저장
        data = self._load_data(account_id)
        comments = data.get("comments", [])
        for i, c in enumerate(comments):
            if c.get("id") == comment_id:
                comments[i] = comment
                break
        
        data["comments"] = comments
        self._save_data(data, account_id)
        return reply
    
    def delete_comment(self, comment_id: str, account_id: Optional[str] = None) -> bool:
        """댓글 삭제"""
        data = self._load_data(account_id)
        comments = data.get("comments", [])
        
        original_length = len(comments)
        comments = [c for c in comments if c.get("id") != comment_id]
        
        if len(comments) < original_length:
            data["comments"] = comments
            self._save_data(data, account_id)
            return True
        
        return False


# 싱글톤 인스턴스
storage = StorageService()
