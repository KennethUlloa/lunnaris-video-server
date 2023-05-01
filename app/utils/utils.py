from random import randint
def genToken(n):
    result           = ''
    characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    charactersLength = len(characters)
    for i in range(0, n):
        index = randint(0, charactersLength-1)
        result += characters[index]
    return result