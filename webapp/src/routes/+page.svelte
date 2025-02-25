<script>
    import Interpretability from "./Interpretability.svelte";
</script>

<p class="mt-16 mx-auto text-center text-5xl max-w-3xl">Introducing: Content Bottleneck Generative Models</p>

<p class="text-left text-stone-600 mt-18 mx-auto font-extralight max-w-3xl">
The prevailing paradigm that most AI companies use is to train models as monoliths trained solely for narrow performance measures. 
However, this results in models that are difficult to work with, debug, and reliably explain. 
Even more alarming, current systems produce explanations and justifications that are completely unrelated to the actual processes the system used to arrive at its output.
</p>

<p class="text-left text-stone-600 mt-12 mx-auto font-extralight max-w-3xl">
<span class="font-semibold">At Guide Labs we believe you cannot reliably debug, align, and trust a model you don’t understand.</span> 
These critical properties cannot just be left unaddressed until after a model has been trained; they should guide the entire model development pipeline. 
Instead, we are rethinking the entire pipeline–model architecture, datasets, and training procedure—to engineer models that are interpretable, safe, trustworthy, and easier to debug and fix.
Toward this end, we have created <span class="font-semibold">Context Bottleneck Generative Models</span>.
</p>

<p class="text-left text-stone-600 mt-12 mx-auto font-extralight max-w-3xl">
Concept Bottleneck Generative Models have a built-in interpretable layer. This constraints the model to reliably explain its outputs in terms of human-understandable factors.
The Concept Bottleneck is model-agnostic, meaning it can be added into a wide variety of generative models without impacting generation quality.
Concept Bottleneck Generative Model allows users to:
</p>

<ul class="list-disc list-inside text-left text-stone-600 mt-6 mx-auto font-extralight max-w-3xl">
    <li><span class="font-semibold">Interpret</span>: Identify the important concepts that are responsible for the model's generated output</li>
    <li><span class="font-semibold">Steer</span>: Force the model's output to include specific human-understandable concepts.</li>
    <li><span class="font-semibold">Debug</span>: Distinguish wether the model has learned a pre-defined human-understsandable concept during training.</li>
</ul>

<p class="mt-12 mx-auto text-left text-5xl max-w-3xl">Interpretability</p>

<Interpretability/>

<p class="mt-12 mx-auto text-left text-5xl max-w-3xl">Steerability</p>

<p class="mt-12 mx-auto text-left text-5xl max-w-3xl">Debugging</p>