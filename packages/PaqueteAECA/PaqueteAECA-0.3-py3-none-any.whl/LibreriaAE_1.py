def fib(n):
    a, b = 0,1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b


def PI_gregory_leibniz(n):
    s = 0
    for k in range(1, n + 1):
        s += (-1)**(k + 1) / (2 * k - 1)
    print(4 * s)


