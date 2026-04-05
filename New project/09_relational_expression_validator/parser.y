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

%token RELOP
%token <num> NUMBER
%token <id> ID

%left '+' '-'
%left '*' '/'

%%
input:
    relation   { printf("Valid relational expression\n"); }
;

relation:
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
    fprintf(stderr, "Invalid relational expression: %s\n", s);
}

int main(void) {
    printf("Brijesh Vishwakarma - 4SF24CS404\n");
    printf("Enter a relational expression:\n");
    yyparse();
    return 0;
}
