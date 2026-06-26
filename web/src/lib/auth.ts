import { browser } from '$app/environment';
import { writable } from 'svelte/store';
import type { User } from './types';

export const token = writable<string | null>(browser ? localStorage.getItem('token') : null);
export const currentUser = writable<User | null>(null);

if (browser) {
	token.subscribe((v) => {
		if (v) {
			localStorage.setItem('token', v);
		} else {
			localStorage.removeItem('token');
		}
	});
}

export function logout() {
	token.set(null);
	currentUser.set(null);
}
