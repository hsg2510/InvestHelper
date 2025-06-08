import math
import timeit

loops = 250000
a = range(1, loops)


def f(x):
    return 3 * math.log(x) + math.cos(x) ** 2


# timeit 모듈 사용
result = timeit.timeit(lambda: [f(x) for x in a], number=1)
print(f"Execution time: {result:.6f} seconds")
