from method import Method


class RungeKutta(Method):
    def get_y_by_method(self, x_prev, y_prev):
        k1 = self.y_prime(x_prev, y_prev)
        k2 = self.y_prime(x_prev + (self.h) / 2, y_prev + (self.h * k1) / 2)
        k3 = self.y_prime(x_prev + (self.h) / 2, y_prev + (self.h * k2) / 2)
        k4 = self.y_prime(x_prev + self.h, y_prev + self.h * k3)
        return y_prev + self.h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    def count_rungekutta(self):
        self.runge = [0] * len(self.interval)
        self.runge[0] = self.y0
        for i in range(1, len(self.interval)):
            self.runge[i] = self.get_y_by_method(self.interval[i - 1], self.runge[i - 1])
        return self.runge

    def count_gte(self):
        self.gte_arr = [0] * (len(self.interval))
        self.runge = self.count_rungekutta()
        for i in range(len(self.interval)):
            self.gte_arr[i] = float(self.exact_arr[i] - self.runge[i])
        return self.gte_arr

    def count_lte(self):
        self.lte_arr = [0] * len(self.interval)
        self.lte_arr[0] = 0
        for i in range(1, len(self.interval)):
            self.lte_arr[i] = float(
                abs(self.exact_arr[i] - self.get_y_by_method(self.interval[i - 1], self.exact_arr[i - 1])))
        return self.lte_arr
