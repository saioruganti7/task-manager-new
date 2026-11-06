import { useState } from 'react';
import { authApi, type User } from './authApi';
export function AuthPage({onLogin}:{onLogin:(u:User)=>void}) {
 const [mode,setMode]=useState<'login'|'register'>('login');
 const [name,setName]=useState(''); const [email,setEmail]=useState(''); const [password,setPassword]=useState('');
 const [error,setError]=useState(''); const [busy,setBusy]=useState(false);
 async function submit(e:React.FormEvent) {e.preventDefault();setBusy(true);setError('');try{
   const r=mode==='login'?await authApi.login(email,password):await authApi.register(name,email,password);onLogin(r.user);
 }catch(e){setError((e as Error).message)}finally{setBusy(false)}}
 return <main className="mx-auto mt-20 max-w-md rounded-2xl bg-white p-8 shadow-lg">
  <h1 className="text-3xl font-bold text-indigo-700">TaskFlow</h1><p className="mb-6 text-slate-500">{mode==='login'?'Sign in to your workspace':'Create your account'}</p>
  <form onSubmit={submit} className="space-y-4">
   {mode==='register'&&<input required className="field" placeholder="Full name" value={name} onChange={e=>setName(e.target.value)}/>}
   <input required type="email" className="field" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)}/>
   <input required type="password" minLength={mode==='register'?8:undefined} className="field" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)}/>
   {error&&<p role="alert" className="text-red-600">{error}</p>}
   <button disabled={busy} className="btn w-full">{busy?'Please wait...':mode==='login'?'Sign in':'Register'}</button>
  </form>
  <button className="mt-4 text-indigo-700 underline" onClick={()=>{setMode(mode==='login'?'register':'login');setError('')}}>{mode==='login'?'Create an account':'Already registered? Sign in'}</button>
 </main>
}
