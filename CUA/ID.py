from Crypto.Util.number import * 
from sage.all import *
from hashlib import sha512


class ID: 
    def __init__(self,rng):
        self.N = rng.p
        R,(x) = PolynomialRing(Zmod(rng.p), 'x').objgen()
        self.rng = rng
        self.coeff = [self.rng.randint(0, self.N) for _ in range(10)]
        self.getPoly = self.f(x)
        self.x = x

    def f(self,x):
        y  = self.coeff[5] * x**4 + x**3 + x**6 + (x**2 + x + 1)**3 \
            + x**2 + x**7 + x
        z  = y * x**3 + x**4 * y + self.coeff[7] * y*x  + x**2 + x**3 
        a = self.coeff[0]*z + y +self.coeff[1]* x * y + x**3 + x**2
        b = a + x**5 + self.coeff[2]* (x**4 + x**3 + x**2 + x + 1)
        c = b + self.coeff[4] * a * b + a + x**7 + x**5 + x**3 + x * self.coeff[3]
        d = c + b * c + a * c + x**6 + self.coeff[9] * (x**4 + x**2 + 1)
        b = d + c + b + self.coeff[6] * a + x**8 + x**7 + x**5 + x**3 + x
        e = b + a * d + b * c + a * c + self.coeff[8] * x**9 + x**6 + x**4 + x**2 + 1
        return e
    
    def reset_ID(self):
        self.coeff = [self.rng.getrandbits(512) for _ in range(10)]
        self.getPoly = self.f(self.x)

    def getID(self, name):
        h = Integer(bytes_to_long(sha512(name.encode('utf-8', errors='ignore')).digest()))
        return Integer(self.getPoly(h)) % self.N
    
if __name__ == "__main__":
    from Ransom import RNG

    rng = RNG(p=0x10001)
    id_gen = ID(rng)

    names = ["alice", "bob", "charlie", "david", "eve"]
    for name in names:
        print(f"ID for {name}: {id_gen.getID(name)}")
    