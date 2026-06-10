# WAIfinder

### Problem Statement
In the brief hours before an oncoming flood, quickly reaching a secure shelter is a critical component for survival.
While apps such as Google Maps can provide routes to a given end point, they lack crucial features required for reaching a shelter before an oncoming flood.
For example, Google Maps relies on community reports of road closures rather than predicting them in advance; while this suffices for day-to-day traffic issues,
by the time a road closure is reported it may already be too late.

Our project aims to solve this problem; we use a custom implementation of the A* algorithm that optimizes for both travel time and road closure risk.
More specifically, we predict road closure risks in advance, and use them to weight travel time, ensuring an optimal combination of both that can be fine-tuned to meet
the user's specific situation (for example, if the user has severe bleeding, a lower travel time is highly important).

### What is A*?
A* is a highly-efficient algorithm that determines the lowest weighted path from a start node and a graph node.
The road network is represented as a series of nodes (junctions and points of interest) with edges (roads, motorways, etc).
The weight is calculated through the formula $w_{eight} = \frac{travel time}{k - risk}$
