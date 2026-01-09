from Crypto.Util.number import * 
from sage.all import *
from hashlib import sha512


class ID: 
    def __init__(self,rng):
        self.N = rng.p
        R,(x) = PolynomialRing(Zmod(rng.p), 'x').objgen()
        self.rng = rng
        self.coeff = [self.rng.getrandbits(512) for _ in range(10)]
        self.getPoly = self.f(x)
        self.x = x

    def f(self, x):
        y  = self.coeff[5] * x**4 + x**3 + x**6 + (x**2 + x + 1)**3 \
            + x**2 + x**7 + x
        z  = y * x**3 + x**4 * y + self.coeff[7] * y*x  + x**2 + x**3 
        a = self.coeff[0] + z + y +self.coeff[1]* x * y + x**3 + x**2
        b =  x**5 + self.coeff[2]* (x**4 + x**3 + x**2 + x + 1)
        c =  self.coeff[4]  *   x**7 + x**5 + x**3 + x * self.coeff[3]
        d = c + b + a + x**6 + self.coeff[9] * (x**4 + x**2 + 1)
        b = d + c +  self.coeff[6] *  x**8 + x**7 + x**5 + x**3 + x
        e =  a +  c + self.coeff[8] * x**9 + x**6 + x**4 + x**2 + 1
        g = x**11 + x ** 44 + 25062006 * x**25 +  1234567 * x**19 + 7654321 * x**7
        h = x ** 36 + x**33 + x**29 + x**23 + x**19 + x**13 + x**7 + x**3
        i = x ** 55 + x**50 + x**45 + x**40 + x**35 + x**30 + x**25 + x**20 + x**15 + x**10 + x**5 + x
        return y + z + a + b + c + d + e + g * a + h + b + c + i 
    
    def reset_ID(self):
        self.coeff = [self.rng.getrandbits(512) for _ in range(10)]
        self.getPoly = self.f(self.x)

    def getID(self, name):
        h = Integer(bytes_to_long(sha512(name).digest()))
        return Integer(self.getPoly(h)) % self.N
    
if __name__ == "__main__":
    from Ransom import RNG

    rng = RNG(p=0x10001)
    id_gen = ID(rng)

    names = ["alice", "bob", "charlie", "david", "eve"]
    for name in names:
        print(f"ID for {name}: {id_gen.getID(name)}")
    