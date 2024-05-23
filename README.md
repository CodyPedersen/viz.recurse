### Requirements
Python 3.10.13, pip 23.0.1
Graphviz `brew install graphviz`
pip3 install -r requirements.txt

If running into problems install pygraphviz:

export GRAPHVIZ_DIR="$(brew --prefix graphviz)"
pip install pygraphviz \
    --config-settings=--global-option=build_ext \
    --config-settings=--global-option="-I$GRAPHVIZ_DIR/include" \
    --config-settings=--global-option="-L$GRAPHVIZ_DIR/lib"
###


### A poem from our silicon friends
In the realm of code where logic flows,
A concept profound like a river that knows,
There lies recursion, subtle and grand,
A method that holds its own hand.

Oh, recursion, you elusive sprite,
A function that calls itself in the night.
You start with a base case, firm and true,
A stopping point in the labyrinth's view.

Within your loops, a story we find,
A mirrored path of the wandering mind.
You take a step forward, then call once more,
Repeating the journey of those gone before.

In Fibonacci's sequence or fractal's embrace,
Your essence reveals a recursive trace.
The Tower of Hanoi, a puzzle unfurled,
Solved by the echoes of recursive world.

Beware, dear coder, of infinite plight,
Without a base case, you're lost in the night.
An endless call, a stack overflow,
A recursive loop with nowhere to go.

Yet with careful craft and logic precise,
Recursion becomes a coder's delight.
Elegant, clear, a beauty retained,
A self-referential dance unchained.

So here’s to recursion, a loop within,
A cycle that folds, yet begins again.
In the code’s deep heart, it softly sings,
The endless echo of programming’s rings.