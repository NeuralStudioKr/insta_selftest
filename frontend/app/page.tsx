'use client';

import { useState, useEffect } from 'react';
import { getComments, syncComments, getAccounts, createAccount, getInstagramLoginUrl, Account, Comment } from '@/lib/api';
import CommentCard from '@/components/CommentCard';
import styles from './page.module.css';

export default function Home() {
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>('');
  const [syncing, setSyncing] = useState(false);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [selectedAccountId, setSelectedAccountId] = useState<string | null>(null);
  const [showAddAccount, setShowAddAccount] = useState(false);
  const [newAccountName, setNewAccountName] = useState('');
  const [newAccountToken, setNewAccountToken] = useState('');
  const [useOAuth, setUseOAuth] = useState(true); // OAuth 사용 여부

  const loadAccounts = async () => {
    try {
      const data = await getAccounts();
      setAccounts(data);
      if (data.length > 0 && !selectedAccountId) {
        setSelectedAccountId(data[0].id);
      }
    } catch (err: any) {
      console.error('Failed to load accounts:', err);
    }
  };

  const loadComments = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getComments(selectedAccountId || undefined);
      setComments(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || '댓글을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAccounts();
  }, []);

  useEffect(() => {
    if (selectedAccountId) {
      loadComments();
    }
    
    // 30초마다 댓글 새로고침 (폴링)
    const interval = setInterval(() => {
      if (selectedAccountId) {
        loadComments();
      }
    }, 30000);
    
    return () => clearInterval(interval);
  }, [selectedAccountId]);

  const handleSync = async () => {
    if (!selectedAccountId) {
      alert('계정을 선택해주세요.');
      return;
    }
    try {
      setSyncing(true);
      setError(null);
      const result = await syncComments(selectedAccountId, undefined, 10);
      console.log('동기화 완료:', result);
      // 동기화 후 댓글 다시 로드
      await loadComments();
      
      if (result.synced_count === 0) {
        let message = `동기화 완료! ${result.synced_count}개의 댓글을 가져왔습니다.`;
        if (result.message && result.message.includes('No media found')) {
          message += '\n\n⚠️ 중요:\n';
          message += 'Instagram Graph API는 Business Account로 전환된 이후에 올린 게시물만 가져올 수 있습니다.\n\n';
          message += '해결 방법:\n';
          message += '1. Business Account로 전환된 후에 새 게시물을 올리세요\n';
          message += '2. 게시물에 댓글을 달아주세요\n';
          message += '3. 동기화를 다시 시도하세요';
        }
        alert(message);
      } else {
        alert(`동기화 완료! ${result.synced_count}개의 댓글을 가져왔습니다.`);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || '동기화에 실패했습니다.');
    } finally {
      setSyncing(false);
    }
  };

  const handleOAuthLogin = async () => {
    try {
      const { auth_url } = await getInstagramLoginUrl();
      // 새 창에서 Instagram 로그인
      const width = 600;
      const height = 700;
      const left = (window.screen.width - width) / 2;
      const top = (window.screen.height - height) / 2;
      
      const popup = window.open(
        auth_url,
        'Instagram Login',
        `width=${width},height=${height},left=${left},top=${top}`
      );
      
      // OAuth 콜백 메시지 수신
      const messageHandler = (event: MessageEvent) => {
        if (event.data.type === 'instagram_auth_success') {
          loadAccounts();
          setSelectedAccountId(event.data.accountId);
          setShowAddAccount(false);
          alert(`계정이 추가되었습니다: @${event.data.username}`);
          window.removeEventListener('message', messageHandler);
          if (popup) popup.close();
        } else if (event.data.type === 'instagram_auth_error') {
          alert(`로그인 실패: ${event.data.error}`);
          window.removeEventListener('message', messageHandler);
          if (popup) popup.close();
        }
      };
      
      window.addEventListener('message', messageHandler);
      
      // 팝업이 닫혔는지 확인
      const checkClosed = setInterval(() => {
        if (popup?.closed) {
          clearInterval(checkClosed);
          window.removeEventListener('message', messageHandler);
        }
      }, 1000);
      
    } catch (err: any) {
      alert(err.response?.data?.detail || '로그인 URL을 가져오는데 실패했습니다.');
    }
  };

  const handleAddAccount = async () => {
    if (useOAuth) {
      await handleOAuthLogin();
      return;
    }
    
    if (!newAccountName || !newAccountToken) {
      alert('계정 이름과 Access Token을 입력해주세요.');
      return;
    }
    try {
      const account = await createAccount(newAccountName, newAccountToken);
      await loadAccounts();
      setSelectedAccountId(account.id);
      setShowAddAccount(false);
      setNewAccountName('');
      setNewAccountToken('');
      alert('계정이 추가되었습니다.');
    } catch (err: any) {
      alert(err.response?.data?.detail || '계정 추가에 실패했습니다.');
    }
  };

  const filteredComments = filter
    ? comments.filter(
        (comment) =>
          comment.text.toLowerCase().includes(filter.toLowerCase()) ||
          comment.username.toLowerCase().includes(filter.toLowerCase())
      )
    : comments;

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <header className={styles.header}>
          <h1 className={styles.title}>인스타그램 댓글 관리</h1>
          <div className={styles.headerRight}>
            <div className={styles.accountSelector}>
              <label htmlFor="account-select">계정:</label>
              <select
                id="account-select"
                value={selectedAccountId || ''}
                onChange={(e) => setSelectedAccountId(e.target.value)}
                className={styles.accountSelect}
              >
                {accounts.map((account) => (
                  <option key={account.id} value={account.id}>
                    {account.name} {account.username ? `(@${account.username})` : ''}
                  </option>
                ))}
              </select>
              <button
                className={styles.addAccountButton}
                onClick={() => setShowAddAccount(!showAddAccount)}
                title="새 계정 추가"
              >
                +
              </button>
            </div>
            <div className={styles.headerButtons}>
              <button 
                className={styles.syncButton} 
                onClick={handleSync} 
                disabled={syncing || loading || !selectedAccountId}
                title="Instagram에서 최신 댓글 가져오기"
              >
                {syncing ? '동기화 중...' : '📥 동기화'}
              </button>
              <button className={styles.refreshButton} onClick={loadComments} disabled={loading}>
                {loading ? '새로고침 중...' : '🔄 새로고침'}
              </button>
            </div>
          </div>
        </header>

        {showAddAccount && (
          <div className={styles.addAccountForm}>
            <h3>새 계정 추가</h3>
            
            <div className={styles.authMethodSelector}>
              <label>
                <input
                  type="radio"
                  checked={useOAuth}
                  onChange={() => setUseOAuth(true)}
                />
                Instagram으로 로그인 (권장)
              </label>
              <label>
                <input
                  type="radio"
                  checked={!useOAuth}
                  onChange={() => setUseOAuth(false)}
                />
                Access Token 직접 입력
              </label>
            </div>
            
            {useOAuth ? (
              <div className={styles.oauthInfo}>
                <p>Instagram으로 로그인하면 자동으로 계정이 추가됩니다.</p>
                <button onClick={handleAddAccount} className={styles.oauthButton}>
                  📷 Instagram으로 로그인
                </button>
              </div>
            ) : (
              <>
                <input
                  type="text"
                  placeholder="계정 이름"
                  value={newAccountName}
                  onChange={(e) => setNewAccountName(e.target.value)}
                  className={styles.input}
                />
                <input
                  type="text"
                  placeholder="Instagram Access Token"
                  value={newAccountToken}
                  onChange={(e) => setNewAccountToken(e.target.value)}
                  className={styles.input}
                />
              </>
            )}
            
            <div className={styles.addAccountActions}>
              {!useOAuth && (
                <button onClick={handleAddAccount} className={styles.submitButton}>
                  추가
                </button>
              )}
              <button onClick={() => {
                setShowAddAccount(false);
                setNewAccountName('');
                setNewAccountToken('');
              }} className={styles.cancelButton}>
                취소
              </button>
            </div>
          </div>
        )}

        <div className={styles.filters}>
          <input
            type="text"
            placeholder="댓글 검색 (내용, 사용자명)..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className={styles.searchInput}
          />
          <div className={styles.stats}>
            총 {filteredComments.length}개의 댓글
          </div>
        </div>

        {error && <div className={styles.error}>{error}</div>}

        {loading && comments.length === 0 ? (
          <div className={styles.loading}>댓글을 불러오는 중...</div>
        ) : filteredComments.length === 0 ? (
          <div className={styles.empty}>
            {filter ? '검색 결과가 없습니다.' : '댓글이 없습니다.'}
          </div>
        ) : (
          <div className={styles.commentsList}>
            {filteredComments.map((comment) => (
              <CommentCard
                key={comment.id}
                comment={comment}
                onReply={loadComments}
                accountId={selectedAccountId || undefined}
              />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
