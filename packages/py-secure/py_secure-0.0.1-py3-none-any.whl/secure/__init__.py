class top():
    _alphabet = r"abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890`~!@#$%^&*()_+-=,./;'[]<>?:\"{}|₹"

def en(Text):
    encrypted = ''
    for i in Text :
        encrypted += top._alphabet[int((top._alphabet.find(i) + len(Text)) % len(top._alphabet))]
    return encrypted

def de(Text):
    decrypted = ''
    for i in Text :
        decrypted +=top._alphabet[int((top._alphabet.find(i) - len(Text)) % len(top._alphabet))]
    return decrypted
    
