<script>
    import { LayerCake, Svg } from 'layercake';
    import { scaleBand } from 'd3-scale';

    import Column from './Column.svelte';
    import AxisX from './AxisX.svelte';
    import AxisY from './AxisY.svelte'; 

    let { concept_probs } = $props();

    const concepts = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "red", "not red", "green", "not green"];
    var concept_prob_pairs = [];

    for (let i = 0; i < concepts.length; i++) {
        concept_prob_pairs.push({ 
            label: concepts[i],
            prob: concept_probs[i].toPrecision(3)
        })
    }

    concept_prob_pairs.sort(function(a, b) {
        return b.prob - a.prob;
    })

    const data = concept_prob_pairs.slice(0, 5);
    
    const xKey = 'prob';
    const yKey = 'label';
</script>

<div class="chart-container">
    <LayerCake
        padding={{ top: 0, right: 0, bottom: 20, left: 20 }}
        x={"label"}
        y={"prob"}
        xScale={scaleBand().paddingInner(0.3).round(true)}
        xDomain={data.map((c) => {return c.label})}
        yDomain={[0, 1]}
        {data}
    >
        <Svg>
            <AxisX gridlines={false} />
    
            <AxisY snapBaselineLabel />
            <Column />
        </Svg>
    </LayerCake>
</div>
    

<style>
    /*
      The wrapper div needs to have an explicit width and height in CSS.
      It can also be a flexbox child or CSS grid element.
      The point being it needs dimensions since the <LayerCake> element will
      expand to fill it.
    */
    .chart-container {
      width: 100%;
      height: 100%;
    }
</style>