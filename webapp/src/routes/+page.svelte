<script>
    import Interpretability from "./Interpretability.svelte";
    import Steerability from "./Steerability.svelte";
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
That’s why we are rethinking the entire AI development pipeline, from model design to training, to prioritize interpretability, safety, and trust. 
Toward this end, we have created <span class="font-semibold">Context Bottleneck Generative Models (CBGMs)</span>.
</p>

<p class="text-left text-stone-600 mt-12 mx-auto font-extralight max-w-3xl">
CBGMs include a built-in interpretable layer. This constraints the model to reliably explain its outputs in terms of human-understandable concepts.
The Concept Bottleneck is model-agnostic, meaning it can be built into a wide variety of generative models without sacrificing generation quality.
With CBGMs, you can:
</p>

<ul class="list-disc list-inside text-left text-stone-600 mt-6 mx-auto font-extralight max-w-3xl">
    <li><span class="font-semibold">Interpret</span>: Identify the important concepts responsible for the model's generated output</li>
    <li><span class="font-semibold">Steer</span>: Direct the model’s output by adjusting the concepts it uses.</li>
    <li><span class="font-semibold">Debug</span>: Check whether the model has correctly learned certain human-understandable concepts.</li>
</ul>

<p class="mt-12 mx-auto text-left text-5xl max-w-3xl">Interpretability</p>

<p class="text-left text-stone-600 mt-8 mx-auto font-extralight max-w-3xl">
Contemporary generative models are largely inscrutable and provide no way to identify the key concepts upon which they are reliant.
During training, CBGMs learn to associate the features in the training material to specific human-understandable concepts.
Then, when the model generates new outputs, it can tell you which concepts it used and with what level of confidence.
</p>

<p class="text-left text-stone-600 mt-12 mx-auto font-extralight max-w-3xl">
In this demo, we have trained a CBGM on the color-MNIST dataset - a collection of hand-written numbers in red and green.
We constrained the CBGM to learn the human-understandable concepts of numbers (0-9) and color (green and red).
We then use the model to generate new images and also show you the top 5 concept probabilities it for each image, giving you a clear sense of how it arrived at its result.
</p>

<Interpretability/>


<p class="mt-12 mx-auto text-left text-5xl max-w-3xl">Steerability</p>

<p class="text-left text-stone-600 mt-8 mx-auto font-extralight max-w-3xl">
CBGMs don’t just tell you which concepts they used - they also let you steer the generation process. 
By adjusting the concept probabilities, you can guide the model’s output to emphasize specific concepts, giving you control over what the model generates.
</p>

<p class="text-left text-stone-600 mt-12 mx-auto font-extralight max-w-3xl">
In this part of the demo, we’ll take the same model trained on the color-MNIST dataset. 
But this time, instead of showing you the concept probabilities for each image, we’ll directly set the probabilities ourselves. 
This allows us to steer the output toward specific concepts — watch how the images change as we adjust the input.
</p>

<Steerability/>


<p class="mt-12 mx-auto text-left text-5xl max-w-3xl">Debugging</p>

<p class="text-left text-stone-600 mt-8 mx-auto font-extralight max-w-3xl">
One of the hardest parts of working with traditional generative models is checking if the model has actually learned the right concepts during training. 
With CBGMs, you can track the model’s accuracy on each individual concept throughout the training process. 
After training, you can also assess the quality of the model by looking at the probability distribution of each concept in a random samples.
</p>


<p class="mt-12 mx-auto text-left text-5xl max-w-3xl">AI systems engineered for interpretability</p>

<p class="text-left text-stone-600 mt-8 mx-auto font-extralight max-w-3xl">
By building in an interpretable layer, CBGMs let you see exactly which concepts drive the model’s output. 
This gives you the power to interpret the model’s outputs, steer its behavior, and easily debug any issues - making AI more transparent, trustworthy, and controllable.
</p> 

<p class="text-left text-stone-600 mt-12 mx-auto font-extralight max-w-3xl"> 
At Guide Labs, we believe that transparency and trust should be at the core of every AI system. 
CBGMs represent a new era of AI development, where safety and explainability are prioritized from the start. 
Our mission is to create AI systems that you can trust because you understand how they work.
</p>


<p class="mt-12 mx-auto text-left text-5xl max-w-3xl">Sources</p>

<ol class="list-decimal list-inside text-left text-stone-600 mt-6 mb-10 mx-auto font-extralight max-w-3xl">
    <li><a href="https://www.guidelabs.ai/post/introducing-guide-labs-engineering-interpretable-and-auditable-ai-systems">Guide Labs Blog</a></li>
    <li><a href="https://openreview.net/forum?id=L9U5MJJleF">Concept Bottleneck Generative Models</a></li>
</ol>
