# Sally

Interpreter for a toy programming language called "Sally."

## Getting Started

On Windows, just run 0runsally.bat. Or open a terminal and run

```
python sally_interpreter.py
```

This starts a REPL environment for Sally.

To run a specific script, use "python sally_interpreter.py my_file.sal"

### Prerequisites

Sally requires Python 2.7 (does not work with Python 3, yet). No additional libraries are required as Sally only uses the *sys* and *logging* libraries provided with Python.

### Installing

There is no installation, just create a directory and download the repository.

To see a demonstration of what Sally can do, run examples.sal using either

```
python sally_interpreter.py examples/examples.sal
```

or from within the REPL using the command

```
"examples/examples" run
```

Running the examples file loads some words into Sally's dictionary, but to actually see anything you'll need to run the words.

You can try:

```
5 fibonacci-display
```

To see a demonstration of the first five digits of the Fibonacci sequence. Or try:

```
27 36 gcd print
```

To see an implementation of Euclid's GCD algorithm.

A neat quasi-graphical demonstration produces the Sierpinski gasket fractal, provided you enter the correct dimensions for your console window:

```
25 80 sierpinski
```

## Contributing

Sally is just a toy project and there are no plans for further development at this time.

## Authors

* **James Durtka** - *Design and programming*

## Acknowledgments

* Sally borrows heavily from the Forth programming language, but is not exactly equivalent
* The interpreter design is an implementation of that described by Ruslan Spivak at https://ruslanspivak.com/lsbasi-part7/