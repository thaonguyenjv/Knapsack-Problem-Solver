import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from woa_solver import WOA
from problem import weights, values, capacity, fitness
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WOAGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Whale Optimization Algorithm - Knapsack Problem")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Variables
        self.is_running = False
        self.woa = None
        self.history = []
        
        # Tạo giao diện
        self.create_widgets()
        
        # Xử lý sự kiện đóng cửa sổ (phải đặt sau create_widgets)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="WHALE OPTIMIZATION ALGORITHM", 
                              font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Parameters and Control
        left_frame = tk.LabelFrame(main_frame, text="Cấu hình & Điều khiển", 
                                   font=("Arial", 12, "bold"), bg="#ecf0f1", padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Problem info
        problem_frame = tk.LabelFrame(left_frame, text="Thông tin bài toán", 
                                     font=("Arial", 10, "bold"), bg="#ecf0f1", padx=10, pady=5)
        problem_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(problem_frame, text=f"Weights: {weights}", 
                bg="#ecf0f1", font=("Arial", 9)).pack(anchor="w")
        tk.Label(problem_frame, text=f"Values: {values}", 
                bg="#ecf0f1", font=("Arial", 9)).pack(anchor="w")
        tk.Label(problem_frame, text=f"Capacity: {capacity}", 
                bg="#ecf0f1", font=("Arial", 9, "bold")).pack(anchor="w")
        
        # Parameters
        param_frame = tk.LabelFrame(left_frame, text="Tham số WOA", 
                                   font=("Arial", 10, "bold"), bg="#ecf0f1", padx=10, pady=5)
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(param_frame, text="Số lượng cá voi:", bg="#ecf0f1", 
                font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=5)
        self.n_whales_var = tk.IntVar(value=30)
        tk.Spinbox(param_frame, from_=10, to=100, textvariable=self.n_whales_var, 
                  width=15, font=("Arial", 9)).grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(param_frame, text="Số vòng lặp:", bg="#ecf0f1", 
                font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=5)
        self.max_iter_var = tk.IntVar(value=100)
        tk.Spinbox(param_frame, from_=50, to=500, textvariable=self.max_iter_var, 
                  width=15, font=("Arial", 9)).grid(row=1, column=1, pady=5, padx=5)
        
        # Control buttons
        control_frame = tk.Frame(left_frame, bg="#ecf0f1")
        control_frame.pack(fill=tk.X, pady=10)
        
        self.start_btn = tk.Button(control_frame, text="▶ Chạy WOA", 
                                   command=self.start_optimization,
                                   bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                                   padx=20, pady=10, cursor="hand2")
        self.start_btn.pack(fill=tk.X, pady=5)
        
        self.stop_btn = tk.Button(control_frame, text="⬛ Dừng", 
                                  command=self.stop_optimization,
                                  bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
                                  padx=20, pady=10, cursor="hand2", state=tk.DISABLED)
        self.stop_btn.pack(fill=tk.X, pady=5)
        
        # Progress
        progress_frame = tk.LabelFrame(left_frame, text="Tiến trình", 
                                      font=("Arial", 10, "bold"), bg="#ecf0f1", padx=10, pady=5)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.StringVar(value="Chưa bắt đầu")
        tk.Label(progress_frame, textvariable=self.progress_var, 
                bg="#ecf0f1", font=("Arial", 9), fg="#2c3e50").pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Results
        result_frame = tk.LabelFrame(left_frame, text="Kết quả", 
                                    font=("Arial", 10, "bold"), bg="#ecf0f1", padx=10, pady=5)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(result_frame, height=12, width=35, 
                                   font=("Courier New", 9), bg="white", 
                                   relief=tk.SOLID, borderwidth=1)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Visualization
        right_frame = tk.LabelFrame(main_frame, text="Biểu đồ hội tụ", 
                                   font=("Arial", 12, "bold"), bg="#ecf0f1", padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(6, 5.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Initialize plot
        self.init_plot()
        
    def init_plot(self):
        """Khởi tạo biểu đồ trống"""
        self.ax.clear()
        self.ax.set_title("Waiting for optimization...", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Iteration", fontsize=10)
        self.ax.set_ylabel("Best Fitness Value", fontsize=10)
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
        
    def update_plot(self, history):
        """Cập nhật biểu đồ với dữ liệu mới"""
        self.ax.clear()
        self.ax.plot(history, linewidth=2, color='#3498db', marker='o', 
                    markersize=3, markevery=max(1, len(history)//20))
        self.ax.set_title("WOA Convergence Curve", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Iteration", fontsize=10)
        self.ax.set_ylabel("Best Fitness Value", fontsize=10)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlim(0, len(history)-1)
        if len(history) > 0:
            y_min = min(history) * 0.9 if min(history) > 0 else 0
            y_max = max(history) * 1.1
            self.ax.set_ylim(y_min, y_max)
        self.canvas.draw()
        
    def start_optimization(self):
        """Bắt đầu tối ưu hóa"""
        if self.is_running:
            messagebox.showwarning("Cảnh báo", "Thuật toán đang chạy!")
            return
        
        # Disable start button, enable stop button
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.is_running = True
        
        # Clear results
        self.result_text.delete(1.0, tk.END)
        self.init_plot()
        
        # Run optimization in separate thread
        thread = threading.Thread(target=self.run_woa, daemon=True)
        thread.start()
        
    def run_woa(self):
        """Chạy thuật toán WOA"""
        try:
            n_whales = self.n_whales_var.get()
            max_iter = self.max_iter_var.get()
            
            # Create WOA instance
            self.woa = WOA(n_whales=n_whales, max_iter=max_iter, dim=len(weights))
            
            # Initialize population
            population = self.woa.initialize_population()
            continuous_pop = [[0] * self.woa.dim for _ in range(n_whales)]
            
            # Find initial best
            fitness_list = [fitness(whale) for whale in population]
            best_idx = max(range(len(fitness_list)), key=lambda i: fitness_list[i])
            self.woa.best_position = population[best_idx].copy()
            self.woa.best_fitness = fitness_list[best_idx]
            self.history = [self.woa.best_fitness]
            
            # Main loop
            for iteration in range(max_iter):
                if not self.is_running:
                    break
                
                # Update progress
                progress = (iteration + 1) / max_iter * 100
                self.root.after(0, self.update_progress, iteration + 1, max_iter, progress)
                
                # WOA algorithm
                a = 2 - iteration * (2.0 / max_iter)
                
                for i in range(n_whales):
                    import random
                    import numpy as np
                    r1 = random.random()
                    r2 = random.random()
                    A = 2 * a * r1 - a
                    C = 2 * r2
                    b = 1
                    l = random.uniform(-1, 1)
                    p = random.random()
                    
                    if p < 0.5:
                        if abs(A) < 1:
                            D = [abs(C * continuous_pop[best_idx][j] - continuous_pop[i][j]) 
                                 for j in range(self.woa.dim)]
                            continuous_pop[i] = [continuous_pop[best_idx][j] - A * D[j] 
                                                for j in range(self.woa.dim)]
                        else:
                            rand_idx = random.randint(0, n_whales - 1)
                            D = [abs(C * continuous_pop[rand_idx][j] - continuous_pop[i][j]) 
                                 for j in range(self.woa.dim)]
                            continuous_pop[i] = [continuous_pop[rand_idx][j] - A * D[j] 
                                                for j in range(self.woa.dim)]
                    else:
                        D = [abs(continuous_pop[best_idx][j] - continuous_pop[i][j]) 
                             for j in range(self.woa.dim)]
                        continuous_pop[i] = [D[j] * np.exp(b * l) * np.cos(2 * np.pi * l) + 
                                            continuous_pop[best_idx][j] for j in range(self.woa.dim)]
                    
                    population[i] = self.woa.binary_conversion(continuous_pop[i])
                    population[i] = self.woa.repair_solution(population[i])
                
                # Update best
                fitness_list = [fitness(whale) for whale in population]
                current_best_idx = max(range(len(fitness_list)), key=lambda i: fitness_list[i])
                if fitness_list[current_best_idx] > self.woa.best_fitness:
                    self.woa.best_fitness = fitness_list[current_best_idx]
                    self.woa.best_position = population[current_best_idx].copy()
                    best_idx = current_best_idx
                
                self.history.append(self.woa.best_fitness)
                
                # Update plot every 5 iterations
                if (iteration + 1) % 5 == 0 or iteration == max_iter - 1:
                    self.root.after(0, self.update_plot, self.history.copy())
            
            # Show final results
            if self.is_running:
                self.root.after(0, self.show_results)
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")
        finally:
            self.root.after(0, self.optimization_complete)
    
    def update_progress(self, current, total, percentage):
        """Cập nhật tiến trình"""
        self.progress_var.set(f"Vòng lặp: {current}/{total}")
        self.progress_bar['value'] = percentage
        
    def show_results(self):
        """Hiển thị kết quả cuối cùng"""
        if self.woa and self.woa.best_position:
            total_weight = sum([weights[i] * self.woa.best_position[i] 
                              for i in range(len(weights))])
            selected_items = [i+1 for i in range(len(weights)) 
                            if self.woa.best_position[i] == 1]
            
            result = "="*40 + "\n"
            result += "KẾT QUẢ TỐI ƯU\n"
            result += "="*40 + "\n\n"
            result += f"Nghiệm: {self.woa.best_position}\n\n"
            result += f"Vật được chọn: {selected_items}\n\n"
            result += f"Tổng giá trị: {self.woa.best_fitness}\n\n"
            result += f"Tổng trọng lượng: {total_weight}/{capacity}\n\n"
            result += f"Số vòng lặp: {len(self.history)-1}\n"
            result += "="*40 + "\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            
            messagebox.showinfo("Hoàn thành", 
                              f"Tối ưu hóa hoàn tất!\nGiá trị tốt nhất: {self.woa.best_fitness}")
    
    def stop_optimization(self):
        """Dừng tối ưu hóa"""
        self.is_running = False
        self.progress_var.set("Đã dừng")
        messagebox.showinfo("Thông báo", "Đã dừng thuật toán!")
        
    def optimization_complete(self):
        """Hoàn thành tối ưu hóa"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        if self.progress_bar['value'] >= 100:
            self.progress_var.set("Hoàn thành")
    
    def on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        if self.is_running:
            if messagebox.askokcancel("Thoát", "Thuật toán đang chạy. Bạn có chắc muốn thoát?"):
                self.is_running = False
                plt.close('all')  # Đóng tất cả figure matplotlib
                self.root.destroy()
        else:
            plt.close('all')  # Đóng tất cả figure matplotlib
            self.root.destroy()

def main():
    root = tk.Tk()
    app = WOAGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()