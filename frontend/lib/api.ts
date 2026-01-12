import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Comment {
  id: string;
  post_id?: string;
  text: string;
  username: string;
  timestamp?: string;
  replies?: Reply[];
  created_at?: string;
  like_count?: number;
}

export interface Reply {
  id: string;
  text: string;
  username: string;
  timestamp?: string;
  created_at?: string;
}

export interface ReplyRequest {
  message: string;
}

export interface Account {
  id: string;
  name: string;
  user_id?: string;
  username?: string;
  created_at: string;
  is_active: boolean;
}

// 계정 목록 조회
export async function getAccounts(): Promise<Account[]> {
  const response = await api.get('/api/accounts');
  return response.data;
}

// 계정 추가 (Access Token 직접 입력)
export async function createAccount(name: string, accessToken: string): Promise<Account> {
  const response = await api.post('/api/accounts', { name, access_token: accessToken });
  return response.data;
}

// Instagram OAuth 로그인 URL 가져오기
export async function getInstagramLoginUrl(): Promise<{ auth_url: string; state: string }> {
  const response = await api.get('/api/auth/instagram/url');
  return response.data;
}

// 계정 삭제
export async function deleteAccount(accountId: string): Promise<void> {
  await api.delete(`/api/accounts/${accountId}`);
}

// 댓글 목록 조회
export async function getComments(accountId?: string, postId?: string, limit = 100, offset = 0): Promise<Comment[]> {
  const params: any = { limit, offset };
  if (accountId) {
    params.account_id = accountId;
  }
  if (postId) {
    params.post_id = postId;
  }
  
  const response = await api.get('/api/comments', { params });
  return response.data;
}

// 특정 댓글 조회
export async function getComment(commentId: string, accountId?: string): Promise<Comment> {
  const params: any = {};
  if (accountId) {
    params.account_id = accountId;
  }
  const response = await api.get(`/api/comments/${commentId}`, { params });
  return response.data;
}

// 댓글에 답글 작성
export async function replyToComment(commentId: string, message: string, accountId?: string): Promise<any> {
  const params: any = {};
  if (accountId) {
    params.account_id = accountId;
  }
  const response = await api.post(`/api/comments/${commentId}/reply`, { message }, { params });
  return response.data;
}

// 댓글 삭제
export async function deleteComment(commentId: string, accountId?: string): Promise<void> {
  const params: any = {};
  if (accountId) {
    params.account_id = accountId;
  }
  await api.delete(`/api/comments/${commentId}`, { params });
}

// 댓글 동기화 (폴링)
export async function syncComments(accountId?: string, mediaId?: string, limit = 10): Promise<any> {
  const params: any = { limit };
  if (accountId) {
    params.account_id = accountId;
  }
  if (mediaId) {
    params.media_id = mediaId;
  }
  
  const response = await api.post('/api/comments/sync', null, { params });
  return response.data;
}
