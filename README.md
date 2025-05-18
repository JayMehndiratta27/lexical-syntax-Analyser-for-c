# C Code Analyzer (Tkinter GUI)
A desktop GUI application built using Python and Tkinter that allows users to input C language source code and analyze it through:

## Lexical Analysis – Breaks code into tokens like keywords, identifiers, operators, etc.

## Syntax Tree – Visualizes code structure such as functions, control structures, and blocks.

## Grammar Analysis – Validates grammar rules like function definitions, header inclusion, indentation, etc.

# Features
## Lexical Analysis
Identifies:

Keywords (int, return, if, etc.)

Identifiers (x, main)

Numbers and Strings

Operators and Punctuations

Comments and Preprocessors



# Grammar Checking
Validates C code for:

Presence of main() function

Header files

Balanced { and }

Variable declarations

Statement counts

Proper indentation (4 spaces)

# How It Works
User Input: Paste or write C code in the input field.

Click "Analyze":

The app processes the input code in 3 stages:

Lexical Tokenization

Syntax Tree Construction

Grammar Rule Checking

Results Display:

Lexical tokens shown in the Lexical Analysis tab

Code structure shown in Syntax Analysis tab

Rule validation in Grammar Analysis tab

