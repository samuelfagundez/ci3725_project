from lexer import lexer
import string


# input del lexer
lexer.input("{{begin-world Place--a 5 of web in basket\n of color Basket of capacity end-world true false}}\nHola true")
# Evalua el lexer
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)