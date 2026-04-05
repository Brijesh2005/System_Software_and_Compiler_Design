%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex(void);
void yyerror(const char *s);

enum {
    TYPE_INT = 1,
    TYPE_FLOAT = 2,
    TYPE_ERROR = -1
};

typedef struct {
    char name[64];
    int type;
} Symbol;

static Symbol table[100];
static int symbol_count = 0;

static void declare_symbol(const char *name, int type) {
    int i;
    for (i = 0; i < symbol_count; i++) {
        if (strcmp(table[i].name, name) == 0) {
            table[i].type = type;
            return;
        }
    }
    strcpy(table[symbol_count].name, name);
    table[symbol_count].type = type;
    symbol_count++;
}

static int get_symbol_type(const char *name) {
    int i;
    for (i = 0; i < symbol_count; i++) {
        if (strcmp(table[i].name, name) == 0) {
            return table[i].type;
        }
    }
    return TYPE_ERROR;
}

static int compatible(int lhs, int rhs) {
    if (lhs == TYPE_FLOAT && (rhs == TYPE_FLOAT || rhs == TYPE_INT)) {
        return 1;
    }
    if (lhs == TYPE_INT && rhs == TYPE_INT) {
        return 1;
    }
    return 0;
}

static int promote(int a, int b) {
    if (a == TYPE_ERROR || b == TYPE_ERROR) {
        return TYPE_ERROR;
    }
    if (a == TYPE_FLOAT || b == TYPE_FLOAT) {
        return TYPE_FLOAT;
    }
    return TYPE_INT;
}
%}

%union {
    int type;
    int ival;
    float fval;
    char *id;
}

%token INT FLOAT
%token <ival> IVAL
%token <fval> FVAL
%token <id> ID
%type <type> type_spec expr term factor

%left '+' '-'
%left '*' '/'

%%
input:
    /* empty */
  | input line
;

line:
    declaration '\n'
  | assignment '\n'
  | '\n'
;

declaration:
    type_spec ID ';'
    {
        declare_symbol($2, $1);
        printf("Declared %s as %s\n", $2, $1 == TYPE_INT ? "int" : "float");
        free($2);
    }
;

assignment:
    ID '=' expr ';'
    {
        int lhs = get_symbol_type($1);
        if (lhs == TYPE_ERROR) {
            fprintf(stderr, "Undeclared variable: %s\n", $1);
        } else if (!compatible(lhs, $3)) {
            fprintf(stderr, "Type error: cannot assign float value to int variable %s\n", $1);
        } else {
            printf("Type check success for %s\n", $1);
        }
        free($1);
    }
;

type_spec:
    INT      { $$ = TYPE_INT; }
  | FLOAT    { $$ = TYPE_FLOAT; }
;

expr:
    expr '+' term   { $$ = promote($1, $3); }
  | expr '-' term   { $$ = promote($1, $3); }
  | term            { $$ = $1; }
;

term:
    term '*' factor { $$ = promote($1, $3); }
  | term '/' factor { $$ = promote($1, $3); }
  | factor          { $$ = $1; }
;

factor:
    '(' expr ')'    { $$ = $2; }
  | IVAL            { $$ = TYPE_INT; }
  | FVAL            { $$ = TYPE_FLOAT; }
  | ID
    {
        $$ = get_symbol_type($1);
        if ($$ == TYPE_ERROR) {
            fprintf(stderr, "Undeclared variable: %s\n", $1);
        }
        free($1);
    }
;
%%

void yyerror(const char *s) {
    fprintf(stderr, "Syntax error: %s\n", s);
}

int main(void) {
    printf("Brijesh Vishwakarma - 4SF24CS404\n");
    printf("Enter declarations and assignments:\n");
    yyparse();
    return 0;
}
