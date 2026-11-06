import { api } from '../../shared/api';
export type User = { id: number; name: string; email: string };
export const authApi = {
  me: () => api<{user:User}>('/auth/me'),
  login: (email:string,password:string) => api<{user:User}>('/auth/login',{method:'POST',body:JSON.stringify({email,password})}),
  register: (name:string,email:string,password:string) => api<{user:User}>('/auth/register',{method:'POST',body:JSON.stringify({name,email,password})}),
  logout: () => api('/auth/logout',{method:'POST'}),
  updateProfile: (name:string) => api<{user:User}>('/auth/profile',{method:'PATCH',body:JSON.stringify({name})}),
};
