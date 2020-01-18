from lexer import lexer

# input del lexer
lexer.input("repeat 20 times ponganTusa")

# Evalua el lexer
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)