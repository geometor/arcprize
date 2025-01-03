Nov 24, 2024

Professor Swarat Chaudhuri from the University of Texas at Austin and visiting researcher at Google DeepMind discusses breakthroughs in AI reasoning, theorem proving, and mathematical discovery. Chaudhuri explains his groundbreaking work on COPRA (a GPT-based prover agent), shares insights on neurosymbolic approaches to AI.

Professor Swarat Chaudhuri:
https://www.cs.utexas.edu/~swarat/


Tufa AI Labs is a brand new research lab in Zurich started by Benjamin Crouzier focussed on ARC and AGI, they just acquired MindsAI - the current winners of the ARC challenge. Are you interested in working on ARC, or getting involved in their events? Goto https://tufalabs.ai/

TOC:
[00:00:00] 0. Introduction / CentML ad, Tufa ad

1. AI Reasoning: From Language Models to Neurosymbolic Approaches
[00:02:27] 1.1 Defining Reasoning in AI
[00:09:51] 1.2 Limitations of Current Language Models
[00:17:22] 1.3 Neuro-symbolic Approaches and Program Synthesis
[00:24:59] 1.4 COPRA and In-Context Learning for Theorem Proving
[00:34:39] 1.5 Symbolic Regression and LLM-Guided Abstraction

2. AI in Mathematics: Theorem Proving and Concept Discovery
[00:43:37] 2.1 AI-Assisted Theorem Proving and Proof Verification
[01:01:37] 2.2 Symbolic Regression and Concept Discovery in Mathematics
[01:11:57] 2.3 Scaling and Modularizing Mathematical Proofs
[01:21:53] 2.4 COPRA: In-Context Learning for Formal Theorem-Proving
[01:28:22] 2.5 AI-driven theorem proving and mathematical discovery

3. Formal Methods and Challenges in AI Mathematics
[01:30:42] 3.1 Formal proofs, empirical predicates, and uncertainty in AI mathematics
[01:34:01] 3.2 Characteristics of good theoretical computer science research
[01:39:16] 3.3 LLMs in theorem generation and proving
[01:42:21] 3.4 Addressing contamination and concept learning in AI systems

REFS:
00:04:58 The Chinese Room Argument, https://plato.stanford.edu/entries/ch...
00:11:42 Software 2.0,   / software-2-0
00:11:57 Solving Olympiad Geometry Without Human Demonstrations, https://www.nature.com/articles/s4158...
00:13:26 Lean, https://lean-lang.org/
00:15:43 A General Reinforcement Learning Algorithm That Masters Chess, Shogi, and Go Through Self-Play, https://www.science.org/doi/10.1126/s...
00:19:24 DreamCoder: Bootstrapping Inductive Program Synthesis with Wake-Sleep Library Learning (Ellis et al., PLDI 2021), https://arxiv.org/abs/2006.08381
00:24:37 The Lambda Calculus, https://plato.stanford.edu/entries/la...
00:26:43 Neural Sketch Learning for Conditional Program Generation, https://arxiv.org/pdf/1703.05698
00:28:08 Learning Differentiable Programs With Admissible Neural Heuristics, https://arxiv.org/abs/2007.12101
00:31:03 Symbolic Regression With a Learned Concept Library (Grayeli et al., NeurIPS 2024), https://arxiv.org/abs/2409.09359
00:41:21 Turing Machines, https://plato.stanford.edu/entries/tu...
00:41:30 Formal Verification of Parallel Programs, https://dl.acm.org/doi/10.1145/360248...
01:00:08 The Feynman Lectures, https://www.feynmanlectures.caltech.edu/
01:00:37 Training Compute-Optimal Large Language Models, https://arxiv.org/abs/2203.15556
01:12:26 Fermat's Last Theorem, https://en.wikipedia.org/wiki/Fermat%...
01:18:19 Chain-of-Thought Prompting Elicits Reasoning in Large Language Models, https://arxiv.org/abs/2201.11903
01:18:42 Draft, Sketch, and Prove: Guiding Formal Theorem Provers With Informal Proofs, https://arxiv.org/abs/2210.12283
01:19:49 Learning Formal Mathematics From Intrinsic Motivation, https://arxiv.org/pdf/2407.00695
01:20:19 An In-Context Learning Agent for Formal Theorem-Proving (Thakur et al., CoLM 2024), https://arxiv.org/pdf/2310.04353
01:23:58 Learning to Prove Theorems via Interacting With Proof Assistants, https://arxiv.org/abs/1905.09381
01:35:50 Algorithmic Game Theory, https://www.amazon.ca/Algorithmic-Gam...
01:39:58 An In-Context Learning Agent for Formal Theorem-Proving (Thakur et al., CoLM 2024), https://arxiv.org/pdf/2310.04353
01:42:24 Programmatically Interpretable Reinforcement Learning (Verma et al.,
ICML 2018), https://arxiv.org/abs/1804.02477 


Transcript:

neuros symbolic programming is this
approach to artificial intelligence where you are representing models using a
mix of neural networks and classical symbolic code you mentioned Alpha proof
that's a great example but I would say that even these agents that are
generating some code using language model and then executing the code and then
getting feedback and then using that to make further decisions they are really
doing something new symbolic as well right because you are actually using a
python interpreter which is a symbolic tool now there is a universe where you
have again an extremely low-level language a sort of Assembly Language and then
you just let the machine figure out over time what kinds of obstructions are
useful and to me that could have a lot of value because you could discover
Things That No human would ever imagine and that would enable you potentially to
do new kinds of math new kinds of physics new kind of biology and you are going
to you know discover these higher level building blocks yes you know no human
has figured that out yet but this AI has but then you're using this building
block to build parsimonious programs models that can do amazing things and then
you're just bootstrapping and you're building up this entirely new universe of
mathematics and computation I can imagine such a world mlst is sponsored by
sense ml which is the model serving platform for machine learning workloads now
you log into their platform the first thing you see is the SAS option so this is
the really simple option just like on open AI you can send requests up you stick
your access token in there and you can access all of the latest open source
models and it's faster and it's cheaper by the way when you sign up you get 10
free credits which means you can do some experimentation without spending a
penny also watch the interview I did with Gennady their CEO the other day enjoy
mlst is sponsored by tuur AI labs this is a research lab started by Benjamin
crua over in Zurich they have just acquired min's AI the winners of the arc
challenge their sole purpose is trying to figure out AGI as quickly as possible
and they're looking at the arc challenge in particular um if you're in Zurich
and you want to join their monthly meetups if you're interested in working for
Ben as an ml researcher reach out to him go to tabs. welcome to mlst thank you
very much thanks for having me it's so nice to have you here can you um tell us
about your background I'm a professor of computer science at uh the University
of Texas at Austin and um this year I'm also a visiting researcher at uh Google
Deep Mind in London my original research background is in symbolic methods for
reasoning and programming languages but uh over the last 10 years I've also
gotten very involved in machine learning and these days I'd say that I have a
you know foot in on both sides uh both symbolic methods and and machine learning
wonderful now um we had a very interesting conversation in the car on the way
over about reasoning that's right what is reasoning well to me reasoning is to
some extent in the eyes of the beholder you know it's one of those things that
you know it when you see it um but I think that for the from the point of view
of um defining that in the AI context it makes sense to have some criteria in
mind um so what constitutes reasoning so um one of these is uh in my mind doing
well at um mathematical or programming or planning these kinds of tasks uh right
that uh historically people have associated with um with deeper thinking and and
and reasoning so I would say that if a system is uh performing better at those
tasks compared to existing methods then that's I would say that that it's doing
you know it's it's showing Improvement on reasoning so I hesitate to say that a
model either does or does not do reasoning because to me it's not a Boolean it's
really a quantitative measure and uh you can see you know progress on this
measure uh over time um now this is more about the the what of it you know what
does the model do in order to be uh in order for it to be doing reasoning
there's also the question of how and I think that it's really useful to separate
the how consideration from this because I think that there are many many
different methods uh for doing reasoning we have seen some of them um in in the
recent past gain prominence but there are other kinds of methods as well yeah
this is this is it though do you think that it's you you know like some people
are human chauvinists and they say that it's not really reasoning the way we
reason is is better John so is a famous example of this you know he he argued
that there was some complicated physical causation that can't easily be
replicated in in in in a machine but we can agree that you know certainly in
simulation there's a a myriad of different ways we can make something behave as
if it's it's reasoning what's the difference right so I think then again it's
one of those things that we have to decide on our criteria so if you have a
system that takes a very large amount of compute in order to solve a very
difficult mathematical problem is that reasoning right so by your definition I
think that uh that probably wouldn't count uh but um I think that you know one
could argue that uh it's the end that matters that if you're able to solve this
hard math problem then you are doing reasoning well yeah I mean that there's
also the the robustness aspect of it because um for example you could simulate
something that happened in the physical world and you could reproduce the trace
and you could say well it's the same thing so why is it not reasoning but but
the real phenomenon would be able to reason in many many different situations
and certainly with language models when they are trained on specific types of
reasoning then of course they can generalize in in that setting but there are
these holes in in the Swiss cheese all over the place so there's always this
problem with test set contamination isn't there right yeah so I think that then
you know you have just named one additional Criterion uh for a model to be doing
reasoning which is that you need to have this form of robustness I would add to
it going back to the previous Point uh maybe computational budget is also a
consideration if it takes you you know 5,000 hours of compute on a massive
cluster in order to solve a math problem maybe it's not exactly doing reasoning
either right but to me again you have to decide what your definitions are right
what your criteria are and then you can talk about whether or not a system is
making progress on those measures talking about a model is doing reasoning based
on you know humanlike Behavior to me that's sort of a it's a bit too ambiguous
for my taste I would say yeah there there's this challenge with
anthropomorphization that the existence proof we have of course are humans doing
it but um it wouldn't be particularly good from an AI point of view if we have
to create a simulacrum of of of a human I I do believe though that there's some
kind of spectrum of strength of of reasoning and it feels to me that language
models create these very blown up circuits and it's not reusing the same
circuits in different situations and we seem to have this incredible ability to
um reflect these very parsimonious abstract motifs and and some cognitive
psychologists argue that there's something fundamental about these motifs maybe
it's the way the universe works or certainly it's the way our cognition works
and that doesn't seem to be the way that language models work I completely agree
we have been arguing for um these sorts of more modular compositional models uh
for a long time and I think that obstruction is an essential capability of
humans that modern language models lack but I would say that that's again going
into the the how of things you know there are a certain set of goal posts that I
want to be able to achieve certain tasks right to me it's useful to separate
that definition of what we are trying to do from how we are achieving it right
using modular models in which there are explicit abstraction mechanisms and we
are going to talk about examples of that uh from my work in and in other folks
work I'm sure in the going forward but I think that uh it's it's possible uh
that uh you know there may be some class of language models that comes up you
know maybe with a different training objective but that even though it's not
explicitly uh dealing in uh dealing with modularity it's able to nevertheless
achieve robustness right I I don't know that such a possibility is just uh not
there however I would say that given all we have seen from recent uh language
models there seems to be something fundamentally challenging in terms of
robustness and to me you know mechanisms for abstraction and modularity would be
a a good bet uh to have uh uh to achieve those goals mhm 01 from open AI is is
it reasoning uh to me it's uh it's a milestone in reasoning there's a big
Headroom ahead of it but uh it definitely by measures uh that we just discussed
uh you know performance in in programming tasks and solving math problems it
seems to be substantially better than prior models so to me it's a step towards
models that can reason in interesting um are there any situations where I mean
maybe we should first say in situations where it is doing reasoning which means
it's it's fitting your criteria I I think it's fair to say that yes yes it's
it's reasoning and then there's the space of situations where perhaps it it it
doesn't reason for many reasons possibly because of computational reasons it
might be trying to solve an NP hard problem and it just simply runs out of
context um or it might be trying to um do reasoning in a domain where it hasn't
been you know trained on um um for example so that there are limitations but you
think in principle those limitations could be overcome I think that uh oan
augmented with a lot of other things could make substantial steps towards
overcoming those limitations okay now there are a few things here that I have
left ambiguous and to me that's where the real questions are that what are those
extra uh pieces that need to be added to something like o1 in order to achieve
again I wouldn't say does reasoning you know better performance at reasoning
tasks right and to me there are um clear candidates like for example having more
grounding mechanisms uh using more powerful symbolic tools but uh this is specul
and and over the next few years I think we're going to see if those methods
actually work it's interesting to to see the shift towards neuros symbolic so um
a lot of folks in the um kind of connectionism space and Andre Kathy for example
spoke about software 2.0 there's this idea and Hinton as well there's this idea
that language models can do everything that that they can do this emergent
symbolic um reasoning and and we can train them end to end and what we're
starting to see now are things like Alpha geometry and Alpha proof and so so on
are these hybrid systems that that kind of and and gen generally as well I I
think that the way to robustness is building specific architectures to do
specific things well I think having these completely General Blank Slate things
doesn't work very very robustly but are you are you seeing that Trend as well
yes absolutely um many of us have been arguing for neuros symbolic methods for a
while now but uh increasingly I feel that this term is is is uh unnecessary
because it seems to me that um neuros symbolic methods are really increasingly
everywhere uh you mentioned Alpha proof that's a great example but I would say
that even these agents that are generating some code using language model and uh
then executing the code and then getting feedback and then using that to make
further decisions they are really doing something neuros symbolic as well right
because you are actually using a python interpreter which is a which is a
symbolic tool now that said to me the more interesting question is again not the
word itself but the precise form that these kinds of combinations are going to
take and we have seen some examples of this uh so for example in Alpha proof we
have a machine learning model a neural model that is getting feedback from a a
lean interpreter uh or lover right and and that's providing it a very solid form
of grounding um so I think that we are going to see this trend in other forms as
well in broader settings I don't know that it has to be extremely domain
specific there is a world where you can imagine you know code execution and
formal proofs basically informing all sorts of decision-making in the world with
uh purely neural models serving as the as the layer that goes between human
language and sort of messy signals uh to this kind of reasoning mechanisms can
reasoning exist without axioms that's a great question um I think that again it
depends on what we mean by reasoning uh when we are talking about mathematical
reasoning the entire objective is that you're going from certain axioms to
certain kinds of conclusions so so mathematical reasoning as we understand it
doesn't really make sense uh without axioms what about something like uh
physical reasoning so there everything that we consider to be physical reasoning
it depends on us being in a certain place uh with certain laws of physics so to
me um you know the you can imagine reasoning happening in a world where those
laws are different but even then you have axm it's just that you have different
axioms can we combine together reasoning systems absolutely we in fact do it all
the time we combine mathematical reasoning systems with um for example you know
experimental empirical reasoning methods that people use in the natural uh
Sciences all the times when we're doing any kind of scientific discovery right
and I can imagine that in the future we could have many different reasoning
systems uh with different kinds of capabilities and they all come together in in
um something that's uh bigger than the sum of its parts Alpha zero uh do you
think that's reasoning and and why I think again it is it is definitely a
powerful system that makes highly non-trivial progress on a task that's
traditionally cons considered to be reasoning MH so to me you know it's it's
sort of a behaviorist definition right if it looks like a like a a reasoning
system it does well on a reasoning task then it's doing some kind of reasoning
okay if if it looks like a duck quacks like a duck looks like a duck what is
neuros symbolic programming neuros symbolic programming is this approach to
artificial intelligence where you are representing models uh using a mix of
neural networks and classic iCal symbolic code uh so you could imagine for
example you know a program in which you have some neural modules that are making
decisions about uh perception let's say uh whether or not you know a certain
kind of object appears in a scene and then you have some some vectors coming out
of that and then you have some symbolic methods that are processing those
vectors um a lot of the times this makes sense if you have knowledge about uh
what a model should look like uh so then you can you know imagine using the
symbolic code to basically encode some of those priors you could also Imagine uh
neuros symbolic models being used when interpretability is a concern so for
example you're trying to understand a certain biological process now you may get
this perfect blackbox neural predictor except the scientist cannot really make
sense of it and use it to guide experiments but if you have a more mechanistic
model that is uh coded up in the form of um in the sort of notation that
scientists traditionally use and to me all of those are just you know programs
physics equations and and you know definitions of dynamical systems and so on
these are all just programs of various sorts so if you have a model that is you
know represented mechanistically like that as a as a sort of program but maybe
with certain neural pieces for parts that just cannot be easily symbolically
represented so that would be another uh potential application of this yeah there
seems to be I guess it's quite an ambiguous term but for example fris Chet talks
about discrete program search using a neuron Network to guide the generation of
programs um in in your work for example you could use it to um represent
functions or even some kind of post hoc validation type process you know to
ensure things are in guard rils um and there are many many more kind of
instantiations so so I guess it's quite an ambiguous thing uh it is so when we
defined the term neuros symbolic programming we want it to be very precise yeah
but um the word neuros symbolic is again as we discussed earlier it's being used
in lots of different forms uh to the extent that I would say it has also kind of
lost all meaning yes but when we talk about neuros symbolic programming we mean
a very specific thing which is that I have a I have a programming language in
which I can represent these Hybrid models I have combinations of of symbolic
code and neural networks and then we have some body of methods that are being
used to discover those programs and these methods may be partly neural partly
symbolic uh typically they are they are a mix of the two so um many fans of the
show would be familiar with the dream code paper by Kevin Ellison and and tanon
B Etc would as I as I recall correctly there was a domain specific language and
they had a you know like a waking phase and they had this neurog guided search
and they had an abstraction sleep and so on um so it's related to that idea
absolutely yeah so um I would say that there are a few categories of methods uh
that have come out in the last few years in this space and one big challenge is
Library learning Where You Are not just working with a fixed programming
language and trying to find programs in that language but you are actually doing
explicit abstraction and you're trying to discover New Primitives uh that are
then added to the programming language and dreamcoder falls in this category in
dreamcoder you are starting with an extremely low-level language the Lambda
calculus and then progressively you are discovering bigger and bigger um modules
which are uh abstractions really you're seeing patterns in these really
low-level programs and then you're abstracting them into these modules and then
you're reusing them right now um the programming language that they had over
there is purely symbolic but one can easily generalize it and there's in fact
some work that's happened more recently where uh that's been done um so you
could imagine then these uh programs that are mixtures of um neural networks and
these sorts of Lambda calculus terms right and then the method that they used
for discovering these Library functions and also uh just you know uh do program
synthesis search for programs those were all neural over there one could imagine
you know modernizing them uh it's recent enough but you know few years back uh
you could imagine bringing them to uh sort of 2024 adapting them to 2024 deep
learning by using large language models to do the of her programs and and the
obstruction interesting so um so dreamcoder was not using language models and it
had a hardcoded DSL and one thing that interests me is what The Primitives are
so for example we we could search the space of Turing machines we could use
Lambda calculus we I think um Josh tanber is a big fan of cognitive psychology
which is that we have these native fundamental priors of of cognition therefore
we should search those priors and presumably it was trained uh to do a
particular task you could train it to do the arc challenge for for you know so
then what it's kind of doing is it's saying well what composition of these
seeded prize in my DSL um produce skill programs that you know would work for
this particular thing so so like there's the question of where where do you
start and to what extent is the task you're training it on kind of does that
derange or influence the the library that you learn right so to me uh the prior
question is open I think that humans May well have uh a set of cognitive priors
but we don't necessarily know what they are what is however true is that the
presence of priors makes your ability to solve the program synthesis problem or
the learning library learning problem uh a lot better um and uh by that I mean
that if you have already a reasonable set of Primitives that are there in your
programming language you won't have to discover everything from scratch that
said I can imagine a world where you're starting with an extremely low-level
language without any sort of um priors and you are you just have these basic
operations like composition and uh then you are just discovering the entire
universe of programming of mathematics of physics uh what have you does it
matter if we can't understand the programs that that are generated this will be
a theme in this in this discussion because of course you're working theorem
proving as well is talking about how um essentially mathematicians don't do the
stuff themselves anymore we're we're leaning on computers to to you know search
this huge space but but just with this discret program search thing um we might
be creating programs that are still you know lots of abstractions and lots of
interesting efficiencies in there but but they seem quite inscrutable that's
right so I think that we should distinguish between the interpretability
question and the capability question to me there is potential value in
interpretability definitely in certain application domains like scientific
discovery we really care about interpretability uh there's also a potential
Safety and Security kind of angle and and we're going to discuss that later but
I think that it's useful to separate that concern from the concern of just uh
what would it take to build models that are really robust and and capable and so
I think that there is a universe where you have again an extremely low-level
language a sort of Assembly Language uh and I consider the Lambda calculus to be
something like that and then you just let the machine figure out over time what
kinds of obstructions are useful and to me that could have a lot of value
because you could discover Things That No human would ever imagine right and
that would enable you potentially to do new kinds of math new kinds of physics
new kinds of biology and so I don't rule out that possibility uh at all uh I
think this idea of obstruction would be valuable even in that regime because
what that will mean is that you are going to you know discover these higher
level building blocks yes you know no human has figured that out yet but but
this AI has but then you're using this building block to build parsimonious
programs models uh that can do amazing things and then you were just
bootstrapping and you're building up this you know entirely new universe of of
mathematics and and computation right um I can imagine such a world so can you
tell us about your work in this area so so so you you've created this
architecture that that uses llms and does uh type directed search and learning
to search and so on can can you tell us about that right so I have a series of
efforts in this space um I back in the day did a lot of work on just symbolic
methods for program synthesis and the setup there is that you have a programming
language you have a programming task that is defined either by at that time it
was either logical constraints or a set of examples and then you were defining a
search problem find me a program that fits the the task specification and so
those symbolic methods had some scalability challenges and then when deep
learning came about you know we all moved uh in that direction and this sort of
neurally guided program search this became became a a a very powerful approach
uh now uh some of the methods there they combined uh these older symbolic ideas
with the Deep learning ideas so for example we had these results on uh typ
directed neural program synthesis where you have a you are generating programs
in a strongly typed language and the type system of the language serves as a
pruning mechanism as well as a guidance mechanism so it rules Out programs that
are obviously not going to be reasonable and uh also helps us focus on certain
kinds of sub goals now if you think of what's going on in the world of theorem
proving uh it's actually very closely related uh so lean is really a functional
programming language with a really powerful type system and um so when you are
for example using feedback from the theorem prover to rule out certain kinds of
steps in your in your math proof search um you were really using a version of
this idea right uh but we had been thinking about that for for a while and the
broader program synthesis community that came out of the programming languages
World they were thinking about this problem okay so um then um this is still in
the context of you have a fixed programming language and you're looking for
programs in that language mhm now uh there are uh other approaches that that uh
are relevant here so we had for example uh these results on using neural
relaxation so there is this paper we have uh led by Amish sha and uh with isong
Yu uh who's my long-term collaborator and and Jennifer Son um and my former
student D Verma uh so this was on using neural relaxations of of of programs uh
as heuristics for doing a search over programs so the idea is this suppose you
are doing a search over programs and you are progressively filling up these uh
incomplete programs so you start with nothing just an just a code with a big
piece of uh a big hole in it and then you're progressively adding more and more
code so one challenge here was that because you're always working with these
incomplete programs how do you know whether or not a certain uh decision is
valuable right as in you know should I keep a certain incomplete program in the
in the pool or should I throw it out and the idea then was that you know in that
hole you're going to uh so there is a space of possible ways to to complete that
program so there are a lot of symbolic discrete terms that you can you can plug
into that that hole but instead of that what you do is that you stick a neural
network in there and there is this kind of a subset relationship so there is a
so because these neural networks are more expressive than any symbolic program
in your programming language uh you are going to have the property that um the
if you train the neural net well enough you are going to get a loss that is
better than whatever you would get with any sort of symbolic program and this
leads to a an argument that you can basically use the the the the loss that you
get after you have plugged in this neural network into that hole uh you can use
that as a lower bound on the cost to go that is the the uh best possible thing
you can do from that point on using a symbolic program and this can in turn be
used to guide uh heuristic search you know these sort of classic search
algorithms like AAR and um and Branch Unbound plus you know iterative depending
search and and so on so there are the this this whole slew of algorithms uh from
GOI back in the day right and now you're imagining accelerating these sorts of
algorithms with these neural relaxations y um so this sort of idea has been
there so in general we have looked a lot at this uh question of you know can I
use a neural network as a relaxation a sort of continuous approximation of a
discrete program and to what use can we put such a relaxation and we have looked
at a few versions of this other uh more recent efforts so we have this uh recent
paper on um Library learning in the context of symbolic regression with with
llms and here we are doing a lot of these same sorts of things uh you know
searching for programs uh doing obstruction but this time using llms and um in
particular an llm can be a really good way of um guiding even if you're doing
this sort of traditional search over programs for example using a genetic
algorithm or using you know some sort of type directed enumeration you can still
imagine you know an llm serving as the neural network that guides such a search
but on top of that you could also Imagine using an llm as a tool for abstraction
of the sort that we were talking about a little while ago so for example you
know in dreamcoder the way abstraction would happen is that you uh you know look
at a set of programs that did well and then you find syntactic substructures
that show up in those programs again and again right and then you would say that
okay this is a module that I can potentially reuse and that then becomes part of
my library the issue is that this is this process can be difficult because
identifying these sorts of common substructures in a large pool of programs can
be very challenging and there were these symbolic methods that were used for
this purpose but you could imagine not doing that and instead just using an llm
what could that look like well you should read this paper which is led by Arya
gy and aurel um and it's with Miles CRI cranmer and Omar ceras uh appearing at
new rips this year but the basic idea is that you are going to use an llm as the
ab structor so you're going to ask an llm what are some of the common patterns
that are showing up in these programs and you're going to use its natural
language you know reasoning I understand it's a loaded term but its ability to
at least uh you know find patterns in syntaxes in the syntax of programs uh
you're going and and explain that in natural language you're going to use that
capability to do the obstruction right and that's how you're going to learn a
concept I'm a big fan of Miles crr he wrote a a landmark paper on symbolic
regression that's right a few years ago and I I guess that is that another form
of neuros symbolic programming that and and also I've heard people talk about
doing symbolic decomposition of language models so this idea that you know you
you you start with this kind of block of clay you do stochastic gradient descent
and then we we tease out some kind of symbolic structure from it it's a
fascinating idea absolutely so uh going to your first question first uh symbolic
regression I see it as a form of program synthesis yeah really what you're
trying to do there is that you're given a data set you're trying to find a a an
expression right that that uh fits that data set well but an expression is just
a special kind of programs so some of the methods that we have talked about for
example this um this neural admissible hakes that was done in the symbolic
regression setting that you're trying to find a program that fits a data set
well right but now one can imagine you know going Beyond the sort of genetic
programming approaches or these approaches of distillation where you first train
a neural network and then distill it into a a symbolic program uh you can go
beyond these kinds of strategies and you can use an llm uh really heavily in
order to do that to solve that symbolic regression problem right and and so what
are the ways in which that can be used one angle is that you could use an llm to
basically do the search of her programs or guide the search of her programs or
expressions in particular these let's say that we are talking about evolutionary
search so you could imagine using an llm to do the crossover or the mutation of
the programs that are there in your pool and you can also use n llm to do the
obstruction which is that you could ask the llm to to come up with some of the
concepts that are showing up inside the high performing programs right and then
those Concepts become a a condition under which they they basically condition
the search of her of her programs at that point so I spoke with um sabar kamti
very recently and he's got this llm modulo architecture you know so he said llms
are very creative so we you know we we can kind of like Traverse this space and
and then we stick a verifier on the end you know so we actually we can kind of
cherry pick when it actually getss it correct right but I had a bit of a
disagreement with him because certainly when we let the llms um find creative
things when when we're doing let's say llm guided search and when we let the
llms do abstraction I feel that they are still somewhat parasitic on the data
that they are trained on which means there is a kind of creativity Gap we seem
to have access to a source of creativity which is richer and and then there's
the thing where we're building up this Library and at some point does the weight
of the library kind of affect our creative ability that's a fantastic question
uh so one thing I would add is that in settings like symbolic regression you
have the advantage that you have grounding provided by the the data at the end
of the day what you're trying to do is you have seen some empirical you have
made some empirical observations and you're trying to find Expressions that fit
the those those observations right so now when you have a new candidate that is
creatively constructed by the llm you could imagine actually evaluating that on
your data set and seeing how well it does right so that's something that
prevents it from going off the rails completely now um regarding the the prior
knowledge question yes absolutely llms are drawing on the prior knowledge that
they have seen and and if you're using llms in a purely blackbox zero shot way
then uh you are only going to be constrained by what the llm has seen before now
I would add that this is still a there's still a non-trivial value in that prior
knowledge because when you are doing new science you are typically building on
science that other people have done before and the llm has presumably seen that
in the form of various sorts of scientific papers and you know math problems and
and so on but that said you know you don't have to be stuck to this zero shot
blackbox model you could imagine a loop where you come up with candidates
creatively using an llm you empirically evaluate these candidates and then you
use the the experience to basically fine-tune the model further and you could
even imagine a universe where you are starting with an llm that is completely
Blank Slate maybe it has some Elementary knowledge of language but not much
science and then you are just progressively building it up on all manners of
scientific tasks and it's seeing you know how various kinds of hypothesis
performed it's getting feedback from The Real World right in the form of
experiments maybe it can even go ahead and do new experiments right reason about
uh causality and and and determine what are some of the new experiments to try
out and then get feedback in terms of the results of those experiments and then
use that to to uh we can use that information to fine tune it further right so a
lot more is possible than just using you know an llm and then uh as a black box
and then just having a verifier um at the end I agree with that and there's
always this discussion about creativity I mean Demis is be but Demis hassabis
spoke about the ladder of creativity with the inventive one being the the
highest strength of course you know we can we can imagine unicorns we can
imagine things that we haven't seen in the real world because they're still
composed of Primitives that are in the convex hole of of things that we
understand but in the in the context of of program generation though so language
models they have so many degrees of freedom you know they understand you know
natural language and like madeup languages and programming languages and so on
and then we can do things like generating code and we can use um dsls and even
even then if if if if we execute a bunch of these programs they might not halt
or they might not be valid so there seems to be like another step we need to do
to actually check that these are these are good programs to run that's right and
uh by the way you can get more forms of feedback than just whether or not this
program ran correctly on a few tests you can do more serious kinds of analysis
of programs as well but at the end um yes so you are getting all these extra
forms of feedback uh from those external tools and then the question is what do
you do with that right so you could just use that to decide whether or not you
keep this program uh but you could do more maybe you could go and go back to the
the llm and and use this information to basically train it further and uh guide
the way it writes programs and if you think of human programmers that's how it
happens right so you write code and then you try out various sorts of things and
then you uh see that certain kinds of programs work and certain kinds do not you
get feedback from your compiler your type Checker your interpreter right and
then you use that to refine the way you code as well yes even with the hting
problem I mean I I have some idea in my mind that this is I don't know it's a
it's a quadratic algorithm and it's got a thousand data points and it's still
running after 90 seconds probably there's something wrong here control C I go
back fix the Buton yeah and and you know there is a huge body of work on uh
solving the halting problem even though in principle this is an undecidable
problem in practice this literature on proving termination of programs the way
it works is that it recognizes that proving termination of a program is really
about coming up with an inductive argument so what you're showing is there is
some kind of uh an expression whose value goes down strictly each time you
execute one step of the program so if you think of a loop right so you have
written a loop where it says that while I is less than n you know something
something and then I gets incremented you know that this program is going to
terminate uh you know in spite of alen touring the the reason is that what's
going on is something very simple each step of the loop you are incrementing
this I and it can only go up so far right and so there is this value which is n
minus I which is strictly going down in every step and it can only go down so
far it cannot go down below zero because zero or whatever you know lower bound
you have set because of the way your program is structured and so this kind of a
reasoning that you're doing here right this is an example of an inductive proof
uh except applied to programs and there is a lot of work on automatically
discovering these sorts of inductive proofs which are really you know very
simple symbolic Expressions right and you could imagine using an llm or other
kinds of machine learning techniques to search for these sorts of arguments
couple of points on that and maybe you should bring in turing's famous proof
because that he proved by contradiction didn't he about the the hting problem
but but also if I understand correctly you're pointing to specific instances
where you can do proof by induction that a program would would halt but but
would you accept that there are still a space of programs that that you wouldn't
be able to do that um so I didn't say anything about automatically discovering
those uh inductive proofs right so so my point is that for a vast number of
practical programs in fact most Loops that people write or most recursion that
people write the argument for why these programs are going to terminate is very
simple and you can search for those kinds of uh proofs um using various sorts of
methods even just basic enumeration Works quite well but you could imagine you
know using more contemporary machine learning techniques to solve this problem
but you cannot possibly have a method that is going to be automated and it's
going to sort of uh uh it's going to always terminate and it's going to work for
all programs no but the question is that you know for realistic programs uh will
this work or not and we have every evidence that uh for realistic programs that
people write uh you could just do one of these things you could try some of
these strategies to prove termination and if that doesn't work you just say that
okay you know there is a problem here just go fix it right and maybe there is
some reason why that program would still work but you know whatever you know you
can just ignore that program and find a different way of solving the problem so
my co-host uh Dr dgar he's really interested in in touring machines and he says
you know language models there I mean we're just we're not talking about llm
systems we're just talking about just a language model he said they are finite
State autometer and um a touring machine still has a finite State autometer as a
controller for these kind of push down autometer and he said you know so that
there there's a a space of algorithms in the FSA class he would actually call
these touring machine algorithms even though they are for a finite State
autometer that cannot be searched discovered with stochastic radient descent
because of this halting problem now I think you were pointing to earlier some
interesting research that's been done in this space I mean he would be
fascinated in that right right yes uh so there's been a whole lot of work on
using gradient descent to solve program synthesis and to me searching for
touring machines it's just a form of program synthesis it's just the programming
language is extremely lowlevel it is the uh that every program has you know
access to this one counter uh the the tape and then uh and then also a
controller which is a finance State machine right so to me this is a very simple
kind of programming language um and it was useful in mathematical proofs in the
theory of computation because it was so simple right but I don't think that
there is anything special about touring machines from the point of view of uh
programming right anything any reasoning that you can do about touring machines
you can also make the same kinds of arguments about other broader class of
classes of programs now there has been a lot of prior work on doing gradient
descent to find programs and these have not been very successful for the reasons
that you are alluding to yeah and that's why people have historically uh wanted
to use neural networks in a sort of guiding role that you are still going to
have some kind of a discrete search going on and then you would um you know uh
use a neural network to guide that search process in various ways and I would
say that the use of neural networks in dreamcoder is an example of this but also
the use of llms to write programs or guide searches over programs that's also um
those are also examples of this interesting so um touring machines have this
amazing ability to expand their memory so we don't we don't need to train the
thing again from scratch we we can just say I need I need to I need to get some
more data I need to get some more data to add to my memory and people say well
um you take a language model and you can train it to do rag so even during its
training process presumably it's actually retrieving things from from a datab
base or you could train it to do code execution and then you could say well
aren't we basically searching touring space because I can I can say generate me
a program that computes the nth digit of pi yes uh which is something that you
know has a has an arbitary um runtime and um and and then I can run that on on a
tool and then I can pass it back in but it feels to me that there's a difference
in kind right but but what is the difference what's the difference between doing
that and actually having a machine that can search Turing space natively okay so
I'm trying to understand so um you could imagine having the definition of the of
the touring machine programs as as just a DSL right you could Define a
programming language that's where each program is a touring machine right so to
me this is this is just what you would do if you open a theory of computation
textbook if you go to the definition of touring machines it's just a programming
language right there is a syntax there is a semantics so now what is the
difference between training an llm to generate programs in this language and um
any other kind of program synthesis that llms already do right I don't think
there is a fundamental difference uh between you know touring machine generation
and python code generation now I think what you describing though is something
slightly different which is that the process that is being used for this
generation you know is that process a finite State process or is that process
something more like a touring machine and that I think is a very interesting
question right so what you're really saying that instead of having a language
model which is just operating which is a strain in this particular way that it's
just predicting the next uh token and uh and yes maybe it can retrieve us a
bounded amount of information maybe you know instead of having a massively
scaled up llm uh massively scaled up Auto regressive model you could have a
massively scaled up touring machine that is doing all sorts of generation right
and I think that's a very exciting idea well yeah exactly and the the thing that
it took me a while to get my head around is is the the controller in a touring
machine is a finite State autometer so that there exist a set of Weights in a
language model that would allow it to you know to to expand its memory with some
push down autometer or something like that so we just can't find it with
stochastic gradient descent and um the the other thing is yeah I completely
agree that we could in principle imagine we had a huge data set of internet
scale of touring machines and descriptions because I think the descriptions is
important because what's the point in having a touring machine language model
that we can't program in in any way so there needs to be some kind of
intelligible mapping to something that that we could use to instruct it right so
again though I would make a distinction between the what is generated and how
you're generating it so there are two different possibilities so one is that you
use a language model whether it be a touring machine language model or U an RNN
language model or an you know uh a Transformer language model you're using some
sort of a language model to generate programs in this touring machine language
so that is version one okay version two is one where you're making the specific
point that this language model itself is a touring machine that it goes it has
this ability to you know access this unbounded memory and it goes and you know
looks up stuff uh uh from from this this infinite tape this unbounded memory and
that is something that is a very interesting proposition my one hesitation there
would be that we are finding out that the architecture may not matter that much
after all uh what really matters is the scale so there are all these new results
about you know State space models and and highly scaled up rnns and we are
seeing that many of these tasks for which Transformers seemed especially capable
um are also being done by these extremely scaled up rnns right so I think that
you know it is possible that this touring machine architecture is going to lead
to you know amazing new capabilities but I would probably um wait to see some
more evidence on that but that said it's definitely a very interesting idea to
explore yeah that there's always the objection of well for all practical
purposes it doesn't matter either because we can scale up the models and I'm
very excited about you know Min lstm State space models and and mber and all of
these things because they can allow us to possibly 10x our model size and then
there's always the question of well at at some point the models are going to be
big enough to do all of the the reasonable types of computation that we want to
do but the counterargument to that is you know we we sometimes spend a lot of
time pondering problems and you know the the Linux operating system Keith always
gives this as an example you know that we've had to design some really
complicated artifacts to reach the level of you know technological complexity
and and maturity that that we have now and it seems Out Of Reach of of these
models even if we hundredx them that's right that's right yes so I think that um
you know I'm a big believer in having algorithms that are that go beyond just
the the um Auto regressive language model Paradigm and that's why we were
talking about these methods where you have these external tools like um you know
code interpreters or or you know leanover or theorem provs like lean and uh
using feedback from them to do something um more than what we could do with auto
regressive models but to me the power of these methods come not from the
internal architecture of the language model but more in the higher level
architecture of how these different kinds of grounding mechanisms work together
together with neural networks right and I think that that's uh it's it's
possible that a different neural implementation of of llms is going to give you
drastically better results I may be a little bit skeptical about that it's
something I would like to see uh more evidence of but what to me is very clear
is that if you have these sorts of higher level uh architectures where you are
combining neural networks of whatever sort right with these kinds of um symbolic
grounding mechanisms um executing in the real world human feedback U all of
these things uh you're going to get something better than what we have today and
to me the challenge then is how do you pass back feedback from these various
sorts of grounding mechanisms back to the neural network and maybe when you are
doing so certain kinds of neural architectures are going to uh be a lot better
but that is something I'm I'm still kind of on the fence about I really agree
with with what you're saying I mean one thing I've noticed is right now
certainly building real world applications the way to overcome this complexity
curse is with architecture and process and it's the only way to to robustify
these things possibly the only trade-off though is the more engineering and
architecture you put into a problem you're kind of robot busying it for that
problem but you're also somehow taking away some of its generality and other
problems right so this is why I would ideally like to see something quite simple
um an architecture that is quite simple and and domain General but it seems to
me that there are a few examples of this so you know let's take mathematics so
to me mathematics is a an an a very useful model for uh doing a lot of different
Kinds of Kinds of solving a lot of different kinds of problems um so for example
if you're doing physics if you're doing uh biology if you're doing programming
mathematics is useful even for day-to-day logical reasoning mathematics is
useful and so I could imagine that U the use of a a tool that can give you
rigorous feedback about um the mathematical soundness of your models of the
world uh to me that makes a lot of sense and so I would probably not consider
that a restriction on the kinds of uh approaches that uh or on the kinds of
domains that you can apply your methods in likewise code execution to me code is
a very general uh model way of representing models of the world and programs to
me always come with semantics so being able to execute programs and also analyze
them and you know reason about sort of worst case behaviors and so on this is
also something that I don't think imposes a massive restriction so to me the
idea would be that you would have these sorts of grounding mechanisms that are
fairly General and then you would have a flexible uh way of composing them
together uh you wouldn't impose you know you wouldn't hardcode a lot of things
uh you would maybe hardcode when you are deploying these meth methods in
particular applications but the framework should be perfectly General where you
can write out you know new kinds of complex compositions of say lean proofs and
code execution and neural prediction and maybe some natural language processing
and vision as well why not right so you would allow compositions of all of these
different kinds of modules into new kinds of models and then you would you know
maybe let a uh an AI system just go and try to find the right composition can
you tell us about the laser architecture absolutely the laser approach uh the
goal of this approach is to to um use llms to drive a search over programs and
also to come up with obstructions that um explain what is going on in h
performing programs this was done in the context of symbolic regression where
the setup is that you have a you have a data set and you have a language of
programs or expressions and you are trying to find a Hy performing expression
now prior approaches here they used evolutionary search and there is also some
work that uses um llms to basically direct some parts of that search process but
what we were really exploring is that can we use llms to come up with highle
explanations or high level Concepts that show up in the high performing programs
and so you could imagine a process where you know Evolution research is coming
up with a pool of candidates and you are actually evaluating these candidates in
a using the data that you have and so this serves as a grounding mechanism now
you have a bunch of high performing candidates left now you're using the llm to
to explain what are some of the common themes that are showing up in these these
high performing programs and then you are remembering those themes those
Concepts and then using those to drive the search as well right so an approach
like this one big appeal is that even if you're not using all of the you know
the scientific prior knowledge that the llm has just the ability of llms to
abstruct pieces of text into higher level Concepts that is something that is
still very helpful um so uh we deployed this approach in um the problem of
finding rediscovering a bunch of standard equations so specifically equations
from the all the equations in the finan lectures on on physics uh this is a task
that was proposed in this AI findan paper by Max tar and and others and in
addition we also evaluated the system on some synthetic benchmarks and we also
used it to do a new discovery of an actually an llm scaling law oh tell us yes
absolutely uh so uh here we wanted to go beyond the chinchila law we wanted to
come up with a new law uh just uh using data on llms so you have you know
information about uh for example number of parameters the size of the data set
uh um and you know how many shots were used in in in training and and so on so
you have a bunch of these parameters and then you have you have also data set
characteristics right and then you have performance and so now you could ask
this question that uh can I come up with a can I discover as a symbolic law that
is going to um explain the llms Behavior now what we found was that we have this
uh uh we got this law that was a little bit different from the chinchila law and
that was definitely an objective that we wanted to find something that is
different but yet as explanatory and yes for more details please see the paper
but in addition to that we also evaluated the system on completely synthetic
tasks and there also we found that um this concept learning idea made some
difference so even if you ignore the lm's prior understanding of the problem
domain which is not something I would argue you should do because at the end of
the day in real world applications you are building on pre-existing knowledge uh
but even if you ignored that uh bit you still have uh another way to use llms
which is as a tool for coming up with abstractions yes and I'm also inspired by
Melanie Mitchell's um she's done some work in in in this area there seems to be
something really interesting about iteratively abstracting that's right which is
to say that there's almost some fixed out a loop and you're going up and you're
going up and you're going up that seems tell me about that that would make a lot
of sense uh the way we are doing it right now in laser is a little bit less
sophisticated we have our obstructions described in just natural language but
you could imagine a world where you have these obstructions represented in a
more symbolic programmatic form as well and now as time goes by your
obstructions you are deliberately designing these obstructions to be higher and
higher level uh that is not something that we have done but I would say that
that is something that's present in dreamcoder because in dreamcoder you uh do
have once you discover some Library modules you can write new programs using
those Library modules and then you can abstract them further right so this
abstraction process it is naturally directed towards discovering higher and
higher level modules and could you make a quick comment as well that this is to
me it's so exciting it it's not currently so I mean certainly dreamcoder for
example isn't soter on on the arc challenge but I have a a a deep kind of I can
feel it in my bones that it's the right way to go and unfortunately because of
the soer chasing and and and so on there isn't enough attention being being paid
to this really really Innovative work I mean what what are you Reflections on
that I think that sorta chasing is is a really unfortunate trend um it is also I
think um it's a misallocation of resources there are companies that are well
suited to chasing soda because you know you need both exploration and
exploitation and uh chasing s would be exploitation right you have a well-
defined approach now you're scaling it up you are you are um solving new
problems that that you couldn't do before great but I think there is also this
exploration direction that is very important and unfortunately s chasing is uh
is hurting that a bit but at the same time I would say that there are a lot of
folks that are that are coming up with new interesting algorithms um what needs
to perhaps happen is more of an arc from the exploration to the exploitation uh
so in other words words you know let's say that you have this this algorithm
like dreamcoder how do you scale that up okay so our laser method is one way of
scaling it up a bit uh by using llms but maybe you know there are other
approaches as well and also there is the question of how can you connect this to
run this on very very large amounts of compute and and then uh can we see what
happens now this is something that uh we haven't done yet but that's that's a
direction that we are definitely very interested in we are speaking with various
uh Partners uh to see if there's any way of scaling this up fastly um and we
would be very excited to know what happens uh uh once we do that you've worked
extensively on mathematical Discovery and uh I think you made the comment in one
of your papers that you think we might have an AI co-pilot by 2026 what makes
you think that that was actually a point made by Terren ta oh my apologies whom
I greatly who I greatly respect um and I actually agree with that so I think
that um we are in an extremely exciting time in AI for Math and I would imagine
that um getting an AI as a significant contributor although not the you know the
sole author in a math paper uh or even a computer science paper with significant
mathematical components should be should be possible uh in the not to distant
future now okay so what do we really mean by that uh so you know if you think of
the way mathematics is done and even actually what happens in theoretical
computer science you have these definitions uh that are pretty rigorous uh but
ultimately uh and and you have proofs uh but ultimately the purpose of these is
to convince human reviewers and human readers right and so what that means is
that you can make mistakes there are Corner cases that you can you can uh forget
and your proofs may be broken as a result of that so this is one possible risk
uh from the way in the way mathematics is done today the other thing is is just
scaling up right even if you don't think that there is anything fundamentally
wrong with the way math is is done today there is an opportunity uh to scale up
mathematics using computational tools uh that was just not possible until now so
what I mean by that is that if you think of you know a very large Software
System if you think of say the Linux kernel or the Google Cloud infrastructure
these are extremely complex systems that no individual human can necessarily
fully understand people understand these systems at the high level of
obstruction and maybe they know you know all the low-level details of specific
components but I would say that there is really no one or at least very few
people who have a detailed View of the of the entire uh system all the way now
if you think of math proofs historically math has been very oriented towards
these um individual contributors so when you are thinking about a a
mathematician it's somebody who you know they produce a proof and this all the
details of the proof they they know right and and they have produced it
themselves or at least they have understood uh those details but imagine a world
where you have these extremely complex mathematical theorems where uh maybe you
know no human is individual human is able to understand all of the details but
you still have the guarantee that the overall proof can be broken down into
these pieces that are more manageable by humans right just the way we write code
could we do that for mathematics what would that look like I think that that's a
tremendous opportunity that these systems like lean provide and now a naturally
comes in just the way AI co-pilots have made it much easier to write code you
could imagine having AI co-pilots writing math proofs as well now if all of that
is possible so we'll have maybe new kinds of mathematics new modalities of
collaboration between humans and this is something Tera has uh extensively
talked about um and then AI driving this process making us 10x more productive
would I say that that would lead to know new papers with uh with AI contributors
I would say yes now you know maybe we wouldn't list the AI as a co-author
necessarily uh because uh just like we don't you know list our calculators or
computers as coauthors uh we probably would just accept that okay you know there
is this tool over here and it did a bunch of things but but uh there is still
human creativity at the higher level and those are going to be the co-authors
but I would say that the AI would definitely still still uh do a lot of things
that today a math grad student has to do interesting so we are seeing I guess a
lot of people think about mathematical theorems as being quite parsimonious
units that um an individual mathematician or or a few mathematicians have have
worked out and understood and we've I guess not until recently thought about
what would it look like for this to scale massively right and so yeah we need to
convince the reviewers and you're saying that the reviewers even though it's
increasingly inscrutable because it's so large the reviewers would be more
inclined to trust it if it were found by a computer so I would even question why
you need a reviewer to understand every single detail of the proof right maybe
the reviewer needs to understand the high level components of the proof and then
just uh have an assurance that the lower bits of the proof are done correctly
just like when you are reading code you don't necessarily think about okay here
is a system call that this code made is this system call implemented correctly
at the assembly level you don't reason about that it's something that you assume
that the Linux kernel implementor has properly figured out right so in the same
way one could imagine proofs where the proof is at the higher level of
obstruction and then there are these lower level building blocks that you are
you are uh taking for granted now also one could imagine you know just like when
when you're building a big system in software you break up the system into
pieces you pass these responsibilities onto different folks and there is an
interface where things are supposed to check out and so long as they do uh and
there are tests that pass uh at the unit level and end to end uh you just accept
that this system is okay right so likewise you know maybe for mathematical
proofs we should also have the same sort of of decomposition you would have this
you know big complex proof let's say we are talking about pharma's L theorem
which took an individual human a very long time to prove right but maybe now
you're going to come up with decompositions you're going to have a team of a
thousand mathematicians that go and look at the pieces and then there is some
way of assuring that assuming these pieces are done correctly everybody fulfills
their local obligation the global goal of proving pharma's Last Theorem is going
to be true so I'm I'm fascinated by that by this idea of kind of decomposing a
larger hole into these local obligations let's look at the Linux operating
system do you think there is some kind of a bottleneck introduced by having
these human intelligible interface modules at the local level and what I mean by
that is I can imagine a future where language models are so powerful they can
they can just regenerate the entire code all of the time but that's going to be
a nightmare for checking in code isn't it because you know John I've just broken
John's component and this interface has changed and the schema over there has
has changed so do you think there's always going to be an interesting kind of
tradeoff where in order to have an interface that is consistent we'll need to
almost in like increase the complexity of of the local modules right so I think
this goes back to this discussion of interpretability and and capability so I
think that in principle it is possible to come up with a uh Linux kernel that is
written entirely in low-level assembly code and it is it is not modular it
doesn't have these sorts of human comprehensible interfaces right but yet it is
provably safe and by that I mean that you have these high level objectives that
some set of humans have written down uh of what are the properties that the
Linux kernel needs to satisfy and then you know your AI goes in and produces
this massive blob of Assembly Language code and then there's also formal proof
that this code is actually doing the right thing right so then why would be have
any objection the issue to me is that number one there is that kind of AI is at
this point fantasy we don't really have any AI that can produce you know large
bodies of Highly reliable code without any kind of human intervention except at
the very top level of doing some specification um and also you know over time
requirements are going to evolve and uh you may you want to have a path through
which humans can be involved in the in the maintenance of this Linux kernel of
yours and I think that the same sorts of argument apply to mathematical proof as
well there is a world where all math gets done just via uh you push one button
and then the math gets done so the mathematician comes up with this theorem they
State the theorem and then they push a button and then your AI goes in and just
comes up with a proof in the lowest possible level without any kind of any kind
of uh human interpretability but there is a proof Checker namely let's say the
lean proof Checker that has checked the proof for you right so I think that this
is possible in principle in practice we are very far away from that so at least
in the short run we want to have proofs that are at least you know uh
interpretable at module boundaries and uh then humans can be involved in
designing the high level process and then the machine takes care of the
low-level uh details but I could imagine a world where humans are less and less
involved although you know that would raise some questions about what's the
point of this mathematics you know part of the reason for mathematics is that
it's fun it teaches us something about the world but you know if the point of
mathematics is that it's purely an instrumental thing that uh you are doing this
mathematics so that you can predict whether or not I don't know a certain kind
of chemical reaction is going to take place then maybe that's something that you
can allow the AI to do just like today use Mathematica or or or mat lab uh to to
do a lot of that uh simulation so um what are some of the advancements in this
area I me I know you've done a lot of work in in this area what what should
people look at right so there are a few different directions uh the direction
that's the most well studied is theorem proving and so here there are couple of
versions one version is that you are starting with a formal statement of the
theorem in a language like lean and then you are searching for a proof of this
theorem so in a framework like lean a proof is just uh it's just like code it's
a sequence of instructions which are in that setting uh called tactics and so
you are finding a sequence of tactics that's going to lead the goal to be proven
which is really like finding a program that's going to achieve a certain
specification and there's a lot of work on this uh the most promising approach
is they combine the use of a neural network with execution in the um lean
environment and you getting some feedback uh as to whether or not you know the
decision that you the tactic that you applied led to good things or not and then
you would use that feedback to to um do more generation so that's sort of what's
going on there there is also a body of work on informal theorem proving where
you have natural language problem statements and you are using a lot of the
times purely informal methods like you know the sort of variant of Chain of
Thought uh to to do math reasoning but sometimes you're also combining these two
approaches so there was this um nice paper by Shan wallak and and others on uh
doing using a natural language model to come up with a highlevel proof sketch
and then using that proof sketch to drive a formal prover what was the name of
that paper draft sketch proof yeah and uh so that's One Direction theorem
proving formal theorem proving and also informal theorem proving there are also
a lot of other interesting questions which are less explored One Direction that
is uh really fascinating is sort of open-ended exploration um if you think of uh
what's really needed in mathematics uh what can AI contribute one big
opportunity is in coming up with better conjectures creatively coming up with
better goals uh that uh you want to prove not just the pro proofs themselves but
but yeah also the also the statements of the theorems so that's a direction that
I think is extremely important but um unfortunately there hasn't been that much
on that so far uh but there are several research groups that are very interested
in that problem as well and um and so for example uh there are these uh efforts
where you know you have a so Noah Goodman had this really uh nice recent paper
on using intrinsic motivation to to drive a approver uh so the idea there is
that you are you have these two agents so you have an agent that is coming up
with new claims and you have a different agent that is trying to prove them and
so really you know you have this interplay between the process of conjecturing
and the process of proving which is really what happens in in mathematics if you
think of it so um last night I read your copra paper which which was really
really interesting and I mean you already spoke about lean in in high level
terms but maybe you could go into a little bit more detail but um essentially it
was an algorithm to um you know you have a theorem and then you have all of
these obligations and then the algorithm would um resolve using a language model
these lemas and then um it would then recursively um kind of call itself until
it ran out of obligations and I guess theistic part was was using the language
model to find an appropriate Lema from this Lemma database and it's a
fascinating architecture can you tell us about that uh sure so uh one thing here
that is uh in common with all of the other lean theorem proving or formal
theorem proving uh efforts is that there's this overall structure of a formal
prover and the idea there is that you have a goal that you're starting out with
a a top level theorem that you're starting out with and then you're
progressively applying these tactics which are simplifying this goal into sub
goals right and after a while assuming you have selected a good set of sequence
of tactics you have no more goal left to prove and then you're done your theorem
has been proved QED right so this is just lean this has nothing to do with AI
mhm now the question is that how can you use AI to select tactics in a smart way
and there the copra paper made a few contributions one was that you are just
using a large language model um without any kind of fine-tuning you were just
prompting it to guest tactics and this is different from prior work where uh
folks used models that were explicitly fine-tuned on uh proof data formal proof
data now what was sort of remarkable to us was that even just a blackbox model
uh could predict reasonable tactics for for um this sort of formal proof even
though the language is fairly esoteric now an important point though is that it
wasn't enough to just query the language model you also had to do this llm
modulo thing where you are getting the tactic predicted by the llm and then you
are using that to actually change the you executing that tactic in the
underlying lean framework and then you're getting back a new state a new set of
obligations to prove and then you're going forward with that right and the llm
can actually see what the current obligations are and also actually some some it
has some memory uh from the uh from the past and all of this is plugged into a
bigger search right and this search process is doing backtracking it's recording
what failed what didn't work or what worked and what failed and all of that
information is being used to guide the generation process of the llm so that is
one idea and then the other idea is that you are doing retrieval um now here the
intuition is uh that when you're doing math typically you are using definitions
from other projects uh and you're using lemas from other projects and the idea
of using these these um sorts of external knowledge bases this was used
originally introduced in uh this model called reprover led by Caillou Yang who's
now at at uh meta doing AI for math research and this reprover model uh was
fine-tuned but here what we wanted to explore was that could we just use a large
language model in a few shot way uh to uh do the same sort of thing and we found
that yes it was able to use this retrieved knowledge uh from external databases
and so what that shows really is that in context learning can go a long way even
in this sort of very esoteric setting of doing formal theorem proving yes and
you you tried it on gbt 3.5 turbo and gbt 4 you noticed that there was a
significant Improvement of gbt 4 you you ablated the retrieval and the retrieval
helped dramatically I think you limited it to about about 60 steps but
presumably if you went for longer it would have been even better and um the
backtracking presumably had some notion of I'm in a bad State now I'm going to
go back how did that work so the good thing about a formal framework like lean
is that you are getting information about what is a what what kind of state is
bad right so if you are if you are at a certain uh state of the proof uh you
have a certain set of obligations to prove now you take a tactic that's not
helping uh or in fact that is just not applicable in the current state then
you're going to get feedback or for example if you're finding that you are
cycling back to something that you have already a state that you had already
seen and so you're basically going to end up with an infinite Loop in the in the
state space then that is also something that uh you should avoid right and this
kind of information you can get by explicitly embedding the llm inside a broader
search process I think again though that the that the main finding in that paper
is that in context learning can be interesting uh even in this setting now we
limited it to 60 because we were working with an academic compute budget and
also gbd4 was fairly expensive at that time but I think that going forward as
the models get cheaper it would be really interesting to see how far this sort
of llm plus uh search plus external grounding through through lean or other
kinds of Frameworks how far this can be pushed I think that it can actually go a
long way especially if you are willing to do export iteration which is that you
collect data and then you use that to fine tune the model further and and you
carry on like that a couple of things so I'm I'm interested in this concept of
reachability so so you you have um a whole bunch of tactics in in a database and
then there's there's some notion that we've been kind of pointing to about the
convex Hull of the tactics giving you some reachable space that's right so so
maybe we should talk about that convex hole but presumably there would be
examples of of um theorems that have a goal state which is not reachable um with
the tactics I mean could you talk through that right so there are really
low-level tactics that would uh enable you to really find anything it's just
that the there may exist a sequence of tactics that lead you to that uh goal
state but it may be so long and so complicated that your AI may not be able to
find it and that happens all the time there are lots of statements that we are
unable to prove now I think one interesting question is that do you um expect uh
to do better if you were able to abstract these sorts of lowlevel tactics into
higher level tactics and I think the answer is yes right if you think of how a
mathematics student progresses you start with really basic algebra and and or
maybe even before that you start with arithmetic and then you you get to algebra
and then suddenly you have this big leap and then you get to calculus and you
know you you learn probability and then you get get even more abstract um you go
to complex numbers and and so there is this hierarchy of abstractions that a
human student goes through while learning mathem matics and the purpose of these
abstractions is that you are able to be more robust you able to handle more and
more kinds of problems uh so you're unifying a lot of sort of Point Solutions
into into General Solutions and I can imagine that that approach would be
valuable even in this context uh of AI for math that you would start with some
low-level set of tactics but then maybe in this kind of dreamcoder way you're
going to discover more abstract tactics and then you would be using those uh to
do more suing proofs and then stuff would just explode at at some point that you
You' be discovering new kinds of mathematics how does the resolution play into
the leakiness I mean I'm certainly thinking about in physics for example there
are you know Newtonian mechanics and relativity and so on do you do you
introduce leakiness by relying on higher level abstractions not in this setting
of formal proofs and the reason is that the way a framework like or other there
are other ones as well uh these Frameworks are architected you have to have
certainty all the way through otherwise your proof is not going to uh be
accepted and so even if you are at a higher level of abstraction you are going
to have implementations of that high level primitive in terms of lower level
Primitives that actually are are sound now that said you could certainly imagine
versions of this uh where that is not the case so for instance you could imagine
a version of AI for mathematics where there are some low-level or or some some
proof obligations that are just sort of empirical right imagine that I'm making
a statement that um I don't know maybe this is not a universal mathematical law
but maybe it's a property of a certain place and and and time right so maybe you
are you have a predicate that you just evaluating empirically now you could give
it mathematical meaning uh by making it into a probabilistic predicate but you
don't know that you know the distribution that You' have selected is the right
one right so in so in that case what would happen is that the more high level
your resolution or or the cors seror resolution uh the more uncertainty there
would be but you would still have some amount of um if you're using you know um
formal mathematics above that level you would still have some amount of
assurance about the claims that you are uh making so it would be not that
different from you know when you're using math in in um in a natural science
there are empirical observations that you're making and there is noise in that
right but you are at some point abstracting them into this cleaner mathematical
model and all the inferences that you're making based on that model they're
conditioned on your assumptions your modeling being correct right and I think
that it's not that different from this that if you have two course scen a model
you are going to have you know more uncertainty regarding your conclusions right
it's not a01 that it has to be they're fully certain or or completely uncertain
I was speaking with um David SPAC recently he's is very well known in applied
category Theory and he was kind of saying that our entire epistemic framework
almost derives from the questions that we ask and I wonder whether it's a
similar thing when we talk about theorems and and the utility of of theorems and
the role of humans in creating the these theorems um that there must be some
kind of you know reason why we're asking these questions like where does that
come from I think that for a lot of mathematics it's been inspired by the goal
of solving real world problems if you think of why people came up with geometry
uh why people came up with Calculus I think there was a very pragmatic goal that
you wanted to understand how the world works and you wanted to then apply it to
to do new things to to solve real world engineering challenges and so so I think
that that's often the starting point but then of course you know there's this
motivation of Elegance as well that and curiosity that you want to have Elegant
unified Solutions rather than Point solutions that are just hacked up um and you
also are curious that okay so I have made these sorts of assumptions in this
definition what if I change these definitions in this way what would happen and
I feel like if you just combine these these ideas uh the idea of modeling
phenomena that are that are visible in our uh day-to-day lives and combine that
with these motivations of curiosity where you are just asking okay what if I did
this what would happen and unification of Point Solutions into something more
abstract I think you would get to a lot of mathematics that way could you expand
on that a tiny bit so what if you could break this down what makes a really good
mathematical theorem I am not a professional mathematician so I'm probably not
the best person to ask this question maybe I can talk about computer science and
and I can try to answer this question for let's say theoretical computer science
papers because I come from that community so there I would say that um one
question is uh whether or not this there's this question of interestingness yes
yes so what is interesting um I think that it should be clean the problem that
you're trying to solve uh it should be a clean statement it shouldn't be that
I've come up with this Bizarro definition with n different uh case cases and
then um I want to prove a certain theorem about that right so it would it should
be something that is relatively succinct elegant and then um it should be novel
so if it feels like I have seen n versions of this before and I can take a proof
for one of those previous models and this tweak it a little bit and then the
proof comes out that's just not worth pursuing so I think novelty and elegance
are big criteria then I would say that in computer science specifically utility
is a consideration as well the reason why computer scientists often care about
certain kinds of theory is that that theory models real world computational
processes so there was in an interest in in say online algorithms because uh you
know there were there were many practical computer systems that needed to
process data online there was an interest interest in algorithmic Game Theory
Because the Internet came about and then all of a sudden we were departing from
this traditional centralized view of the of the computational world instead the
internet was this massive computer and you had all these agents that were driven
by their own objectives but they were coordinating using this let's say an ad
auction or or uh any number of other kinds of online coordination mechanisms
right and that led to all of this interesting work on on algorithmic Game Theory
where it was asked that all right so let's say that I have these K different
agents and they are arriving at an equilibrium right which is this uh this
market right um the the the equilibrium of the market but um I want to now ask
in contrast to traditional Game Theory can I reach an equilibrium in polinomial
time right is this equilibrium not only reachable but computationally tractable
uh to reach so the way I see it a lot of interesting computer science theory has
happened by taking these sorts of long-standing principles in math and and prior
computer science and then adapting them to these um new settings new models
which are inspired by practical problems on the ground in in in um computer
systems game theory is a beautiful example absolutely beautiful I mean I'm I'm
interested in ageny and that's a a wonderful example of one of these just it's a
phenomena in the natural world yes and it it beautifully demarcates certain
dynamics of of behavior and so on and then we create this game theory thing
which is also using the concept of an agent and it's it has this unreasonable
effectiveness of modeling many um you know comp Lex systems even though we
choose to model the the agents at at different scales and even mixing different
scales inside a model but coming back to your definition of really good theorem
though um you said clean and I think you were talking about like Pony but you
know Chomsky said that uh llms aren't a theory of of language because they they
don't have that clean demarcation they don't it doesn't demarcate what he thinks
is language versus anything else like an impossible language or or something
random so is there something about this this demarcation I think that llms um
would be would produce whatever is it's there in the in the training set right
and and and some amount of composition thereof so I think that if an LM was
primarily trained on beautiful theorems and beautiful literature I think that
you would see certain certain um aspects of that in the the text that they
generate as well however I think that that clean that Elegance also it's subtle
it's not just about following certain high level motives of beauty but it's also
about um being consistent so a lot of the times for example when I use llms for
writing I find that okay this paragraph is really well written nice but then the
next paragraph is somewhat different it's it may be you know individually fine
but then when I put the two together it just becomes something horrendous right
so I think that this idea of Elegance it's it's a sort of a global notion that
it's not just that you know little pieces of the theorem are cleanly stated and
therefore the the the entirety is uh cleanly stated as well um so I think that
to me it's a very open question that can an llm come up with uh with elegant
theorem statements H I don't know that the answer is is no or or yes and just to
close this off because you you did sketch out in your ablation um going all the
way just to a zero shot you know Blank Slate gbg4 wasn't gbt 4 wasn't it and um
I think it got something like 2.3% if I remember correctly and then it sort of
ranged all the way up to about 30% with with with all of this coera algorithm
and the retrieval and the backtracking um the thing is that there's always this
nagging thing in the back of our minds about the test set contamination that's
right um and you and you did some little bit of work on on that could you talk
talk about that yeah so this is a very difficult uh issue with LM based approach
there is always this worry that that the results you're seeing are because of
contamination now we did what we could to address this issue uh and what that
means is that so first we showed that if you strip out all of the extra pieces
that we added we just asked uh the llm to go and produce the proof um and to end
it wasn't successful it got something like 2% as as you mentioned we also looked
at a lot of the proofs that were generated and we looked very hard for for
similar examples in the on the internet and um we just didn't find any so that
is another indicator that the proofs that we were seeing were not just uh an
artifact of contamination now that said contamination could have played an
indirect role maybe there are similar kinds of problems that the llm has seen
before that we just couldn't find uh that's definitely a possibility but I feel
like at this point of history in AI research we just have to you know be very
aware Ware of this risk but still continue um using llms yes when I spoke with
sabar he said when he was um solving a planning problem in Blox world he made a
mystery bloxs World version where he just scrambled all of the tokens and
apparently that that did cause a significant deterioration in in performance but
it's it's it's so slippery isn't it it's very very difficult yeah yes yes on
standard benchmarks I think this is a big risk now I think that one could
imagine using synthetic benchmarks U now the approach that we took in the cpra
paper I just don't think it's welld designed for completely arbitrary synthetic
benchmarks because the whole point was that the prior knowledge inside the llm
helps with uh finding new tactics but uh there is this other paper that we
recently worked on uh which is uh it involves concept learning um using an llm
in the context of uh symbolic regression and there we also used an llm inside
this search framework it's this evolutionary search in this process in in that
case and uh I mentioned this paper earlier in our conversation you are actually
using the llm to do concept abstraction as well and you're using these abstract
Concepts to guide the search process now in that case we did experimentation
with with synthetic uh problems and we found that uh the llm does help there as
well and the reason is that even if you are not using any sort of prior
knowledge the obstruction ability of the llm that is to come up with you know
high level Concepts based on some some examples of text that is helpful um but
that's not a part of the cpra approach and so there is no reason to believe that
if you just come up with a completely synthetic problem uh Cor would be able to
do that well amazing and uh before we go where can people find out more about
you just Google my name and uh and then you'll get to my website and all of my
papers are are linked from there and um I also have a Twitter account uh just
swarat um but if you really want to discuss something uh technical just send me
a message um and I'd be happy to chat more amazing and we'll be putting the the
papers up on on the screen as you mentioned um SW this has been a brilliant
conversation thank you so much for joining us thank you so much for having me I
loved it as well [Music]
