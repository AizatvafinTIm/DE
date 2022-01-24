from math import e as eps


class Method:
    def __init__(self, h, x0, y0, l, r):
        self.interval = []
        self.h = (float('{:.7f}'.format((r - l) / h)))
        self.x0 = x0
        self.y0 = y0
        self.l, self.r = l, r
        i = self.l
        self.const = (self.y0 + 1 + self.x0 ** 2) / (eps ** (self.x0 ** 2))

        while i <= self.r:
            self.interval.append(float(i))
            i += self.h
            i = float(i)
        self.exact_arr = self.count_exact()

    def exact_val(self, x):
        try:
            return float(

                self.const * eps ** (x ** 2) - x ** 2 - 1

            )

        except OverflowError:
            pass

    def y_prime(self, x, y):
        return float(2 * x * (x ** 2 + y))

    def count_exact(self):
        self.exact_arr = [0] * len(self.interval)
        self.exact_arr[0] = self.y0
        for i in range(1, len(self.interval)):
            self.exact_arr[i] = self.exact_val(self.interval[i])
        return self.exact_arr

    def get_interval(self):
        return self.interval
