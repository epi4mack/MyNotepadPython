def encrypt(text, keyP, keyK):
    keyO = keyP * keyK
    result = ''
    for symbol in text:
        K = ord(symbol)
        K ^= keyO
        Cc = chr(K)
        result += Cc
    return result