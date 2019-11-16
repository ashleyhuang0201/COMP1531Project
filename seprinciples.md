In order to utilise good software engineering design, we have used a range of 
principles to eliminate design smells and follow the design principles.


#DRY
We have reduced repetition in our code by creating a single helper function file
that our other files import from. This allows us to reduce redundant functions
and makes changing these functions much more efficient in the future.

While converting input to the correct type it is necessary to handle exceptions
and change them from the default ValueError to our custom ValueError so that the
message can be displayed correctly on the frontend. Instead of using the 
standard python parsers (int() etc) we abstracted this as to_int() to allow it
for this exception handling once rather than checking each input individually

Removed nearly duplicate function "valid_u_id" which found a user and returned
either true or false and instead just use "get_user_by_u_id" and check whether
an actual user was returned or not. This function was also run 


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


Abstraction of our classes have been improved by removing references to a 
classes variables outside of that class, instead we have used "get" style 
methods to access these methods. For the most case this just means returning
the variable however this allows the function to be less rigid to change.