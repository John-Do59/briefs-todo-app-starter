export interface Todo {
	id: number;
	title: string;
	description: string | null;
	completed: boolean;
	owner_id: number | null;
	assignee_id: number | null;
	assignee: User | null;
	created_at: string;
	updated_at: string | null;
}

export interface User {
	id: number;
	username: string;
	email: string;
	avatar_url: string | null;
}

export interface AuthResponse {
	access_token: string;
	token_type: string;
}

export interface TodoCreate {
	title: string;
	description?: string | null;
	completed?: boolean;
}

export interface TodoUpdate {
	title?: string;
	description?: string | null;
	completed?: boolean;
	assignee_id?: number | null;
}

export type Filter = 'all' | 'active' | 'completed';
