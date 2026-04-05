%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex(void);
void yyerror(const char *s);

typedef struct {
    char name[64];
    int value;
} Symbol;

static Symbol table[100];
static int symbol_count = 0;

static int lookup(const char *name, int *found) {
    int i;
    for (i = 0; i < symbol_count; i++) {
        if (strcmp(table[i].name, name) == 0) {
            *found = 1;
            return table[i].value;
        }
    }
    *found = 0;
    return 0;
}

static void assign_value(const char *name, int value) {
    int i;
    for (i = 0; i < symbol_count; i++) {
        if (strcmp(table[i].name, name) == 0) {
            table[i].value = value;
            return;
        }
    }

    strcpy(table[symbol_count].name, name);
    table[symbol_count].value = value;
    symbol_count++;
}
%}

%union {
    int num;
    char *id;
}

%token <num> NUMBER
%token <id> ID
%type <num> expr term factor

%left '+' '-'
%left '*' '/'

%%
input:
    /* empty */
  | input line
;

line:
    ID '=' expr '\n'
    {
        assign_value($1, $3);
        printf("%s = %d\n", $1, $3);
        free($1);
    }
  | expr '\n'
    {
        printf("Result = %d\n", $1);
    }
  | '\n'
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
  | ID
    {
        int found;
        $$ = lookup($1, &found);
        if (!found) {
            fprintf(stderr, "Undefined variable: %s\n", $1);
            $$ = 0;
        }
        free($1);
    }
;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    printf("Brijesh Vishwakarma - 4SF24CS404\n");
    printf("Enter assignments or expressions (Ctrl+D/Ctrl+Z to stop):\n");
    yyparse();
    return 0;
}
