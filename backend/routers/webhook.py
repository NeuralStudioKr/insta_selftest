from fastapi import APIRouter, Request, Response, HTTPException, Header
from typing import Optional
import hmac
import hashlib
import json
from config import settings
from services.storage import storage
from services.instagram_client import instagram_client

router = APIRouter()


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """웹훅 서명 검증"""
    expected_signature = hmac.new(
        settings.instagram_app_secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)


@router.get("/webhook")
async def verify_webhook(
    hub_mode: Optional[str] = None,
    hub_verify_token: Optional[str] = None,
    hub_challenge: Optional[str] = None
):
    """
    Meta 웹훅 검증 엔드포인트
    Meta는 웹훅 설정 시 이 엔드포인트를 호출하여 검증합니다.
    """
    if hub_mode == "subscribe" and hub_verify_token == settings.webhook_verify_token:
        return Response(content=hub_challenge, media_type="text/plain")
    else:
        raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def handle_webhook(request: Request, x_hub_signature_256: Optional[str] = Header(None)):
    """
    Meta 웹훅 이벤트 수신 엔드포인트
    인스타그램에서 댓글이 달리면 이 엔드포인트로 이벤트가 전송됩니다.
    """
    try:
        body = await request.body()
        
        # 서명 검증 (선택사항, 보안 강화용)
        if x_hub_signature_256:
            if not verify_webhook_signature(body, x_hub_signature_256):
                raise HTTPException(status_code=403, detail="Invalid signature")
        
        data = json.loads(body.decode('utf-8'))
        
        # 웹훅 이벤트 처리
        if "entry" in data:
            for entry in data["entry"]:
                # 댓글 이벤트 처리
                if "changes" in entry:
                    for change in entry["changes"]:
                        if change.get("field") == "comments":
                            value = change.get("value", {})
                            
                            # 새 댓글 추가
                            if "text" in value:
                                comment_data = {
                                    "id": value.get("id"),
                                    "post_id": value.get("media_id") or entry.get("id"),
                                    "text": value.get("text"),
                                    "username": value.get("from", {}).get("username", "unknown"),
                                    "timestamp": value.get("created_time"),
                                    "replies": []
                                }
                                
                                # 저장소에 저장
                                storage.add_comment(comment_data)
                                
                                # Instagram API에서 상세 정보 가져오기 (선택사항)
                                if comment_data["id"]:
                                    try:
                                        detailed_comment = instagram_client.get_comment(comment_data["id"])
                                        if detailed_comment:
                                            comment_data.update({
                                                "like_count": detailed_comment.get("like_count", 0),
                                                "replies": detailed_comment.get("replies", {}).get("data", [])
                                            })
                                            storage.update_comment(comment_data["id"], comment_data)
                                    except Exception as e:
                                        print(f"Error fetching detailed comment: {e}")
        
        return {"status": "ok"}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        print(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
