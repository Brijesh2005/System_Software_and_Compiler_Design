# Lex and Yacc Programs

This repository contains 10 standalone Lex/Yacc lab programs.

## Folder Layout

- `01_infix_to_postfix`
- `02_boolean_evaluator`
- `03_calculator_with_variables`
- `04_for_loop_validator`
- `05_balanced_parentheses`
- `06_variable_declaration_validator`
- `07_if_else_validator`
- `08_simple_type_checker`
- `09_relational_expression_validator`
- `10_arithmetic_evaluator`

## Build

On Linux/macOS with Flex/Bison:

```sh
cd 01_infix_to_postfix
bison -d parser.y
flex lexer.l
gcc lex.yy.c parser.tab.c -o program
./program
```

On Windows with win_bison/win_flex:

```powershell
cd 01_infix_to_postfix
win_bison -d parser.y
win_flex lexer.l
gcc lex.yy.c parser.tab.c -o program.exe
.\program.exe
```

Repeat the same steps inside any exercise folder.

## Notes

- Each program reads from standard input.
- Most programs expect a single line or a small set of lines, then print the result.
- If you use `gcc`, make sure Flex/Bison generated files are in the same folder.
# System Software and Compiler Design
