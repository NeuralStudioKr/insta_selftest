'use client';

import { useState } from 'react';
import { Comment, Reply } from '@/lib/api';
import { replyToComment } from '@/lib/api';
import styles from './CommentCard.module.css';

interface CommentCardProps {
  comment: Comment;
  onReply?: () => void;
  accountId?: string;
}

export default function CommentCard({ comment, onReply, accountId }: CommentCardProps) {
  const [isReplying, setIsReplying] = useState(false);
  const [replyText, setReplyText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    try {
      const date = new Date(dateString);
      return date.toLocaleString('ko-KR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return dateString;
    }
  };

  const handleReply = async () => {
    if (!replyText.trim()) {
      setError('답글 내용을 입력해주세요.');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      await replyToComment(comment.id, replyText, accountId);
      setReplyText('');
      setIsReplying(false);
      if (onReply) {
        onReply();
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || '답글 작성에 실패했습니다.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={styles.commentCard}>
      <div className={styles.commentHeader}>
        <div className={styles.userInfo}>
          <span className={styles.username}>@{comment.username}</span>
          {comment.like_count !== undefined && comment.like_count > 0 && (
            <span className={styles.likeCount}>❤️ {comment.like_count}</span>
          )}
        </div>
        {comment.created_at && (
          <span className={styles.timestamp}>{formatDate(comment.created_at)}</span>
        )}
      </div>

      <div className={styles.commentText}>{comment.text}</div>

      {comment.replies && comment.replies.length > 0 && (
        <div className={styles.replies}>
          {comment.replies.map((reply: Reply) => (
            <div key={reply.id} className={styles.reply}>
              <span className={styles.replyUsername}>@{reply.username}</span>
              <span className={styles.replyText}>{reply.text}</span>
            </div>
          ))}
        </div>
      )}

      {!isReplying ? (
        <button
          className={styles.replyButton}
          onClick={() => setIsReplying(true)}
        >
          답글 작성
        </button>
      ) : (
        <div className={styles.replyForm}>
          <textarea
            className={styles.replyTextarea}
            value={replyText}
            onChange={(e) => setReplyText(e.target.value)}
            placeholder="답글을 입력하세요..."
            rows={3}
          />
          {error && <div className={styles.error}>{error}</div>}
          <div className={styles.replyActions}>
            <button
              className={styles.cancelButton}
              onClick={() => {
                setIsReplying(false);
                setReplyText('');
                setError(null);
              }}
              disabled={isSubmitting}
            >
              취소
            </button>
            <button
              className={styles.submitButton}
              onClick={handleReply}
              disabled={isSubmitting || !replyText.trim()}
            >
              {isSubmitting ? '작성 중...' : '작성'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
