# Guide Labs CBGM Demo

This is a demo to showcase the capabilities of Guide Lab's [Concept Bottleneck Generative Model](https://openreview.net/forum?id=L9U5MJJleF).

## Installation
1. Clone repo `git clone git@github.com:zhichen-guo/cbgm_demo.git`
2. `cd cbgm_demo`
3. Make sure Docker Dashboard is running
4. Build containers `docker compose build`
5. Start containers `docker compose up`
6. View the website in your browser at `localhost:5173`

## Future Work
* Creating a better demo for the "Debugging" section
* Make the defaults for the "Steerability" section random instead of "0" and "Red"
* Train CelebA and use that instead of Color-MNIST