import numpy as np

# Định nghĩa dữ liệu Knapsack
weights = [10, 20, 30, 40, 50]
values = [60, 100, 120, 150, 200]
capacity = 100

def fitness(solution):
    total_weight = np.sum(np.array(weights) * np.array(solution))
    total_value = np.sum(np.array(values) * np.array(solution))
    if total_weight > capacity:
        return 0  # vượt quá sức chứa → nghiệm không hợp lệ
    return total_value

if __name__ == "__main__":
    # ví dụ test
    s = [1, 0, 1, 0, 1]  # chọn vật 1, 3, 5
    print("Fitness:", fitness(s))
