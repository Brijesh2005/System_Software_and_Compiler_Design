%{
#include <stdio.h>
#include <stdlib.h>

int yylex(void);
void yyerror(const char *s);
%}

%union {
    int num;
    char *id;
}

%token IF ELSE RELOP ASSIGN
%token <num> NUMBER
%token <id> ID

%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%left '+' '-'
%left '*' '/'

%%
input:
    stmt   { printf("Valid if-else syntax\n"); }
;

stmt:
    IF '(' condition ')' stmt %prec LOWER_THAN_ELSE
  | IF '(' condition ')' stmt ELSE stmt
  | simple_stmt ';'
  | block
;

block:
    '{' stmt_list '}'
;

stmt_list:
    /* empty */
  | stmt_list stmt
;

simple_stmt:
    ID ASSIGN expr   { free($1); }
;

condition:
    expr RELOP expr
;

expr:
    expr '+' expr
  | expr '-' expr
  | expr '*' expr
  | expr '/' expr
  | '(' expr ')'
  | ID              { free($1); }
  | NUMBER
;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Invalid if-else syntax: %s\n", s);
}

int main(void) {
    printf("Brijesh Vishwakarma - 4SF24CS404\n");
    printf("Enter an if-else statement:\n");
    yyparse();
    return 0;
}
