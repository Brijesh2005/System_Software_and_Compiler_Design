%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex(void);
void yyerror(const char *s);

static char *make_postfix(const char *left, const char *right, const char *op) {
    size_t len = strlen(left) + strlen(right) + strlen(op) + 3;
    char *result = (char *)malloc(len);
    snprintf(result, len, "%s %s %s", left, right, op);
    return result;
}
%}

%union {
    char *str;
}

%token <str> NUMBER ID
%type <str> expr term factor

%left '+' '-'
%left '*' '/'

%%
input:
    expr '\n'    { printf("Postfix: %s\n", $1); free($1); }
;

expr:
    expr '+' term   { $$ = make_postfix($1, $3, "+"); free($1); free($3); }
  | expr '-' term   { $$ = make_postfix($1, $3, "-"); free($1); free($3); }
  | term            { $$ = $1; }
;

term:
    term '*' factor { $$ = make_postfix($1, $3, "*"); free($1); free($3); }
  | term '/' factor { $$ = make_postfix($1, $3, "/"); free($1); free($3); }
  | factor          { $$ = $1; }
;

factor:
    '(' expr ')'    { $$ = $2; }
  | NUMBER          { $$ = $1; }
  | ID              { $$ = $1; }
;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Invalid expression: %s\n", s);
}

int main(void) {
    printf("Brijesh Vishwakarma - 4SF24CS404\n");
    printf("Enter infix expression: ");
    yyparse();
    return 0;
}
