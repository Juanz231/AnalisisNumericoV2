from services.cap1.bisection_method import bisection_method

result = bisection_method(2, 14, 5e-5, 100, '2*(x-3)')

print(result)
