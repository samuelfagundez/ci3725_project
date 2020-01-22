from lexer import lexer
import string


# input del lexer
lexer.input("{{begin-world Place--a 5 of web in basket of color Basket of capacity end-world true false}}\n Hola true")
# Evalua el lexer
while True:
    tok = lexer.token()
    if not tok:
        break

    # Si el lexer tiene bloques de comentario anidados, regresa un error
    if(tok.type == "BLOCKCOMMENT"):
        print("Error: Comentario anidado en " + str(tok.lineno) + ", " + str(tok.lexpos))
        continue

    print(tok)