# overunder
Overunder is an interpreted programming language in Python that receives as rules basic weaving instructions 'over' and 'under' and apply a pattern onto text, simulating a plain weave.

To start, add your text of choice in a file called `input.txt`.

To run:

```
$ overunder
```

Commands:

- `load` - loads the input text. Should be the first command you type inside the interpreter.
- `show` - shows which line you are currently working on
- `over + int(x)` - keeps the corresponding x characters intact
- `under + int(x)` - replaces the corresponding x characters with a symbol
- `pattern` - generates the pattern created so far
- `save` - saves the pattern in a text file
- `enter/return` - moves to the next line of text
- `quit` - quits the program

See more [here](https://pzwiki.wdka.nl/mediadesign/User:Alice/Special_Issue_V).
