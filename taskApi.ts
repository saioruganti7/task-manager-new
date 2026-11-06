import { api } from '../../shared/api';
export type Status = 'pending'|'in_progress'|'completed';
export type Priority = 'low'|'medium'|'high';
export type Task = {id:number;title:string;description:string;priority:Priority;status:Status;due_date:string|null;created_at:string;completed_at:string|null};
export type TaskInput = {title:string;description:string;priority:Priority;due_date:string|null};
export const taskApi={
 list:(search='')=>api<{tasks:Task[]}>(`/tasks?search=${encodeURIComponent(search)}`),
 create:(data:TaskInput)=>api<{task:Task}>('/tasks',{method:'POST',body:JSON.stringify(data)}),
 update:(id:number,data:Partial<TaskInput>)=>api<{task:Task}>(`/tasks/${id}`,{method:'PATCH',body:JSON.stringify(data)}),
 remove:(id:number)=>api<void>(`/tasks/${id}`,{method:'DELETE'}),
};
