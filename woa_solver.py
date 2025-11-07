import numpy as np
import random
import problem as p

class WOA:
    """
    Whale Optimization Algorithm for Knapsack Problem
    """
    def __init__(self, n_whales=30, max_iter=100, dim=None):
        self.n_whales = n_whales
        self.max_iter = max_iter
        self.dim = len(p.weights) if dim is None else dim
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
            total_weight = sum([p.weights[i] * solution[i] for i in range(self.dim)])
            if total_weight <= p.capacity:
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
        fitness_list = [p.fitness(whale) for whale in population]
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
                pr = random.random()
                # Chuyển best_position sang continuous để tính toán
                best_continuous = continuous_pop[best_idx]
                
                if pr < 0.5:
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
            fitness_list = [p.fitness(whale) for whale in population]
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