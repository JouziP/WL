# WL
Wang-Landau sampling method for calculation of Density Of States

Given an interacting network (example a network of friends on facebook) and the type of interactions 
(e.g. friends may both like or dislike a particular post) one may construct a cost funtion that
takes in a configuration (a series of likes and dislikes) of the network as input, and outputs a value 
(called energy of the network). This code provides the statistical distribution of energies for a given 
cost model. 

The Wang-Landau is an example of non-Markovian importance sampling methods: 

https://en.wikipedia.org/wiki/Wang_and_Landau_algorithm.

Fugao Wang and D. P. Landau Phys. Rev. Lett. 86, 2050 – Published 5 March 2001.


