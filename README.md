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
First you must install Talon.
```bash
pip install talonlang
```
Then you can run Talon programs:
```bash
tal [-c] <input.tal[c]> [-o <output.talc>]
```
- The `-c` switches on compiling. If no `-o` flag is provided (along with a filename), the output file will be named according to the input file. Eg. `input.tal` to `input.talc`. (Note: you may compile already compiled code, but that is redundant and pointless.)
- The `-o` flag changes the name of the output file. It can only be used if `-c` is present.
- If the `-c` flag is not included, the interpreter will either
  - compile and run the provided code if the file ends in `.tal`,
  - or interpret the compiled code if the file extension is `.talc`.

## Basic Syntax
A basic rundown of Talon's syntax.

### Comments

Single line:
```
// I'm a comment
print('Hello') // Another comment
```

Multi-line:
```
/*
  This is a multi-line comment.
  It can cover multiple lines.
*/
```

### Variables
Variables are initialized with the `this` keyword:
```
this foo = bar
```
Like in JavaScript, values are *not* required when first initializing a variable:
```
this x
```
However, re-initializing a variable results in an error:
```
this name = 'Talon'
this name // ERROR
```
Assignment can be accomplished via a variety of operators:
```
this n
n = 1
n += 2    // n = n + 2
n -= 5    // n = n - 5
n *= 7    // n = n * 7
n /= 1.5  // n = n / 1.5
n %= 3    // n = n % 3
n ^= 20   // n = n ^ 20
```

### Values
- Numbers
  - Integer: `42`, `1`, `-67`
  - Float: `3.1415`, `98.6`, `-1.168`
- Strings
  - Single-quoted: `'Hello!'`
  - Double-quoted: `"Good day!"`
- Booleans
  - Truthy: `true`, `on`, `yes`
  - Falsey: `false`, `off`, `no`
- Lists
  - Creating
    - Single dimensional: `[1, 2, 3, 4]`
    - Multi-dimensional: `[[1, 2], [3, 4]]`
  - Accessing: `list[index]`, `list[index][index2]`
  - Slicing: `list[:-1]`, `list[1:]`, `list[2:-2]`
- Ranges
  - Inclusive: `1 to 10`
  - Exclusive: `1 upto 11`

### Operators
- Binary
  - Addition: `a + b`
  - Subtraction: `a - b`
  - Multiplication: `a * b`
  - Division: `a / b`
  - Modulus: `a % b`
  - Exponent: `a ^ b`
- Unary
  - Negation: `-x`
  - Absolute value: `+x`
  - Not: `!x`
- Comparing
  - Equals: `a == b`
  - Not equals: `a != b`
  - Less than: `a < b`
  - Greater than: `a > b`
  - Less than or equal to: `a <= b`
  - Greater than or equal to: `a >= b`
- Boolean
  - And: `a && b`
  - Or: `a || b`

### Conditional Statements
```
if (/* condition */) {
  ...
} else if (/* condition */) {
  ...
} else {
  ...
}
```

### Loops
While loop:
```
this i = 0

while (i < 10) {
  print(i)
  i += 1
}
```
For loop:
```
this i

for (i in 1 to 10) {
  print(i)
}
```
```
this alphabet = 'abcdefghijklmnopqrstuvwxyz'
this letter

for (letter in alphabet) {
  printf('The letter is %0.', [letter])
}
```

### Functions
Functions can be created by a variety of methods:
```
fun foo(bar) {
  ret bar * 2
}
```
```
this foo = fun (bar) {
  ret bar * 2
}
```
```
this foo = (bar) -> {
  ret bar * 2
}
```
```
this foo = (bar) -> (bar * 2)
```
They have their own scope:
```
fun scope() {
  this x = 2
  x = 5
  y = 6
}

this x = 1
this y = 1

scope()

print(x, y) // 1, 6
```

### Imports
Currently very limited, importing allows you to import functions and variables from other Talon scripts.

```
// a.tal

import('b.tal')

print(add(1, 2)) // 3
```
```
// b.tal

fun add(a, b) {
  ret a + b
}
```

> Hopefully namespaces (which aren't yet supported) will be implemented in the future.
> ```
> import('b.tal', 'b')
>
> print(b.add(1, 2))
> ```