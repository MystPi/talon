# The Talon Programming Language

Talon is a toy programming language with Python and JavaScript flavors.

```talon
fun factorial(n) {
  if (n == 1) {
    ret 1
  } else {
    ret n * factorial(n - 1)
  }
}

this f = factorial(4)

print(f) // -> 24
```

```talon
this name = getstr('What is your name? ')
this length = len(name)

printf('Your name is %0; it has %1 characters.', [name, length])
```
> You can view more demos in the [examples](examples/) folder.

## Running and Compiling Code
Talon is not yet on PyPi, so to run/compile Talon code, you must directly execute a Python script.

```bash
python talon.py [-c] <input.tal[c]> [-o <output.talc>]
```
- The `-c` switches on compiling. If no `-o` flag is provided (along with a filename), the output file will be named according to the input file. Eg. `input.tal` to `input.talc`. (Note: you may compile already compiled code, but that is redundant and pointless.)
- The `-o` flag changes the name of the output file. It can only be used if `-c` is present.
- If the `-c` flag is not included, the interpreter will either
  - compile and run the provided code if the file ends in `.tal`,
  - or interpret the compiled code if the file extension is `.talc`.

## Documentation
Docs possibly coming soon.