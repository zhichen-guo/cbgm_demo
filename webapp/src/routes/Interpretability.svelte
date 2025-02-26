<script>
    import BarChart from "$lib/barchart/BarChart.svelte";
    import logo from "$lib/assets/guidelabs.png";
    import { onMount } from "svelte";

    let images = $state();
    let concept_probs = $state();

    onMount(() => {
        generate_images();
    })

    async function generate_images() {
        images = null;
        const response = await fetch(`${import.meta.env.VITE_API_URL}/interpret`, {
            method: 'GET'
        });
        if (!response.ok) {
            console.log("Error generating images!");
        }
        const blob = await response.json();
        images = blob.image;
        concept_probs = blob.data;
    }
</script>

<div class="relative mt-12 mx-auto font-extralight max-w-3xl h-130 bg-purple-50 rounded-xl">
    {#if images}
        <img class="w-full object-cover" src={`data:image/png;base64,${images}`}/>
        {#if concept_probs}
            {#key concept_probs}
                <div class="flex mx-10 gap-x-12 h-1/3">
                    <BarChart concept_probs={concept_probs[0]}/>
                    <BarChart concept_probs={concept_probs[1]}/>
                    <BarChart concept_probs={concept_probs[2]}/>
                </div>
            {/key}
        {/if}
    {:else}
        <div class="flex items-center justify-center h-full">
            <img src={logo} class="w-10 animate-spin"/>
        </div>
    {/if}
    <button onclick={generate_images} class="absolute bottom-6 right-8 bg-indigo-500 rounded-full px-4 py-3 text-white text-medium duration-400 hover:bg-indigo-600">Regenerate</button>
</div>