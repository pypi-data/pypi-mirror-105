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
    l =[]
    for x in decrypted:
      l.append(x)
    if "₹" in l:
      return decrypted.replace("₹", "\n")
    else:
      return decryped
    
def ef(text, file):
  f = open(file, "w")
  f.write(en(text))
  f.close
  return True

def df(text, file):
  f = open(file, "r")
  k = f.read()
  x = de(k)
  f.close()
  return x