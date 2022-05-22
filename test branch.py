fin = 9
res = 14
den = int(round(fin/3))
final = [even_frame * den for even_frame in range(den)]
print(final)
fr_num = [even_frame + res for even_frame in final]
print(fr_num)