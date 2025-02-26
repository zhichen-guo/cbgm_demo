<script>
    import BarChart from "$lib/barchart/BarChart.svelte";
    import { onMount } from "svelte";

    let images = $state();
    let number = $state(0);
    let color = $state("red");

    onMount(() => {
        generate_images();
    })

    async function generate_images() {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/steer?number=${number}&color=${color}`, {
            method: 'GET'
        });
        if (!response.ok) {
            console.log("ERROR!");
        }
        const blob = await response.blob();
        images = URL.createObjectURL(blob);
        console.log(blob.blob);
    }
</script>

<div class="relative mt-12 mx-auto font-extralight max-w-3xl h-130 bg-purple-50 rounded-xl">
    <div class="grid grid-cols-3 gap-4 p-6">
        <div class="col-span-2">
            {#if images}
                <img class="w-full object-cover" src={images}/>
            {/if}
        </div>
        <div>
            <div class="mt-2">
                <label for="number">Number:</label>
                <select bind:value={number} class="mt-2 block p-2 bg-white w-full rounded-full border-1 border-slate-200">
                    {#each [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] as n}
                        <option value={n}>{n}</option>
                    {/each}
                </select>
            </div>
            <div class="mt-4">
                <label for="color">Color:</label>
                <select bind:value={color} class="mt-2 block p-2 bg-white w-full rounded-full border-1 border-slate-200">
                    {#each ["red", "green"] as c}
                        <option value={c}>{c}</option>
                    {/each}
                </select>
            </div>
        </div>
    </div>

    <button onclick={generate_images} class="absolute bottom-6 right-8 bg-indigo-500 rounded-full px-4 py-3 text-white text-medium duration-400 hover:bg-indigo-600">Regenerate</button>
</div>