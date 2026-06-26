<script lang="ts">
	import { api } from '$lib/api';
	import { token, currentUser } from '$lib/auth';
	import { goto } from '$app/navigation';

	let username = $state('');
	let password = $state('');
	let error = $state('');

	async function login(e: Event) {
		e.preventDefault();
		try {
			const body = new URLSearchParams();
			body.append('username', username);
			body.append('password', password);
			const res = await api.login(body);
			token.set(res.access_token);
			const user = await api.me();
			currentUser.set(user);
			goto('/');
		} catch (err: any) {
			error = err.message || 'Login failed';
		}
	}
</script>

<div class="mx-auto max-w-sm mt-20 p-6 bg-white rounded-xl shadow-md">
	<h1 class="text-2xl font-bold mb-6 text-center">Login</h1>
	{#if error}
		<div class="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{error}</div>
	{/if}
	<form onsubmit={login} class="space-y-4">
		<div>
			<label class="block text-sm font-medium text-gray-700" for="username">Username</label>
			<input id="username" bind:value={username} class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border" required />
		</div>
		<div>
			<label class="block text-sm font-medium text-gray-700" for="password">Password</label>
			<input id="password" type="password" bind:value={password} class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border" required />
		</div>
		<button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700">
			Sign In
		</button>
	</form>
	<p class="mt-4 text-center text-sm">
		Don't have an account? <a href="/register" class="text-indigo-600 hover:text-indigo-500">Register</a>
	</p>
</div>
