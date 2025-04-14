# PinsaScript manual
A manual to learn PinsaScript.

## Table of contents
TBA

## 1: What is PinsaScript?
PinsaScript is a scripting language made to automatically manage files without having to do every operation manually.
It has a syntax which is heavely inspired from BASIC and Minecraft commands.
As a scripting language, it has a very small variety of instructions and is very easy to remember.
However, it is so reduced the only flow control it has is a very restrictive 'if' statement.
Also, it is not case-sensitive when it comes to instructions, but it is when it comes to attributes.

## 2: Making a 'Hello, World' program
PinsaScript offers two different ways of making a 'Hello, World' program.
### 2.1: With LOG instruction
The LOG instruction writes a message on the console. Making a 'Hello, World' with it is quite simple:
<pre>
log Hello, World
</pre>
And so, the output output will be:
<pre>
LOG: Hello, World
</pre>
### 2.2: With NOTICE instruction
The NOTICE instruction works similarly to the LOG instruction, except it requires the user to press the RETURN key
in order to continue running the script.
A 'Hello, World' with it looks like:
<pre>
notice Hello, World
</pre>
So, the output is:
<pre>
NOTICE: Hello, World
Press [RETURN] to continue...
</pre>

## 3: Commenting
In really large scripts, comments may come in handy to label different parts of your script.
Comments do just that, and are completely ignored during script execution.
A comment can be declared as such with the '#' character:
<pre>
# THIS is a comment.
</pre>
Howerver, because limitations of the language, you cannot put a comment after an instruction,
as the comment itself would be considered part of the instrucion.
Here's an example:
<pre>
# Do this,
log and not # this!
</pre>
OUTPUT:
<pre>
LOG: and not # this!
</pre>

## 4: TBA


{TO FINISH}
