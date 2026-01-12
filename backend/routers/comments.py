from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from services.storage import storage
from services.instagram_client import InstagramClient
from services.account_manager import account_manager

router = APIRouter()


class ReplyRequest(BaseModel):
    """답글 작성 요청 모델"""
    message: str


class CommentResponse(BaseModel):
    """댓글 응답 모델"""
    id: str
    post_id: Optional[str] = None
    text: str
    username: str
    timestamp: Optional[str] = None
    replies: List[dict] = []
    created_at: Optional[str] = None
    like_count: Optional[int] = 0


@router.get("/comments", response_model=List[CommentResponse])
async def get_comments(
    account_id: Optional[str] = Query(None, description="계정 ID (없으면 기본 계정)"),
    post_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    댓글 목록 조회
    - account_id: 계정 ID (선택사항, 없으면 기본 계정)
    - post_id: 특정 게시물의 댓글만 필터링 (선택사항)
    - limit: 최대 반환 개수
    - offset: 건너뛸 개수
    """
    if account_id and not account_manager.get_account(account_id):
        raise HTTPException(status_code=404, detail="Account not found")
    
    comments = storage.get_all_comments(account_id)
    
    # post_id로 필터링
    if post_id:
        comments = [c for c in comments if c.get("post_id") == post_id]
    
    # 정렬 (최신순)
    comments.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    # 페이지네이션
    paginated_comments = comments[offset:offset + limit]
    
    return paginated_comments


@router.get("/comments/{comment_id}", response_model=CommentResponse)
async def get_comment(
    comment_id: str,
    account_id: Optional[str] = Query(None, description="계정 ID (없으면 기본 계정)")
):
    """특정 댓글 조회"""
    if account_id and not account_manager.get_account(account_id):
        raise HTTPException(status_code=404, detail="Account not found")
    
    comment = storage.get_comment_by_id(comment_id, account_id)
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return comment


@router.post("/comments/{comment_id}/reply")
async def reply_to_comment(
    comment_id: str, 
    reply_request: ReplyRequest,
    account_id: Optional[str] = Query(None, description="계정 ID (없으면 기본 계정)")
):
    """
    댓글에 답글 작성
    인스타그램에 실제로 답글이 게시됩니다.
    """
    if account_id and not account_manager.get_account(account_id):
        raise HTTPException(status_code=404, detail="Account not found")
    
    # 저장소에서 댓글 확인
    comment = storage.get_comment_by_id(comment_id, account_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # 계정의 Access Token 가져오기
    account = account_manager.get_account(account_id or "default")
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    client = InstagramClient(account["access_token"])
    
    # 테스트 댓글인지 확인 (test_로 시작하는 ID는 테스트 댓글)
    is_test_comment = comment_id.startswith("test_")
    
    if is_test_comment:
        # 테스트 댓글의 경우 Instagram API 호출 없이 로컬에만 저장
        from datetime import datetime
        reply_data = {
            "id": f"test_reply_{datetime.utcnow().timestamp()}",
            "text": reply_request.message,
            "username": "me",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        
        saved_reply = storage.add_reply(comment_id, reply_data, account_id)
        
        return {
            "success": True,
            "reply": saved_reply,
            "instagram_id": None,
            "note": "Test comment - reply saved locally only"
        }
    else:
        # 실제 Instagram 댓글의 경우 Instagram API 호출
        try:
            instagram_response = client.reply_to_comment(
                comment_id, 
                reply_request.message
            )
            
            if not instagram_response:
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to post reply to Instagram"
                )
            
            # 저장소에 답글 저장
            reply_data = {
                "id": instagram_response.get("id"),
                "text": reply_request.message,
                "username": "me",  # 현재 사용자
                "timestamp": instagram_response.get("timestamp"),
            }
            
            saved_reply = storage.add_reply(comment_id, reply_data, account_id)
            
            return {
                "success": True,
                "reply": saved_reply,
                "instagram_id": instagram_response.get("id")
            }
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error posting reply: {str(e)}"
            )


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: str,
    account_id: Optional[str] = Query(None, description="계정 ID (없으면 기본 계정)")
):
    """
    댓글 삭제
    인스타그램에서도 댓글이 삭제됩니다.
    """
    if account_id and not account_manager.get_account(account_id):
        raise HTTPException(status_code=404, detail="Account not found")
    
    comment = storage.get_comment_by_id(comment_id, account_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # 계정의 Access Token 가져오기
    account = account_manager.get_account(account_id or "default")
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    client = InstagramClient(account["access_token"])
    
    # 테스트 댓글인지 확인
    is_test_comment = comment_id.startswith("test_")
    
    if is_test_comment:
        # 테스트 댓글의 경우 로컬에서만 삭제
        storage.delete_comment(comment_id, account_id)
        return {"success": True, "message": "Comment deleted (test comment)"}
    else:
        # 실제 Instagram 댓글의 경우 Instagram API 호출
        try:
            deleted = client.delete_comment(comment_id)
            
            if deleted:
                # 저장소에서도 삭제
                storage.delete_comment(comment_id, account_id)
                return {"success": True, "message": "Comment deleted"}
            else:
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to delete comment from Instagram"
                )
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error deleting comment: {str(e)}"
            )


@router.post("/comments/sync")
async def sync_comments(
    account_id: Optional[str] = Query(None, description="계정 ID (없으면 기본 계정)"),
    media_id: Optional[str] = None,
    limit: int = 10
):
    """
    Instagram에서 댓글을 동기화 (폴링 방식)
    - account_id: 계정 ID (선택사항, 없으면 기본 계정)
    - media_id: 특정 미디어의 댓글만 동기화 (없으면 최근 미디어들의 댓글 동기화)
    - limit: 동기화할 미디어 개수 (media_id가 없을 때만 사용)
    """
    try:
        if account_id and not account_manager.get_account(account_id):
            raise HTTPException(status_code=404, detail="Account not found")
        
        # 계정의 Access Token 가져오기
        account = account_manager.get_account(account_id or "default")
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        client = InstagramClient(account["access_token"])
        synced_count = 0
        
        if media_id:
            # 특정 미디어의 댓글만 동기화
            comments = client.get_media_comments(media_id)
            for comment in comments:
                comment_data = {
                    "id": comment.get("id"),
                    "post_id": media_id,
                    "text": comment.get("text", ""),
                    "username": comment.get("username", "unknown"),
                    "timestamp": comment.get("timestamp"),
                    "like_count": comment.get("like_count", 0),
                    "replies": comment.get("replies", {}).get("data", [])
                }
                storage.add_comment(comment_data, account_id)
                synced_count += 1
        else:
            # 사용자의 최근 미디어들의 댓글 동기화
            user_id = client.get_user_id()
            if not user_id:
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to get user ID"
                )
            
            media_list = client.get_user_media(user_id, limit)
            
            if not media_list:
                # 미디어가 없을 때 상세한 메시지 반환
                return {
                    "success": True,
                    "synced_count": 0,
                    "message": "No media found. Please note: Instagram Graph API can only access posts created after converting to Business/Creator Account.",
                    "debug_info": {
                        "user_id": user_id,
                        "media_count": 0,
                        "note": "If you recently posted, the post must be created after the account was converted to Business/Creator Account."
                    }
                }
            
            for media in media_list:
                media_id = media.get("id")
                comments = client.get_media_comments(media_id)
                for comment in comments:
                    comment_data = {
                        "id": comment.get("id"),
                        "post_id": media_id,
                        "text": comment.get("text", ""),
                        "username": comment.get("username", "unknown"),
                        "timestamp": comment.get("timestamp"),
                        "like_count": comment.get("like_count", 0),
                        "replies": comment.get("replies", {}).get("data", [])
                    }
                    storage.add_comment(comment_data, account_id)
                    synced_count += 1
        
        return {
            "success": True,
            "synced_count": synced_count,
            "message": f"Successfully synced {synced_count} comments"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error syncing comments: {str(e)}"
        )
