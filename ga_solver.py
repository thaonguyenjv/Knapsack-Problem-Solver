import random

def calculate_fitness(solution, weights, values, capacity):
    """
    Tính fitness của một nghiệm (chromosome)
    
    Args:
        solution: list nhị phân [0,1,0,1,...] 
        weights: list trọng lượng items
        values: list giá trị items
        capacity: sức chứa tối đa
    
    Returns:
        fitness value (nếu vượt capacity thì trả về 0)
    """
    total_weight = sum(solution[i] * weights[i] for i in range(len(solution)))
    total_value = sum(solution[i] * values[i] for i in range(len(solution)))
    
    # Nếu vượt trọng lượng → fitness = 0 (nghiệm không hợp lệ)
    if total_weight > capacity:
        return 0
    
    return total_value


def initialize_population(pop_size, num_items):
    """
    Khởi tạo quần thể ngẫu nhiên
    
    Args:
        pop_size: số lượng cá thể
        num_items: số lượng items
    
    Returns:
        population: list các chromosome (mỗi chromosome là list nhị phân)
    """
    population = []
    for _ in range(pop_size):
        chromosome = [random.randint(0, 1) for _ in range(num_items)]
        population.append(chromosome)
    return population


def selection_tournament(population, fitnesses, tournament_size=3):
    """
    Chọn lọc bằng Tournament Selection
    
    Args:
        population: quần thể hiện tại
        fitnesses: fitness của từng cá thể
        tournament_size: số cá thể tham gia tournament
    
    Returns:
        selected chromosome
    """
    # Chọn ngẫu nhiên tournament_size cá thể
    tournament_indices = random.sample(range(len(population)), tournament_size)
    
    # Tìm cá thể tốt nhất trong tournament
    best_idx = tournament_indices[0]
    best_fitness = fitnesses[tournament_indices[0]]
    
    for idx in tournament_indices[1:]:
        if fitnesses[idx] > best_fitness:
            best_fitness = fitnesses[idx]
            best_idx = idx
    
    return population[best_idx][:]  # Return copy


def crossover_one_point(parent1, parent2, crossover_rate):
    """
    Lai ghép một điểm cắt (One-point Crossover)
    
    Args:
        parent1, parent2: hai cá thể cha mẹ
        crossover_rate: xác suất lai ghép
    
    Returns:
        child1, child2: hai cá thể con
    """
    # Kiểm tra xem có thực hiện crossover không
    if random.random() > crossover_rate:
        return parent1[:], parent2[:]
    
    # Chọn điểm cắt ngẫu nhiên
    point = random.randint(1, len(parent1) - 1)
    
    # Tạo con bằng cách hoán đổi đoạn sau điểm cắt
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    
    return child1, child2


def mutate(chromosome, mutation_rate):
    """
    Đột biến gen (Bit Flip Mutation)
    
    Args:
        chromosome: cá thể cần đột biến
        mutation_rate: xác suất đột biến mỗi gen
    
    Returns:
        mutated chromosome
    """
    mutated = chromosome[:]
    
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            # Flip bit: 0 -> 1 hoặc 1 -> 0
            mutated[i] = 1 - mutated[i]
    
    return mutated


def solve_ga(weights, values, capacity, pop_size=50, generations=100, 
             crossover_rate=0.8, mutation_rate=0.01):
    """
    Giải bài toán Knapsack bằng Genetic Algorithm
    
    Args:
        weights: list trọng lượng items
        values: list giá trị items
        capacity: sức chứa tối đa
        pop_size: kích thước quần thể
        generations: số thế hệ
        crossover_rate: tỉ lệ lai ghép
        mutation_rate: tỉ lệ đột biến
    
    Returns:
        best_solution: nghiệm tốt nhất (list nhị phân)
        best_value: giá trị fitness tốt nhất
        history: lịch sử fitness qua các thế hệ (để vẽ biểu đồ)
    """
    num_items = len(weights)
    
    # Khởi tạo quần thể
    population = initialize_population(pop_size, num_items)
    
    # Lưu lịch sử để vẽ biểu đồ hội tụ
    history = []
    
    # Lưu nghiệm tốt nhất
    best_solution = None
    best_value = 0
    
    # Chạy qua các thế hệ
    for generation in range(generations):
        # Tính fitness cho toàn bộ quần thể
        fitnesses = []
        for chromosome in population:
            fitness = calculate_fitness(chromosome, weights, values, capacity)
            fitnesses.append(fitness)
        
        # Tìm nghiệm tốt nhất thế hệ này
        max_fitness = max(fitnesses)
        max_idx = fitnesses.index(max_fitness)
        
        # Cập nhật nghiệm tốt nhất toàn cục
        if max_fitness > best_value:
            best_value = max_fitness
            best_solution = population[max_idx][:]
        
        # Lưu lịch sử
        history.append(best_value)
        
        # Tạo quần thể mới
        new_population = []
        
        # Elitism: giữ lại 2 cá thể tốt nhất
        sorted_indices = sorted(range(len(fitnesses)), 
                               key=lambda i: fitnesses[i], 
                               reverse=True)
        new_population.append(population[sorted_indices[0]][:])
        new_population.append(population[sorted_indices[1]][:])
        
        # Tạo các cá thể mới cho đến khi đủ quần thể
        while len(new_population) < pop_size:
            # Chọn lọc
            parent1 = selection_tournament(population, fitnesses)
            parent2 = selection_tournament(population, fitnesses)
            
            # Lai ghép
            child1, child2 = crossover_one_point(parent1, parent2, crossover_rate)
            
            # Đột biến
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            
            # Thêm vào quần thể mới
            new_population.append(child1)
            if len(new_population) < pop_size:
                new_population.append(child2)
        
        # Cập nhật quần thể
        population = new_population
    
    return best_solution, best_value, history


# Test function
def test_ga():
    """Test GA với dữ liệu mẫu"""
    print("=" * 60)
    print("TEST GENETIC ALGORITHM - KNAPSACK PROBLEM")
    print("=" * 60)
    
    # Dữ liệu test
    weights = [2, 3, 4, 5, 9]
    values = [3, 4, 8, 8, 10]
    capacity = 20
    
    print(f"\nDữ liệu test:")
    print(f"Weights: {weights}")
    print(f"Values:  {values}")
    print(f"Capacity: {capacity}")
    
    # Chạy GA
    print(f"\nChạy GA với:")
    print(f"- Population size: 30")
    print(f"- Generations: 50")
    print(f"- Crossover rate: 0.8")
    print(f"- Mutation rate: 0.01")
    
    solution, value, history = solve_ga(
        weights, values, capacity,
        pop_size=30,
        generations=50,
        crossover_rate=0.8,
        mutation_rate=0.01
    )
    
    print(f"\n{'─' * 60}")
    print(f"KẾT QUẢ:")
    print(f"{'─' * 60}")
    print(f"Nghiệm tốt nhất: {solution}")
    print(f"Giá trị đạt được: {value}")
    
    # Tính trọng lượng
    total_weight = sum(solution[i] * weights[i] for i in range(len(solution)))
    print(f"Tổng trọng lượng: {total_weight}/{capacity}")
    
    # Items được chọn
    selected_items = [i for i in range(len(solution)) if solution[i] == 1]
    print(f"Items được chọn: {selected_items}")
    
    print(f"\nQuá trình hội tụ (10 thế hệ đầu):")
    for i in range(min(10, len(history))):
        print(f"  Generation {i+1:3d}: fitness = {history[i]}")
    
    print(f"\nQuá trình hội tụ (10 thế hệ cuối):")
    for i in range(max(0, len(history)-10), len(history)):
        print(f"  Generation {i+1:3d}: fitness = {history[i]}")
    
    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    test_ga()