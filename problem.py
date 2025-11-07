import csv

# Định nghĩa dữ liệu Knapsack
weights = [10, 20, 30, 40, 50]
values = [40, 100, 120, 150, 200]
capacity = 100

def fitness(solution):
    total_weight = sum(weights[i] * solution[i] for i in range(len(weights)))
    total_value = sum(values[i] * solution[i] for i in range(len(values)))
    if total_weight > capacity:
        return 0
    return total_value

# Lấy thông tin từ file 
def get_problem_info():
    info = f"Số lượng vật: {len(weights)}\n"
    info += f"Capacity: {capacity}\n"
    info += "Weights:\n" + str(weights[:10]) + ("..." if len(weights) > 10 else "") + "\n"
    info += "Values:\n" + str(values[:10]) + ("..." if len(values) > 10 else "")
    return info

def load_knapsack_from_csv(file_path):
    """
    Đọc dữ liệu Knapsack từ file CSV bằng thư viện csv
    Cột: Name, Value, Weight
    """
    weights_list = []
    values_list = []
    
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                weights_list.append(int(row['Weight']))
                values_list.append(int(row['Value']))
        
        total_weight = sum(weights_list)
        capacity = int(total_weight * 0.5)
        
        print(f"Đã load {len(weights_list)} items từ {file_path}")
        print(f"  - Tổng trọng lượng: {total_weight}")
        print(f"  - Capacity (50%): {capacity}")
        
        return weights_list, values_list, capacity
    
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        return [], [], 0
    except KeyError as e:
        print(f"Lỗi cột trong file CSV: {e}")
        return [], [], 0
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return [], [], 0