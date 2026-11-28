#coding=utf-8
def isequation3(e1,e2):
# ====== answer-sheet-begin =======
    truth={True,False}
    t=True
    for P in truth:
        for Q in truth:
            for R in truth:
                f1=eval(e1)
                f2=eval(e2)
                t=(f1==f2) and t
    return t
# ======  answer-sheet-end  =======

e1 = '(not (P and Q)) or R'
e2 = '(not P) or ((not Q) or R)'
print(isequation3(e1,e2))
e1 = '(not P) or (Q or R)'
e2 = '(not (Q or R)) or P'
print(isequation3(e1,e2))