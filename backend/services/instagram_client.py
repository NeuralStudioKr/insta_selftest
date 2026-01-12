import httpx
from typing import Dict, List, Optional
from config import settings


class InstagramClient:
    """Instagram Graph API 클라이언트"""
    
    BASE_URL = "https://graph.instagram.com"
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token or settings.instagram_access_token
        self.base_url = self.BASE_URL
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict:
        """API 요청 실행"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        request_params = {"access_token": self.access_token}
        if params:
            request_params.update(params)
        
        with httpx.Client() as client:
            if method.upper() == "GET":
                response = client.get(url, params=request_params)
            elif method.upper() == "POST":
                response = client.post(url, params=request_params, json=data)
            elif method.upper() == "DELETE":
                response = client.delete(url, params=request_params)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
    
    def get_media_comments(self, media_id: str) -> List[Dict]:
        """미디어의 댓글 목록 조회"""
        try:
            response = self._make_request("GET", f"{media_id}/comments", {
                "fields": "id,text,username,timestamp,like_count,replies"
            })
            return response.get("data", [])
        except Exception as e:
            print(f"Error fetching comments: {e}")
            return []
    
    def get_comment(self, comment_id: str) -> Optional[Dict]:
        """특정 댓글 조회"""
        try:
            response = self._make_request("GET", comment_id, {
                "fields": "id,text,username,timestamp,like_count,replies"
            })
            return response
        except Exception as e:
            print(f"Error fetching comment: {e}")
            return None
    
    def reply_to_comment(self, comment_id: str, message: str) -> Optional[Dict]:
        """댓글에 답글 작성"""
        try:
            response = self._make_request(
                "POST",
                f"{comment_id}/replies",
                data={"message": message}
            )
            return response
        except Exception as e:
            print(f"Error replying to comment: {e}")
            return None
    
    def delete_comment(self, comment_id: str) -> bool:
        """댓글 삭제"""
        try:
            self._make_request("DELETE", comment_id)
            return True
        except Exception as e:
            print(f"Error deleting comment: {e}")
            return False
    
    def get_media_info(self, media_id: str) -> Optional[Dict]:
        """미디어 정보 조회"""
        try:
            response = self._make_request("GET", media_id, {
                "fields": "id,caption,media_type,media_url,permalink,timestamp"
            })
            return response
        except Exception as e:
            print(f"Error fetching media info: {e}")
            return None
    
    def get_user_media(self, user_id: str, limit: int = 25) -> List[Dict]:
        """사용자의 미디어 목록 조회"""
        try:
            # 여러 필드 조합 시도
            response = self._make_request("GET", f"{user_id}/media", {
                "fields": "id,caption,media_type,media_url,permalink,timestamp,thumbnail_url",
                "limit": limit
            })
            media_list = response.get("data", [])
            
            # 디버깅 정보 출력
            if not media_list:
                print(f"⚠️  미디어가 없습니다. User ID: {user_id}")
                print(f"   응답: {response}")
                print(f"   참고: Instagram Graph API는 Business Account로 전환된 이후에 올린 게시물만 가져올 수 있습니다.")
                print(f"   또한 게시물이 공개 상태여야 하며, 스토리/릴스는 다른 엔드포인트를 사용합니다.")
            
            return media_list
        except Exception as e:
            print(f"Error fetching user media: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_user_id(self) -> Optional[str]:
        """현재 사용자(계정) ID 조회"""
        try:
            response = self._make_request("GET", "me", {
                "fields": "id,username"
            })
            return response.get("id")
        except Exception as e:
            print(f"Error fetching user ID: {e}")
            return None


# 싱글톤 인스턴스
instagram_client = InstagramClient()
