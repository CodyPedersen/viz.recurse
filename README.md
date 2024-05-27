### About viz.recurse
viz.recurse is a bare-bones library to easily visualize recursion without any significant overhead on the part of the user. This library utilizes common graph and visualization libraries (networkx, matplotlib, pygraphviz).

### Latest PyPi release [1.1.1]
Visit https://pypi.org/project/vizrecurse/1.1.1/

### Requirements
`Python 3.10.13`\
`pip 23.0.1` (graphviz compatibility)\
`brew install graphviz` (MacOS)\
`pip3 install -r requirements.txt`

If running into problems installing `pygraphviz`:
```
export GRAPHVIZ_DIR="$(brew --prefix graphviz)"
pip install pygraphviz \
  --config-settings=--global-option=build_ext \
  --config-settings=--global-option="-I$GRAPHVIZ_DIR/include" \
  --config-settings=--global-option="-L$GRAPHVIZ_DIR/lib"
```
### Usage
Attach `@visualize` decorator to the top of your recursive function and run as normal. e.g.
```
@visualize
def my_function(*args, **kwargs): ...
res = my_function(x=1,y=2)
draw()
```
### Examples
Visit the examples folder to run these for yourself. Each is runnable as a standalone script within the context.

![Towers of Hanoi](https://github.com/CodyPedersen/viz.recurse/blob/main/examples/images/toh.png?raw=true)
![Linear](https://github.com/CodyPedersen/viz.recurse/blob/main/examples/images/linear.png?raw=true)
![Fibonacci](https://github.com/CodyPedersen/viz.recurse/blob/main/examples/images/fib.png?raw=true)

### How it works (execution flow)

  ```
  @visualize
  def toh(args, kwargs): ...

  <__name__ = __main__ context> # <-- [snapshot_1] prev on call stack
  This calls visualize(func)  # no impact
  visualize(func) his returns inner(*args, **kwargs)
  inner(*args, **kwargs) is executed # <-- [snapshot_1] cur on call stack, [snapshot_2] prev on call stack
  this calls custom function toh()
  toh() calls visualize(func)
  this returns inner(*args, **kwargs)
  inner(*args, **kwargs) is executed # <-- [snapshot_2] cur on call stack
  ...
  ```


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