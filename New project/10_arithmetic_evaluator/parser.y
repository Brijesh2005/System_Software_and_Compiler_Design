%{
#include <stdio.h>

int yylex(void);
void yyerror(const char *s);
%}

%union {
    int num;
}

%token <num> NUMBER
%type <num> expr term factor

%left '+' '-'
%left '*' '/'

%%
input:
    expr '\n'  { printf("Result = %d\n", $1); }
;

expr:
    expr '+' term   { $$ = $1 + $3; }
  | expr '-' term   { $$ = $1 - $3; }
  | term            { $$ = $1; }
;

term:
    term '*' factor { $$ = $1 * $3; }
  | term '/' factor
    {
        if ($3 == 0) {
            yyerror("division by zero");
            $$ = 0;
        } else {
            $$ = $1 / $3;
        }
    }
  | factor          { $$ = $1; }
;

factor:
    '(' expr ')'    { $$ = $2; }
  | NUMBER          { $$ = $1; }
;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Invalid arithmetic expression: %s\n", s);
}

int main(void) {
    printf("Brijesh Vishwakarma - 4SF24CS404\n");
    printf("Enter arithmetic expression: ");
    yyparse();
    return 0;
}
