# Nested MVC Code Architecture Command

For all code provided:

- Code will be sent in an artifact with a unique handle, then updated rather than rewritten unless explicitly requested

- Code will be sent one main controller function at a time (along with its nested components), in a unique artifact. These functions must have no placeholders or missing code, and ready to implement as written

- Do not provide code unless I explicitly ask for code. Assume I want to chat about the implementation plan, unless you receive a specific command to write code

- Code will always be written in Nested Model, View, Controller format:

## Nested MVC:

**Controller Nesting**: Main Controllers contain sub-controllers, that coordinate Model and View responsibilities

**Sub-task Nesting**: If a function is called only one time, it should be nested inside of its calling function. If a function needs to be called multiple times, it is not nested at all, but instead at the base level, in a group of "Shared Functions"

**Non-Controllers are "Terminal"**: Every model or view function must be terminal (does not call other functions- if you need to call other functions, coordinate that with another layer of subcontrollers)

**Semi-terminal Controllers are single layer**: every controller that calls a model function directly, should only call model functions, while every controller that calls a view function directly, should only call view functions.