step = ord('Й') - ord('Д')

s = input()
news = ''
for symb in list(s):
    if not (1040 <= ord(symb) <= 1103):
        news += symb
        continue
    newSymb = chr(ord(symb) - step)
    if symb.islower(): newSymb = newSymb.lower()
    else: newSymb = newSymb.upper()
    news += newSymb
print(news)