from lexer import lexer

# input del lexer
lexer.input("begin-world Place 5 of web in basket of color Basket of capacity end-world true false")

# Evalua el lexer
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)