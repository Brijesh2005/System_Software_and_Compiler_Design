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

%token FOR INC DEC RELOP ASSIGN
%token <num> NUMBER
%token <id> ID

%left '+' '-'
%left '*' '/'

%%
input:
    for_stmt   { printf("Valid for loop syntax\n"); }
;

for_stmt:
    FOR '(' opt_expr ';' opt_cond ';' opt_expr ')' body
;

opt_expr:
    /* empty */
  | assignment
  | update
  | expr
;

opt_cond:
    /* empty */
  | condition
;

assignment:
    ID ASSIGN expr    { free($1); }
;

update:
    ID INC            { free($1); }
  | ID DEC            { free($1); }
  | INC ID            { free($2); }
  | DEC ID            { free($2); }
  | assignment
;

condition:
    expr RELOP expr
;

body:
    statement ';'
  | block
;

statement:
  | update
;

block:
    '{' stmt_list '}'
;

stmt_list:
    /* empty */
  | stmt_list statement ';'
;

expr:
    expr '+' expr
  | expr '-' expr
  | expr '*' expr
  | expr '/' expr
  | '(' expr ')'
  | ID                { free($1); }
  | NUMBER
;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Invalid for loop syntax: %s\n", s);
}

int main(void) {
    printf("Brijesh Vishwakarma - 4SF24CS404\n");
    printf("Enter a for loop statement:\n");
    yyparse();
    return 0;
}
