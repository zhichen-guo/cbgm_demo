<script>
	import '../app.css';
	import guidelabs from '$lib/assets/guidelabs.png';
	let { children } = $props();
</script>

<div class="m-auto w-14/15 max-w-7xl h-20">
	<nav class="sticky top-0 my-6 h-14 rounded-full border-1 border-slate-200">
		<a href="https://www.guidelabs.ai/" class="flex items-center h-8 mt-3 ml-3 my-auto w-40">
			<img src={guidelabs} alt="Guide Labs Logo" class="h-full"/>
			<p class="ml-1">Guide Labs</p>
		</a>
	</nav>
	{@render children()}
</div>
