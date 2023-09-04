import numpy as np

arr = np.array([[1, 1, 1],
                [0, 1, 0],
                [1, 1, 1]])

# Xác định các hàng có toàn bộ các số bằng 1
all_ones_rows = np.all(arr == 1, axis=1)

# Đổi các hàng có toàn bộ các số bằng 1 thành -1
arr[all_ones_rows] = -1

print("Mảng sau khi đổi:")
print(arr)