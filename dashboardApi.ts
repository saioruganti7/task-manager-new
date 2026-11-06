import { api } from '../../shared/api';
import type { Task } from '../tasks/taskApi';
export type Summary={total:number;pending:number;in_progress:number;completed:number;overdue:number;completion_percentage:number};
export const dashboardApi={
 summary:()=>api<Summary>('/dashboard/summary'),
 priorities:()=>api<{counts:Record<string,number>}>('/dashboard/priorities'),
 weekly:()=>api<{days:{date:string;completed:number}[]}>('/dashboard/weekly'),
 recent:()=>api<{tasks:Task[]}>('/dashboard/recent'),
};
