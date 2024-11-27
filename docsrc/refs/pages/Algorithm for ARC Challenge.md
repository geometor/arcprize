---
title: Algorithm for ARC Challenge
pageTitle: Algorithm for ARC Challenge - by Alexander Naumenko
created: 24.207.123109
tags: []
source: https://alexandernaumenko.substack.com/p/algorithm-for-arc-challenge
author: Alexander Naumenko
---

# Algorithm for ARC Challenge - by Alexander Naumenko
source: [](https://alexandernaumenko.substack.com/p/algorithm-for-arc-challenge)

> In his 2019 paper "On the Measure of Intelligence" (https://arxiv.org/abs/1911.01547), François Chollet, an AI researcher from Google, proposed Abstraction and Reasoning Corpus for Artificial General Intelligence (ARC-AGI) (https://github.com/fchollet/ARC-AGI


In his 2019 paper "On the Measure of Intelligence" ([https://arxiv.org/abs/1911.01547](https://arxiv.org/abs/1911.01547)), François Chollet, an AI researcher from Google, proposed Abstraction and Reasoning Corpus for Artificial General Intelligence (ARC-AGI) ([https://github.com/fchollet/ARC-AGI](https://github.com/fchollet/ARC-AGI)). You may consider it an IQ test for AI systems. The test was designed to resist memorization-based approaches as each task has only a few examples and includes a novel transformation to figure out.

In short, in each task, we are given a 2d array of maximum size 30x30 that may contain digits from 0 to 9. According to some transformation, the input array transforms into an output array with the same limitations, but the output array may be of different size and may contain different digits or in different positions. There are only a few examples provided for an AI system to figure out the transformation and based on those findings the system has to transform a provided test input array.

Sounds simple? It seems so if we take into account that humans easily solve more than 80% of tasks. But think again. The challenge is to program or train an AI system so that it can solve the challenge without any help from humans. So far, the best score on Kaggle is 41%, which is far from ideal.

The author of the challenge believes that the program that will break the 85% threshold will most likely demonstrate novel approaches and may contribute to the development of AGI. François Chollet proposes to use some form of program synthesis when a task transformation is broken down into primitive transformations, each one of which may be easily implemented. Then the system will only need to "somehow" determine the combination of basic transformations to apply in each task. Basically, we only need that "somehow". This is what we will discuss in this post.

### Objects and Actions vs Properties

My theory of intelligence, to reiterate once again, is based on the need to shift our focus from thinking in terms of objects and actions to thinking in terms of comparable properties. Let's consider what benefits it may provide based on the example of the ARC Challenge.

Consider the following two examples related to one task. To make it easier for humans, François Chollet considered the possibility of visualizing tasks. This is my version of visualizing them.

[

![](Algorithm%20for%20ARC%20Challenge/https%253A%252F%252Fsubstack-post-media.s3.amazonaws.com%252Fpublic%252Fimages%252F8e6af692-9a3d-4ed0-b722-f60745c5f2c3_1245x260.jpeg)

](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e6af692-9a3d-4ed0-b722-f60745c5f2c3_1245x260.jpeg)

In the raw form, the same is represented as the following arrays of digits:

\[\[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]

\[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\]\]

\[\[2 2 2 2 2\]

\[2 0 1 0 2\]

\[2 1 0 1 2\]

\[2 1 0 1 2\]

\[2 2 2 2 2\]\]

Many tasks use 0s as background and other digits to represent "objects" - groups of "pixels". Then the abovementioned transformations are "actions" applied to "objects". In this particular example, the transformation includes several primitive ones - movement, scaling, crop.

Let's express the same in terms of properties. "Objects" are different from the background. They are characterized by a bounding rectangle, coordinates, "color", scale factor, etc. How can we tell that "movement" was applied? Because the relative positions of two objects changed. What about scaling? Can we compare blue objects in input and output? No, but we can try to scale up its input version and then compare them. Or we can check the output object and confirm that it can be scaled down to the input one. What about crop? The crop transformation changes the array dimensions, which is observed here.

Transformations not only change properties. They have their own properties. For example, "movement" needs "direction" and "distance" along with an "object". Scale needs an object and a scale ratio. Crop needs a rectangular area to keep. In this example, there is always a yellow rectangular edge in input and output arrays. The other object of "whatever non-background color" moves to the center of the yellow rectangular area. That area also defines the scale ratio for that object as well as coordinates for the crop operation.

### Generalization

"Whatever non-background color" is the first example of generalization. Let me remind you how I define it - the process of specialization introduces defining differences of subclasses, the process of generalization "forgets" differences to return to the parent class level.

Another example of generalization from ARC Challenge is this task:

[

![](Algorithm%20for%20ARC%20Challenge/https%253A%252F%252Fsubstack-post-media.s3.amazonaws.com%252Fpublic%252Fimages%252F3aca55c1-87dd-407c-9fab-7c726c99de61_611x553.jpeg)

](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3aca55c1-87dd-407c-9fab-7c726c99de61_611x553.jpeg)

We clearly see that objects colored yellow are not all the same pixel-wise but they have "defining features", that the other objects don't have.

Generalization applies to transformations as well. Movement may be for a fixed distance or for a distance defined by some object, in the same direction or in the one dependent on some factor, but if we observe a change in position (relative or absolute) we may suspect that movement was involved.

### Objects and properties

Consider another example:

[

![](Algorithm%20for%20ARC%20Challenge/https%253A%252F%252Fsubstack-post-media.s3.amazonaws.com%252Fpublic%252Fimages%252F91fd4da0-8922-40e4-b443-77331c1e1d75_604x258.jpeg)

](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91fd4da0-8922-40e4-b443-77331c1e1d75_604x258.jpeg)

Obviously, we may say that the color of vertexes in the output depends on the convexity/concavity of each vertex. But how can we define it? In fact this definition is interesting in that it hints at what information about each "object" we may need to collect.

Can we define it via the orientation of adjacent edges? No. Via the number of neighbor pixels outside and inside? Closer, but do not forget objects in corners. But most importantly, you need to keep track of pixels inside and outside. Probably, it is enough to remember "inside" pixels only. Then blue vertexes are those with only 1 inside neighbor, while yellow vertexes have at least 3.

"Object" is not only a set of pixels, it is also edges and vertexes, inside pixels and outside neighbors, quarters, symmetry, non-background colors statistics, "holes", and much more.

### Hypotheses

In the first picture above, from the second example, we may decide that the scale factor is 3, a fixed value. But I propose to always consider options - fixed value and dependent value, in this case. Given these two options, we check them against all other examples and "fixed value" does not survive the test. Had we only that option to consider we would not be able to determine the right one.

The same is true for transformations. When we observe smaller dimensions of output arrays, we may suspect crop. But what about downscaling? There are also other transformations that lead to the same result. Can we differentiate crop from downscaling based on smaller dimensions only? No. But smaller dimensions filter out other transformations. To differentiate further we need additional properties. For example, scale ratios of objects. Crop does not affect them compared to downscaling.

Some objects mirrored are not different from those rotated by 180 degrees. Both are good as our initial options. Consider other examples to finalize the proper one.

Forming hypotheses is an important step. Intelligence is about selecting fitting options from available ones. The selection process narrows down the set quickly. Do not be afraid of adding more options initially, be afraid of missing something.

### Conditionals

Many tasks use what we can call conditionals or mapping. Given one shape color the other object in one color, given the other shape color that object differently. We can track the variability of options and mapped values in some kind of data structure (map, dictionary - depends on your programming language) but we need to have representations of colors, shapes, and other properties fitting for the use in those data structures.

One type of task involves coloring neighbor cells. Diagonal neighbors are colored in one color, horizontal and vertical neighbors are colored in another color. "Diagonal" is a generalization for four different corners. Coloring may be defined differently for each of them. It's another suggestion for what kind of details we may need to keep track of if we want to solve the ARC Challenge.

### Algorithm

The algorithm to solve the ARC Challenge in my opinion does not require deep learning or any other statistical methods. It is a good old programming with if statements and sets and dictionaries.

1 Step. Analyze inputs/outputs in one example. Collect as much information about objects as possible.

2\. Based on that information find differences imposed on the input array and its objects. Use those differences to filter out transformations that are not involved. At this stage, many hypotheses are OK. Also, form hypotheses about the source of parameters of each transformation.

3\. Go through the other examples and finalize proper hypotheses. ARC Challenge allows the submission of two options, so do not be confused by ambiguity.

4\. Figure out the sequence of basic transformation. Prepare the grand transformation.

5\. Set up an Expecto class about what objects to expect in a test input and what properties of those objects to pay attention to.

6\. Apply the grand transformation and Expecto class to a test input.

### The List of Basic Transformations

The list below is my view on the basic transformations used in the ARC Challenge. Surely, I tried to populate it with items that are different, rely on different properties, and affect different properties. Feel free to add other items you may find fitting.

1\. Overlapping is about z-coordinate.

2\. Decomposition is about moving lines (or even pixels) of the object.

3\. Move is about changing position.

4\. Coloring is about changing color (digit).

5\. Mirroring is about symmetry.

6\. Rotating is about angles.

7\. Scaling is about scaling an object or the whole input.

8\. Inversion is about two colors substituting each other.

9\. Removal is about blending an object into the background.

10\. Replicating is about creating copies.

11\. Pattern continuation is about figuring out and continuing some sequence.

12\. Pattern restoration is about finding a missing piece in some pattern.

13\. Replacing is about replacing one thing with a different one (color for color or shape for symmetry axis - it can be anything).

14\. Crop is about removing space.

15\. Adding dimensions is about adding space.

16\. Logical operations are about pixel-wise logical operations.

17\. Stacking is about z-coordinate.

18\. Minmodel is about extreme generalization.

Each of those transformations affects some properties. Observing respective changes from inputs to outputs hints at the possible use of that primitive.

Combining several of them along with the variability of shapes and colors and options for sources of parameters explains well why the ARC Challenge poses such a problem for current AI systems.

### Wish Me Luck or Better - Help!

I am working on implementing the above ideas but the process is slow. If anyone is interested in helping me with Python and cracking the ARC Challenge, I will be more than happy. It’s time to show the potential of this theory and to start developing a new AI paradigm!

### Subscribe to I Solve Intelligence - it's Symbolic

In this post, we start unraveling the mystery of intelligence by proposing its "atoms".
