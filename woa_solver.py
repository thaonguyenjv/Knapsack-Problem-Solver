import numpy as np
import random
from problem import fitness, weights, values, capacity

class WOA:
    """
    Whale Optimization Algorithm for Knapsack Problem
    """
    def __init__(self, n_whales=30, max_iter=100, dim=5):
        self.n_whales = n_whales
        self.max_iter = max_iter
        self.dim = dim
        self.best_position = None
        self.best_fitness = 0
        self.history = []
        
    def initialize_population(self):
        """Khởi tạo quần thể cá voi ngẫu nhiên"""
        population = []
        for _ in range(self.n_whales):
            whale = [random.randint(0, 1) for _ in range(self.dim)]
            population.append(whale)
        return population
    
    def binary_conversion(self, continuous_pos):
        """Chuyển đổi vị trí liên tục sang nhị phân (0 hoặc 1)"""
        binary_pos = []
        for val in continuous_pos:
            # Sử dụng sigmoid để chuyển về xác suất
            sigmoid_val = 1 / (1 + np.exp(-val))
            # Chuyển thành 0 hoặc 1
            binary_pos.append(1 if random.random() < sigmoid_val else 0)
        return binary_pos
    
    def repair_solution(self, solution):
        """Sửa nghiệm nếu vượt quá capacity"""
        while True:
            total_weight = sum([weights[i] * solution[i] for i in range(self.dim)])
            if total_weight <= capacity:
                break
            # Loại bỏ ngẫu nhiên một vật đã chọn
            selected_items = [i for i in range(self.dim) if solution[i] == 1]
            if not selected_items:
                break
            remove_idx = random.choice(selected_items)
            solution[remove_idx] = 0
        return solution
    
    def optimize(self):
        """Thuật toán WOA chính"""
        # Khởi tạo quần thể
        population = self.initialize_population()
        continuous_pop = [[random.uniform(-2, 2) for _ in range(self.dim)] 
                          for _ in range(self.n_whales)]
        
        # Tìm cá voi tốt nhất ban đầu
        fitness_list = [fitness(whale) for whale in population]
        best_idx = np.argmax(fitness_list)
        self.best_position = population[best_idx].copy()
        self.best_fitness = fitness_list[best_idx]
        self.history.append(self.best_fitness)
        
        # Vòng lặp chính
        for iteration in range(self.max_iter):
            a = 2 - iteration * (2.0 / self.max_iter)  # a giảm tuyến tính từ 2 về 0
            a2 = -1 + iteration * (-1.0 / self.max_iter)  # a2 giảm tuyến tính từ -1 về -2
            
            for i in range(self.n_whales):
                r1 = random.random()
                r2 = random.random()
                
                A = 2 * a * r1 - a
                C = 2 * r2
                
                b = 1  # hằng số cho spiral
                l = random.uniform(-1, 1)
                
                p = random.random()
                
                # Chuyển best_position sang continuous để tính toán
                best_continuous = continuous_pop[best_idx]
                
                if p < 0.5:
                    if abs(A) < 1:
                        # Encircling prey (bao vây con mồi)
                        D = [abs(C * best_continuous[j] - continuous_pop[i][j]) 
                             for j in range(self.dim)]
                        continuous_pop[i] = [best_continuous[j] - A * D[j] 
                                            for j in range(self.dim)]
                    else:
                        # Search for prey (tìm kiếm ngẫu nhiên)
                        rand_whale_idx = random.randint(0, self.n_whales - 1)
                        rand_whale = continuous_pop[rand_whale_idx]
                        D = [abs(C * rand_whale[j] - continuous_pop[i][j]) 
                             for j in range(self.dim)]
                        continuous_pop[i] = [rand_whale[j] - A * D[j] 
                                            for j in range(self.dim)]
                else:
                    # Spiral updating position (cập nhật theo hình xoắn ốc)
                    D_prime = [abs(best_continuous[j] - continuous_pop[i][j]) 
                              for j in range(self.dim)]
                    continuous_pop[i] = [D_prime[j] * np.exp(b * l) * np.cos(2 * np.pi * l) + 
                                        best_continuous[j] for j in range(self.dim)]
                
                # Chuyển đổi sang nhị phân và sửa nghiệm
                population[i] = self.binary_conversion(continuous_pop[i])
                population[i] = self.repair_solution(population[i])
            
            # Cập nhật best solution
            fitness_list = [fitness(whale) for whale in population]
            current_best_idx = np.argmax(fitness_list)
            current_best_fitness = fitness_list[current_best_idx]
            
            if current_best_fitness > self.best_fitness:
                self.best_fitness = current_best_fitness
                self.best_position = population[current_best_idx].copy()
                best_idx = current_best_idx
            
            self.history.append(self.best_fitness)
            
            # In tiến trình
            if (iteration + 1) % 10 == 0:
                print(f"Iteration {iteration + 1}/{self.max_iter}, Best Fitness: {self.best_fitness}")
        
        return self.best_position, self.best_fitness, self.history

def solve_knapsack_woa(n_whales=30, max_iter=100):
    """
    Hàm tiện ích để giải bài toán knapsack bằng WOA
    """
    woa = WOA(n_whales=n_whales, max_iter=max_iter, dim=len(weights))
    best_solution, best_value, history = woa.optimize()
    
    # Tính toán chi tiết
    total_weight = sum([weights[i] * best_solution[i] for i in range(len(weights))])
    selected_items = [i+1 for i in range(len(weights)) if best_solution[i] == 1]
    
    print("\n" + "="*50)
    print("KẾT QUẢ WHALE OPTIMIZATION ALGORITHM")
    print("="*50)
    print(f"Nghiệm tốt nhất: {best_solution}")
    print(f"Các vật được chọn: {selected_items}")
    print(f"Tổng giá trị: {best_value}")
    print(f"Tổng trọng lượng: {total_weight}/{capacity}")
    print("="*50)
    
    return best_solution, best_value, history

if __name__ == "__main__":
    # Test thuật toán
    print("Dữ liệu bài toán:")
    print(f"Weights: {weights}")
    print(f"Values: {values}")
    print(f"Capacity: {capacity}")
    print("\nBắt đầu tối ưu hóa...\n")
    
    best_solution, best_value, history = solve_knapsack_woa(n_whales=30, max_iter=100)
    
    # Vẽ biểu đồ hội tụ
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.plot(history, linewidth=2, color='blue')
        plt.title('WOA Convergence Curve', fontsize=14, fontweight='bold')
        plt.xlabel('Iteration', fontsize=12)
        plt.ylabel('Best Fitness Value', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('woa_convergence.png')  # Lưu ảnh thay vì show
        print("\nBiểu đồ đã được lưu: woa_convergence.png")
        # plt.show()  # Comment để không block terminal
    except Exception as e:
        print(f"Không thể vẽ biểu đồ: {e}")