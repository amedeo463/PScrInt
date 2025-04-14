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

## 4: Attributes
Attributes are strings that saved in memory that represent choices made by the user, and unlike instruction names,
attributes *ARE case sensitive*.
Attributes are used to run the contents of sections, which can be entered by possessing the right attributes.
There are plenty of instructions dedicated to gain attributes. They are: ATTRYN, ATTRSEL and ATTRMSEL.
### 4.1: Using ATTRYN
ATTRYN is an instruction that asks the user if it wants to gain a specific set of attributes,
where the user can decide to add this set of attributes by typing a Y,
or to not gain such set of attributes by typing a N.
The syntax of ATTRYN is the following:
<pre>ATTRYN attrA attrB</pre>
This instruction allows the user to choose if it wants to gain the attributes *attrA* and *attrB* or if it does not want to obtain them at all.
### 4.2: Using ATTRSEL
ATTRSEL is an instruction that allows the user to choose one from a set of attributes by typing the number corresponding to the attribute.
The syntax is the following:
<pre>ATTRSEL attrA attrB</pre>   
### 4.3: Using ATTRMSEL
ATTRMSEL works exactly like ATTRSEL, but allows the user to choose multiple attributes to add,
by typing the numbers corresponding to the attributes separated by a comma.
The syntax is the same as ATTRSEL:
<pre>ATTRMSEL attrA attrB attrC</pre>
For example, if we type
<pre>1, 3</pre>
In the input, then attrA and attrC will be gained.
## 5: Go back Action
If a non-valid input is given to ATTRSEL or ATTRMSEL, they will return a status code of -3, called "Go back Action with error".
This status code makes the interpreter go backward in the lines of the script as long as it keeps finding LOG instructions.
There is also a normal "Go back action" that returns no error, but it's currently unused by PScrInt.


{TO FINISH}
