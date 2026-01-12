#!/usr/bin/env python3
"""
댓글 동기화 스크립트
주기적으로 Instagram 댓글을 가져와서 저장합니다.
"""
import sys
import os
import time
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from services.instagram_client import instagram_client
from services.storage import storage


def sync_all_comments(limit: int = 10):
    """모든 미디어의 댓글 동기화"""
    print("댓글 동기화 시작...")
    
    try:
        user_id = instagram_client.get_user_id()
        if not user_id:
            print("❌ 사용자 ID를 가져올 수 없습니다.")
            return False
        
        print(f"✅ 사용자 ID: {user_id}")
        
        # 미디어 목록 가져오기
        media_list = instagram_client.get_user_media(user_id, limit)
        print(f"✅ {len(media_list)}개의 미디어를 찾았습니다.")
        
        total_synced = 0
        for i, media in enumerate(media_list, 1):
            media_id = media.get("id")
            print(f"\n[{i}/{len(media_list)}] 미디어 ID: {media_id}")
            
            # 댓글 가져오기
            comments = instagram_client.get_media_comments(media_id)
            print(f"  - {len(comments)}개의 댓글 발견")
            
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
                storage.add_comment(comment_data)
                total_synced += 1
                print(f"  ✓ 댓글 저장: @{comment_data['username']} - {comment_data['text'][:30]}...")
        
        print(f"\n✅ 동기화 완료! 총 {total_synced}개의 댓글을 저장했습니다.")
        return True
    
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False


def sync_loop(interval: int = 300):
    """주기적으로 댓글 동기화 (폴링)"""
    print(f"댓글 동기화 루프 시작 (간격: {interval}초)")
    print("Ctrl+C를 눌러 종료하세요.\n")
    
    try:
        while True:
            sync_all_comments()
            print(f"\n다음 동기화까지 {interval}초 대기...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n동기화 루프를 종료합니다.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Instagram 댓글 동기화 스크립트")
    parser.add_argument(
        "--once",
        action="store_true",
        help="한 번만 실행 (루프 없이)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="동기화 간격 (초, 기본값: 300)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="동기화할 최근 미디어 개수 (기본값: 10)"
    )
    
    args = parser.parse_args()
    
    if args.once:
        sync_all_comments(args.limit)
    else:
        sync_loop(args.interval)
