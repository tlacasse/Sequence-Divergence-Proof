


x = [200, 120, 175, 150, 300, 320, 240, 180, 210, 260]
y = [3.2, 2.0, 3.0, 2.0, 4.7, 5.5, 3.8, 2.8, 3.4, 4.5]

x_mean = sum(x) / len(x)
y_mean = sum(y) / len(y)

n = [(x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x))]
n = sum(n)

d = sum([(xi - x_mean)**2 for xi in x])

b1 = n / d
b0 = y_mean - (b1 * x_mean)

print(str(b0) + ' + x * ' + str(b1))

def test(z):
    return -0.2966283833702743 + (z * 0.01757136140775069)

for i in x:
    print(test(i))

print((1/len(x))*sum([(test(x[i]) - y[i])**2 for i in range(len(x))]))
