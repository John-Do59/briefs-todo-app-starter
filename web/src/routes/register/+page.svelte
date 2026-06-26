<script lang="ts">
	import { api } from '$lib/api';
	import { goto } from '$app/navigation';

	let username = $state('');
	let email = $state('');
	let password = $state('');
	let avatar_url = $state('');
	let error = $state('');

	async function register(e: Event) {
		e.preventDefault();
		try {
			await api.register({
				username,
				email,
				password,
				avatar_url: avatar_url || null
			});
			goto('/login');
		} catch (err: any) {
			error = err.message || 'Registration failed';
		}
	}
</script>

<div class="mx-auto max-w-sm mt-20 p-6 bg-white rounded-xl shadow-md">
	<h1 class="text-2xl font-bold mb-6 text-center">Register</h1>
	{#if error}
		<div class="bg-red-100 text-red-700 p-3 rounded mb-4 text-sm">{error}</div>
	{/if}
	<form onsubmit={register} class="space-y-4">
		<div>
			<label class="block text-sm font-medium text-gray-700" for="username">Username</label>
			<input id="username" bind:value={username} class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border" required />
		</div>
		<div>
			<label class="block text-sm font-medium text-gray-700" for="email">Email</label>
			<input id="email" type="email" bind:value={email} class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border" required />
		</div>
		<div>
			<label class="block text-sm font-medium text-gray-700" for="password">Password</label>
			<input id="password" type="password" bind:value={password} class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border" required />
		</div>
		<div>
			<label class="block text-sm font-medium text-gray-700" for="avatar">Avatar URL</label>
			<input id="avatar" type="url" bind:value={avatar_url} placeholder="https://..." class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border" />
		</div>
		<button type="submit" class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700">
			Register
		</button>
	</form>
	<p class="mt-4 text-center text-sm">
		Already have an account? <a href="/login" class="text-indigo-600 hover:text-indigo-500">Login</a>
	</p>
</div>
