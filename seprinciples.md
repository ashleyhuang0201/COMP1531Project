In order to utilise good software engineering design, we have used a range of 
principles to eliminate design smells and follow the design principles.

#DRY
We have reduced repetition in our code by creating a single helper function file
that our other files import from. This allows us to reduce redundant functions
and makes changing these functions much more efficient in the future.

#Decorators
Decorators allow us to add functionality to a function without altering the 
function itself. We decided to use decorators for testing a valid token
was given to the function as a parameter. This is because this valid token check
is repeated many times, by wrapping the functions we can eliminate the repetition
and make future changes to the valid token function easier. 

Rigidity of our code has been improved by replacing variables with constants
e.g. max name length of 20 characters. This allows for future potential changes
to be handled in a more efficient manner by changing the constant value, rather
than adjusting each value throughout the code. In addition, it also improves 
code readability and clarity with constant names that reflect the code's 
purpose, rather than just a number.

