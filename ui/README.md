# `ui`

This is a folder for all code that controls user interaction, including interpreting inputs and any output creation

## Files

This folder includes:
 - `annotate.py`: A checklist annotator; it creates a copy of a student's checklist, and annotates the copy with the validity determined by the checks
 - `logger.py`: The setup and distribution of `logging.Logger` modules, provided to checks to abstract away the details of printing based on verbosity and writing to files
 - `parser.py`: A parser for user inputs, as to ensure all of our data (such as class names, terms, grades, etc.) conform to the same format
 - `user.py`: The main user-facing code, responsible for prompting the user for input when necessary and abstracting away response validation

 ## Verbosity

The loggers created in `logger.py` can be modified based on the provided verbosity. By default, the verbosity is off, and information from the checks is not displayed.
However, for debugging, it may be useful to directly display this information; users can turn this on by invoking the `-v` flag. Regardless, the loggers additionally store
all data to a file in a logs directory (default is `logs`, but can be modified with the `-l` flag), organized by check name, then by NetID (ex. `logs/common-core/ec1.log`)