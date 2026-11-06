import { api } from '../../shared/api';
import type { Task, Status } from '../tasks/taskApi';
export const trackingApi={
 upcoming:()=>api<{tasks:Task[]}>('/tracking/upcoming'),
 overdue:()=>api<{tasks:Task[]}>('/tracking/overdue'),
 calendar:()=>api<{tasks:Task[]}>('/tracking/calendar'),
 updateStatus:(id:number,status:Status)=>api<{task:Task}>(`/tasks/${id}/status`,{method:'PATCH',body:JSON.stringify({status})}),
};
