import { useEffect, useState } from 'react';
import { trackingApi } from './trackingApi';
import type { Task,Status } from '../tasks/taskApi';
export function TrackingPage({version,onChanged}:{version:number;onChanged:()=>void}){
 const [tasks,setTasks]=useState<Task[]>([]);const [filter,setFilter]=useState<'calendar'|'upcoming'|'overdue'>('calendar');const [error,setError]=useState('');
 async function load(){try{setTasks((await trackingApi[filter]()).tasks);setError('')}catch(e){setError((e as Error).message)}}
 useEffect(()=>{void load()},[filter,version]);
 async function change(id:number,status:Status){try{await trackingApi.updateStatus(id,status);await load();onChanged()}catch(e){setError((e as Error).message)}}
 return <section className="space-y-5"><h2 className="heading">Tracking & scheduling</h2><div className="flex gap-2">{(['calendar','upcoming','overdue'] as const).map(f=><button key={f} className={filter===f?'btn':'btn-secondary'} onClick={()=>setFilter(f)}>{f[0].toUpperCase()+f.slice(1)}</button>)}</div>
 {error&&<p role="alert" className="text-red-600">{error}</p>}
 {tasks.map(t=><div key={t.id} className="card flex items-center justify-between gap-3"><div><b>{t.title}</b><p className="text-sm text-slate-500">Due: {t.due_date||'No date'}</p></div><select aria-label={`Status for ${t.title}`} className="field max-w-44" value={t.status} onChange={e=>void change(t.id,e.target.value as Status)}><option value="pending">Pending</option><option value="in_progress">In progress</option><option value="completed">Completed</option></select></div>)}
 {tasks.length===0&&<p className="text-slate-500">No tasks in this view.</p>}</section>
}
