from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import RedirectResponse
from typing import Optional
import httpx
import secrets
from config import settings
from services.account_manager import account_manager
from services.instagram_client import InstagramClient
import os

router = APIRouter()

# OAuth 상태 저장 (실제로는 세션이나 DB에 저장해야 함)
oauth_states = {}


@router.get("/auth/instagram")
async def instagram_login():
    """
    Instagram OAuth 로그인 시작
    사용자를 Instagram 로그인 페이지로 리디렉션
    """
    if not settings.instagram_app_id:
        raise HTTPException(
            status_code=500,
            detail="Instagram App ID not configured. Please set INSTAGRAM_APP_ID in .env"
        )
    
    # CSRF 방지를 위한 state 생성
    state = secrets.token_urlsafe(32)
    oauth_states[state] = True
    
    # Facebook OAuth URL 생성 (Instagram은 Facebook OAuth 사용)
    redirect_uri = settings.oauth_redirect_uri
    scope = "instagram_basic,instagram_manage_comments,pages_read_engagement,instagram_content_publish"
    
    auth_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth"
        f"?client_id={settings.instagram_app_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        f"&response_type=code"
        f"&state={state}"
    )
    
    return RedirectResponse(url=auth_url)


@router.get("/auth/instagram/callback")
async def instagram_callback(
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    error_reason: Optional[str] = Query(None)
):
    """
    Instagram OAuth 콜백
    인증 코드를 Access Token으로 교환
    """
    # 에러 처리
    if error:
        error_msg = f"Instagram 로그인 실패: {error}"
        if error_reason:
            error_msg += f" ({error_reason})"
        return f"""
        <html>
            <body>
                <h1>로그인 실패</h1>
                <p>{error_msg}</p>
                <script>
                    window.opener.postMessage({{type: 'instagram_auth_error', error: '{error}'}}, '*');
                    window.close();
                </script>
            </body>
        </html>
        """
    
    if not code:
        return """
        <html>
            <body>
                <h1>로그인 실패</h1>
                <p>인증 코드를 받지 못했습니다.</p>
                <script>
                    window.opener.postMessage({type: 'instagram_auth_error', error: 'no_code'}, '*');
                    window.close();
                </script>
            </body>
        </html>
        """
    
    # State 검증
    if not state or state not in oauth_states:
        return """
        <html>
            <body>
                <h1>보안 오류</h1>
                <p>잘못된 요청입니다.</p>
                <script>
                    window.opener.postMessage({type: 'instagram_auth_error', error: 'invalid_state'}, '*');
                    window.close();
                </script>
            </body>
        </html>
        """
    
    oauth_states.pop(state, None)
    
    try:
        # Access Token 교환 (Facebook OAuth 사용)
        token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
        token_params = {
            "client_id": settings.instagram_app_id,
            "client_secret": settings.instagram_app_secret,
            "redirect_uri": settings.oauth_redirect_uri,
            "code": code
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(token_url, params=token_params)
            
            if response.status_code != 200:
                error_data = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                error_msg = error_data.get("error_message", "Access token 교환 실패")
                return f"""
                <html>
                    <body>
                        <h1>토큰 교환 실패</h1>
                        <p>{error_msg}</p>
                        <script>
                            window.opener.postMessage({{type: 'instagram_auth_error', error: '{error_msg}'}}, '*');
                            window.close();
                        </script>
                    </body>
                </html>
                """
            
            token_response = response.json()
            access_token = token_response.get("access_token")
            user_id = token_response.get("user_id")
            
            if not access_token:
                return """
                <html>
                    <body>
                        <h1>토큰 받기 실패</h1>
                        <p>Access Token을 받지 못했습니다.</p>
                        <script>
                            window.opener.postMessage({type: 'instagram_auth_error', error: 'no_token'}, '*');
                            window.close();
                        </script>
                    </body>
                </html>
                """
            
            # Facebook Pages를 통해 Instagram Business Account 찾기
            pages_url = "https://graph.facebook.com/v18.0/me/accounts"
            pages_params = {"access_token": access_token}
            
            instagram_user_id = None
            instagram_username = None
            final_access_token = access_token
            
            async with httpx.AsyncClient() as http_client:
                pages_response = await http_client.get(pages_url, params=pages_params)
                
                if pages_response.status_code == 200:
                    pages_data = pages_response.json()
                    if pages_data.get("data"):
                        # 첫 번째 Page의 Instagram Business Account 찾기
                        for page in pages_data["data"]:
                            page_id = page.get("id")
                            page_token = page.get("access_token")
                            
                            # Page의 Instagram Business Account 가져오기
                            page_info_url = f"https://graph.facebook.com/v18.0/{page_id}"
                            page_info_params = {
                                "access_token": page_token,
                                "fields": "instagram_business_account"
                            }
                            page_info_response = await http_client.get(page_info_url, params=page_info_params)
                            
                            if page_info_response.status_code == 200:
                                page_info = page_info_response.json()
                                ig_account = page_info.get("instagram_business_account")
                                if ig_account:
                                    ig_user_id = ig_account.get("id")
                                    # Instagram Account 정보 가져오기
                                    ig_info_url = f"https://graph.facebook.com/v18.0/{ig_user_id}"
                                    ig_info_params = {
                                        "access_token": page_token,
                                        "fields": "id,username"
                                    }
                                    ig_info_response = await http_client.get(ig_info_url, params=ig_info_params)
                                    
                                    if ig_info_response.status_code == 200:
                                        ig_info = ig_info_response.json()
                                        instagram_user_id = ig_info.get("id")
                                        instagram_username = ig_info.get("username", "unknown")
                                        final_access_token = page_token  # Page Token 사용
                                        break
                
                # Instagram Account를 찾지 못한 경우 직접 시도
                if not instagram_user_id:
                    try:
                        instagram_client = InstagramClient(access_token)
                        user_info = instagram_client._make_request("GET", "me", {"fields": "id,username"})
                        instagram_user_id = user_info.get("id")
                        instagram_username = user_info.get("username", "unknown")
                    except:
                        # Instagram Graph API 직접 사용 불가시 Facebook User 정보 사용
                        user_url = "https://graph.facebook.com/v18.0/me"
                        user_response = await http_client.get(user_url, params={"access_token": access_token})
                        if user_response.status_code == 200:
                            fb_user = user_response.json()
                            instagram_user_id = fb_user.get("id")
                            instagram_username = fb_user.get("name", "unknown")
                        else:
                            raise Exception("Failed to get user info")
            
            # 계정 추가 또는 업데이트
            account_name = f"{instagram_username}의 계정" if instagram_username else "Instagram 계정"
            existing_account = None
            for acc in account_manager.get_all_accounts():
                if acc.get("user_id") == instagram_user_id or acc.get("username") == instagram_username:
                    existing_account = acc
                    break
            
            if existing_account:
                # 기존 계정 업데이트
                account_manager.update_account(existing_account["id"], {
                    "access_token": final_access_token,
                    "username": instagram_username,
                    "user_id": instagram_user_id
                })
                account_id = existing_account["id"]
            else:
                # 새 계정 추가
                account = account_manager.add_account(
                    name=account_name,
                    access_token=final_access_token,
                    user_id=instagram_user_id,
                    username=instagram_username
                )
                account_id = account["id"]
            
            # 성공 메시지와 함께 프론트엔드로 전달
            return f"""
            <html>
                <body>
                    <h1>로그인 성공!</h1>
                    <p>계정이 추가되었습니다: @{instagram_username or 'unknown'}</p>
                    <script>
                        window.opener.postMessage({{
                            type: 'instagram_auth_success',
                            accountId: '{account_id}',
                            username: '{instagram_username or 'unknown'}'
                        }}, '*');
                        window.close();
                    </script>
                </body>
            </html>
            """
    
    except Exception as e:
        import traceback
        error_detail = str(e)
        traceback.print_exc()
        return f"""
        <html>
            <body>
                <h1>오류 발생</h1>
                <p>{error_detail}</p>
                <script>
                    window.opener.postMessage({{type: 'instagram_auth_error', error: '{error_detail}'}}, '*');
                    window.close();
                </script>
            </body>
        </html>
        """


@router.get("/auth/instagram/url")
async def get_instagram_login_url():
    """Instagram 로그인 URL 반환 (프론트엔드에서 사용)"""
    if not settings.instagram_app_id:
        raise HTTPException(
            status_code=500,
            detail="Instagram App ID not configured. Please set INSTAGRAM_APP_ID in .env"
        )
    
    state = secrets.token_urlsafe(32)
    oauth_states[state] = True
    
    redirect_uri = settings.oauth_redirect_uri
    # Instagram Graph API 권한 (Facebook OAuth를 통해야 함)
    scope = "instagram_basic,instagram_manage_comments,pages_read_engagement,instagram_content_publish,pages_show_list"
    
    # Facebook OAuth 사용 (Instagram은 Facebook OAuth를 통해야 함)
    auth_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth"
        f"?client_id={settings.instagram_app_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
        f"&response_type=code"
        f"&state={state}"
    )
    
    return {
        "auth_url": auth_url, 
        "state": state,
        "app_id": settings.instagram_app_id,
        "redirect_uri": redirect_uri,
        "debug_info": "Meta App 대시보드에서 App ID와 리디렉션 URI를 확인하세요"
    }
