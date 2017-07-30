import app
import time
import os

def test(x, y, z):
    total_runtime = 0.0
    for test_num in range(0, 5):
        start_time = time.time()
        app.generate(x, y, z)
        total_runtime += time.time() - start_time
    print(str(x) + "x" + str(y) + "x" + str(z))
    print("     avg runtime: " + str(total_runtime / 5.0))

def main():
    start_time = time.time()
    test(0, 0, 0)
    test(1, 1, 1)
    test(5, 5, 5)
    test(20, 20, 1)
    test(10, 10, 10)
    test(50, 50, 1)
    test(20, 20, 20)


if __name__ == "__main__":
	main()
