<script>
	import '../app.css';
	import guidelabs from '$lib/assets/guidelabs.png';
	let { children } = $props();
</script>

<div class="m-auto w-14/15 max-w-7xl">
	<nav class="my-6 h-14 rounded-full border-1 border-slate-200">
		<div class="flex items-center h-8 mt-3 ml-3 my-auto w-40">
			<img src={guidelabs} alt="Guide Labs Logo" class="h-full"/>
			<p class="ml-1">Guide Labs</p>
		</div>
	</nav>
	{@render children()}
</div>
