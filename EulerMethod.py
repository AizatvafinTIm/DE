from method import Method


class EulerMethod(Method):

    def get_y_by_method(self, x_prev, y_prev):
        return y_prev + self.h * self.y_prime(x_prev, y_prev)

    def count_euler_arr(self):
        self.euler_arr = [0] * len(self.interval)
        self.euler_arr[0] = self.y0
        for i in range(1, len(self.interval)):
            self.euler_arr[i] = self.get_y_by_method(self.interval[i - 1], self.euler_arr[i - 1])
        return self.euler_arr

    def count_lte(self):
        self.lte_arr = [0] * len(self.interval)

        self.lte_arr[0] = 0

        for i in range(1, len(self.interval)):
            self.lte_arr[i] = float(abs(
                self.exact_arr[i] - self.get_y_by_method(self.interval[i - 1], self.exact_arr[i - 1])))
        return self.lte_arr

    def count_gte(self):
        self.gte_arr = [0] * len(self.interval)
        self.euler_arr = self.count_euler_arr()
        for i in range(len(self.interval)):
            self.gte_arr[i] = float(self.exact_arr[i] - self.euler_arr[i])
        return self.gte_arr
