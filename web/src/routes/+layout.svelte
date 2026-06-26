<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';
	import { api } from '$lib/api';
	import { token, currentUser, logout } from '$lib/auth';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	let { children } = $props();
	let initialized = $state(false);

	onMount(async () => {
		const currentToken = get(token);
		if (currentToken) {
			try {
				const user = await api.me();
				currentUser.set(user);
			} catch (e) {
				logout();
				if ($page.url.pathname !== '/login' && $page.url.pathname !== '/register') {
					goto('/login');
				}
			}
		} else {
			if ($page.url.pathname !== '/login' && $page.url.pathname !== '/register') {
				goto('/login');
			}
		}
		initialized = true;
	});

	let user = $derived($currentUser);
</script>

{#if initialized}
	{#if user}
		<nav class="bg-indigo-600 text-white p-4 flex justify-between items-center shadow-md">
			<div class="font-bold text-xl"><a href="/">To-Do App</a></div>
			<div class="flex items-center gap-4">
				<div class="flex items-center gap-2">
					{#if user.avatar_url}
						<img src={user.avatar_url} alt="Avatar" class="w-8 h-8 rounded-full object-cover bg-white" />
					{:else}
						<div class="w-8 h-8 rounded-full bg-indigo-400 flex items-center justify-center font-bold">{user.username[0].toUpperCase()}</div>
					{/if}
					<span>{user.username}</span>
				</div>
				<button onclick={() => { logout(); goto('/login'); }} class="text-sm bg-indigo-700 hover:bg-indigo-800 px-3 py-1 rounded">Logout</button>
			</div>
		</nav>
	{/if}

	<div class="min-h-screen bg-slate-50">
		{@render children()}
	</div>
{/if}
