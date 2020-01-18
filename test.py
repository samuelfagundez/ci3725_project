from lexer import lexer

# input del lexer
lexer.input("begin-world Place 5 of web in basket end-world")

# Evalua el lexer
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)