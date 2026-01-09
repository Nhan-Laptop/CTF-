from sage.all import *

class RNG:

    def __init__(self, n = Integer(0), p = random_prime(2**512)):
        self.p = Integer(p)
        self.F = GF(self.p)
        self.H = QuaternionAlgebra(self.F, -1, -1)
        self.q_quat = self.H.random_element()
        self.n = n
        if self.n == Integer(0):
            self.seed()

    def seed(self):
        self.n = ZZ.random_element(self.p)
    
    def getrandbits(self, k):
        if k <= 0:
            return 0
        if k > 512:
            raise ValueError("k should be <= 512")
        val = self.gen()
        return int(val) & ((1 << k) - 1)
    
    def random_choice(self, choices):
        idx = self.getrandbits(32) % len(choices)
        return choices[idx]
    
    def randint(self, a, b):
        if a > b:
            raise ValueError("a should be <= b")
        range_size = b - a + 1
        rand_offset = self.getrandbits(32) % range_size
        return a + rand_offset
    
    def urandom(self, n):
        byte_array = bytearray()
        for _ in range(n):
            byte_array.append(self.getrandbits(8))
        return bytes(byte_array)
    
    def gen(self):
        val = (self.q_quat**self.n)[0]
        self.n += 1
        return int(val)


if __name__ == "__main__":
    rng = RNG()
    for _ in range(10):
        print(rng.getrandbits(32))
        print("----")
        print(rng.getrandbits(64))
        print("====")
        print(rng.getrandbits(128))
        print("****")
        print(rng.getrandbits(256))
        print("####")
        print(rng.getrandbits(512))
        print("$$$$")
