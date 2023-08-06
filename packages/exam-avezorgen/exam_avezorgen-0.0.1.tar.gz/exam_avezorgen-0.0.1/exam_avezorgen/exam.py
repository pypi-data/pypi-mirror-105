def convert(num, from_base=10, to_base=10):
    n = int(num, from_base) if isinstance(num, str) else int(str(num), from_base)
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    res = ''
    while n > 0:
        n, m = divmod(n, to_base)
        res += alphabet[m]
    return res[::-1]


def convert_t():
    print("""def convert(num, from_base=10, to_base=10):
    n = int(num, from_base) if isinstance(num, str) else int(str(num), from_base)
    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    res = ''
    while n > 0:
        n, m = divmod(n, to_base)
        res += alphabet[m]
    return res[::-1]""")


def sieve(n):
    sieve = set(range(2, n + 1))
    prim = []
    while sieve:
        prime = min(sieve)
        prim.append(prime)
        sieve -= set(range(prime, n + 1, prime))
    return prim


def sieve_t():
    print("""def sieve(n):
    sieve = set(range(2, n + 1))
    prim = []
    while sieve:
        prime = min(sieve)
        prim.append(prime)
        sieve -= set(range(prime, n + 1, prime))
    return prim""")


def trace_t():
    print("""
    def f(x,y):
        if x>y or x==bad:
            return 0
        if x==y:
            return 1
        else:
            return f(x+1,y)+f(x+2,y)
    print(f(1,15)*f(15,25))""")

def e27_1_t():
    print("""
Рассматриваются всевозможные непустые подмножества,
состоящие из элементов последовательности. Необходимо найти количество подмножеств,
в которых сумма элементов кратна 12
s = [4, 5, 7, 12, 23]
n = len(s)
k = [0] * 12
for i in range(n):
    x = s[i]
    k1 = k.copy()
    for i in range(12):
        k1[(x + i) % 12] += k[i]
    k1[x % 12] += 1
    k = k1.copy()
print(k[0])
3
""")

def e27_2_t():
    print("""
max не дел на 3
d=3
md=[[1000]*3]*d
print(md)
su=0
sp=[[1, 3], [5, 12], [6, 9], [5, 4], [3, 3], [1, 1]]
for i in sp:
    a,b=i
    diff=abs(a-b)
    su+=max(i)
    md[diff%d]=sorted(md[diff%d]+[diff])[:3]
print(su,su%d,md,md[1:])
print(su-min(sum((md[1:]),[])))
32
""")

def bin_search_t():
    print("""
def bin_search(x, a):
    l = 0
    r = len(a) - 1
    m = (r + l) // 2
    while (r - l) > 1:
        m = (l + r) // 2
        if a[m] == x:
            return True
        elif a[m] < x:
            l = m
        elif a[m] > x:
            r = m
    if a[r] == x or a[m] == x or a[l] == x:
        return True
    return False
""")

def h():
    print("""convert(num, from_base=10, to_base=10),sieve(n),
convert_t,sieve_t,trace_t,e27_1_t,e27_2_t,bin_search_t""")
