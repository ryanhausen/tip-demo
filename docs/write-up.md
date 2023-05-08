## Finding AI Authors

### Introduction

We would like to detect and define AI Authors. We define AI Authors as authors
who have written about AI in the past. We will detect these authors by framing
the problem as a graph problem.

### Method

We will consider a **seed** Graph of authors and papers that will be taken for
granted as being about AI. We will then use the seed graph to find other 
other AI authors. 

$$f(H, G, G^{1..N}) \mapsto \hat{y}$$

Where $f$ is the function that we are defiing, $H = <V^H, E^H>$ is the candidate
graph, $G = <V^G, E^G>$ is the seed graph, and $G^{1..N} = <V^{G^{1..N}},
E^{G^{1..N}}>$ are the possible peripheral graphs, $\hat{y} =
\mathbb{R}^{|V^H|}$ is the predicted label for author nodes in $H$.

An inital function $f$ will be defined as follows:

$$
f(H, G, G^{1..N}) \\
$$

