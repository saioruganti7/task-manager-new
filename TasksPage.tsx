import { useEffect, useState } from 'react';
import { taskApi, type Task, type Priority } from './taskApi';
export function TasksPage({version,onChanged}:{version:number;onChanged:()=>void}) {
 const [tasks,setTasks]=useState<Task[]>([]);const [title,setTitle]=useState('');const [description,setDescription]=useState('');
 const [priority,setPriority]=useState<Priority>('medium');const [dueDate,setDueDate]=useState('');const [search,setSearch]=useState('');const [error,setError]=useState('');
 async function load(){try{setTasks((await taskApi.list(search)).tasks);setError('')}catch(e){setError((e as Error).message)}}
 useEffect(()=>{void load()},[version,search]);
 async function add(e:React.FormEvent){e.preventDefault();try{await taskApi.create({title,description,priority,due_date:dueDate||null});setTitle('');setDescription('');setDueDate('');await load();onChanged()}catch(e){setError((e as Error).message)}}
 async function edit(t:Task){const next=window.prompt('Edit task title',t.title);if(next===null)return;try{await taskApi.update(t.id,{title:next});await load();onChanged()}catch(e){setError((e as Error).message)}}
 async function remove(t:Task){if(!window.confirm(`Delete "${t.title}"?`))return;try{await taskApi.remove(t.id);await load();onChanged()}catch(e){setError((e as Error).message)}}
 return <section className="space-y-5"><h2 className="heading">Manage tasks</h2>
 <form onSubmit={add} className="card grid gap-3 md:grid-cols-2"><input required maxLength={200} className="field" placeholder="Task title" value={title} onChange={e=>setTitle(e.target.value)}/>
 <input className="field" placeholder="Description" value={description} onChange={e=>setDescription(e.target.value)}/>
 <select className="field" value={priority} onChange={e=>setPriority(e.target.value as Priority)}><option value="low">Low priority</option><option value="medium">Medium priority</option><option value="high">High priority</option></select>
 <input className="field" type="date" value={dueDate} onChange={e=>setDueDate(e.target.value)}/><button className="btn md:col-span-2">Add task</button></form>
 <input className="field" placeholder="Search tasks..." value={search} onChange={e=>setSearch(e.target.value)}/>
 {error&&<p role="alert" className="text-red-600">{error}</p>}
 <div className="space-y-3">{tasks.map(t=><article key={t.id} className="card flex items-start justify-between gap-3"><div><h3 className="font-semibold">{t.title}</h3><p className="text-sm text-slate-600">{t.description}</p><p className="mt-2 text-xs text-slate-500">{t.priority} priority · {t.status.replace('_',' ')} · Due {t.due_date||'not set'}</p></div><div className="flex gap-2"><button className="btn-secondary" onClick={()=>edit(t)}>Edit</button><button className="btn-secondary" onClick={()=>remove(t)}>Delete</button></div></article>)}{tasks.length===0&&<p className="text-slate-500">No tasks found.</p>}</div></section>
}
