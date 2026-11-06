import { useEffect,useState } from 'react';
import { dashboardApi,type Summary } from './dashboardApi';
export function DashboardPage({version}:{version:number}){
 const [summary,setSummary]=useState<Summary|null>(null);const [weekly,setWeekly]=useState<{date:string;completed:number}[]>([]);const [priorities,setPriorities]=useState<Record<string,number>>({});const [error,setError]=useState('');
 useEffect(()=>{Promise.all([dashboardApi.summary(),dashboardApi.weekly(),dashboardApi.priorities()]).then(([s,w,p])=>{setSummary(s);setWeekly(w.days);setPriorities(p.counts);setError('')}).catch(e=>setError((e as Error).message))},[version]);
 return <section className="space-y-5"><h2 className="heading">Dashboard</h2>{error&&<p role="alert" className="text-red-600">{error}</p>}
 <div className="grid grid-cols-2 gap-3 md:grid-cols-3">{summary&&Object.entries(summary).map(([k,v])=><div className="card" key={k}><p className="text-sm capitalize text-slate-500">{k.replaceAll('_',' ')}</p><p className="mt-1 text-3xl font-bold text-indigo-700">{v}{k==='completion_percentage'?'%':''}</p></div>)}</div>
 <div className="grid gap-4 md:grid-cols-2"><div className="card"><h3 className="mb-4 font-semibold">Completed tasks · last 7 days</h3><div className="flex h-44 items-end gap-3">{weekly.map(d=><div key={d.date} className="flex flex-1 flex-col items-center gap-1"><span className="text-xs">{d.completed}</span><div className="w-full rounded-t bg-indigo-500" style={{height:`${Math.max(5,d.completed*25)}px`}}/><span className="text-xs text-slate-500">{d.date.slice(5)}</span></div>)}</div></div>
 <div className="card"><h3 className="mb-4 font-semibold">Tasks by priority</h3>{['high','medium','low'].map(p=><div key={p} className="mb-3 flex justify-between border-b pb-2 capitalize"><span>{p}</span><b>{priorities[p]||0}</b></div>)}</div></div></section>
}
