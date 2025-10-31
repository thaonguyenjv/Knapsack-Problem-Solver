import numpy as np

# Định nghĩa dữ liệu Knapsack
weights = [10, 20, 30, 40, 50]
values = [40, 100, 120, 150, 200]
capacity = 100

def fitness(solution):
    total_weight = np.sum(np.array(weights) * np.array(solution))
    total_value = np.sum(np.array(values) * np.array(solution))
    if total_weight > capacity:
        return 0  # vượt quá sức chứa → nghiệm không hợp lệ
    return total_value
# Lấy thông tin từ file 
def get_problem_info():
    info = f"Số lượng vật: {len(weights)}\n"
    info += f"Capacity: {capacity}\n"
    info += "Weights:\n" + str(weights[:10]) + ("..." if len(weights) > 10 else "") + "\n"
    info += "Values:\n" + str(values[:10]) + ("..." if len(values) > 10 else "")
    return info
