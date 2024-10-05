# Python Static Code Analyser

## Python code pattern and why - 
When there's a return statement in an if part of an if-else block, then the else part becomes redundant because the if will make the control flow to exit automatically. This code pattern is important for static analysis because unnecessary else makes the code look unreadable and also adds up unnecessary nesting making it harder to follow. It also makes refactoring or reviewing large codebases difficult. Consider the example below - 

Bad Practice -
```bash
  def is_greater(a,b):
    if a > b:
      return "greater"
    else:
      return "lesser"
```

Good Practice - 
```bash
  def is_greater(a,b):
    if a > b:
      return "greater"
    return "lesser"
```

## Run the script by following the below steps - 
```bash
python3 -m unittest analyser.py
```

## Extending this tool in future
We can add multiple python code patterns and antipatterns in the static analyser tool in the future. Some the ones are as listed below:-
1. We shouldn't have wildcard imports in our code since it makes it harder to decipher which variables or functions are being imported into the current namespace.
2. List comprehensions should only be used for forming simple iterables.
3. We shouldn't compare to True or False, write the expression as is instead since it will evaluate to a boolean value implicitly anyway.
4. We shouldn't return True or False explicitly after checking a boolean expression, directly return the boolean expression instead.

## Unit Testing screenshot -
<img width="609" alt="Screenshot 2024-10-05 at 10 43 24 AM" src="https://github.com/user-attachments/assets/05d21482-b29d-4977-84bb-dff0b6ab0157">

