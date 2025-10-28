"""
gui_ga.py - Giao diện Tkinter cho Genetic Algorithm
Giải thuật di truyền (Genetic Algorithm - GA) để giải bài toán Knapsack.
Cho phép người dùng nhập dữ liệu, tham số GA, chạy thuật toán và xem kết quả
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import sys
import os

# Import GA solver từ thư mục cha
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ga_solver import solve_ga, calculate_fitness

# Import matplotlib cho vẽ biểu đồ
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Cảnh báo: Không tìm thấy matplotlib. Cài đặt bằng: pip install matplotlib")


class GAWindow:
    """Cửa sổ GUI cho Genetic Algorithm"""
    
    def __init__(self, parent=None):
        """
        Khởi tạo cửa sổ GA
        Args:
            parent: Cửa sổ cha (nếu gọi từ GUI chính), None nếu chạy độc lập
        """
        # Tạo cửa sổ mới hoặc dùng parent
        if parent is None:
            self.root = tk.Tk()
            self.root.title("Genetic Algorithm - Knapsack Problem")
        else:
            self.root = tk.Toplevel(parent)
            self.root.title("Genetic Algorithm - Knapsack Problem")
        
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Dữ liệu bài toán
        self.weights = []
        self.values = []
        self.capacity = 0
        
        # Kết quả sau khi chạy GA
        self.best_solution = None
        self.best_value = 0
        self.history = []
        
        # Trạng thái animation
        self.animation_running = False
        self.animation_index = 0
        
        # Thiết lập giao diện
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập toàn bộ giao diện"""
        
        # ===== HEADER =====
        title_label = tk.Label(
            self.root,
            text="GENETIC ALGORITHM - KNAPSACK SOLVER",
            font=("Arial", 18, "bold"),
            fg="#2c3e50",
            bg="#ecf0f1",
            pady=10
        )
        title_label.pack(fill=tk.X, pady=(0, 10))
        
        # ===== MAIN CONTAINER =====
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # ===== LEFT PANEL - INPUT =====
        left_frame = tk.LabelFrame(
            main_frame,
            text="⚙ Tham số và Dữ liệu",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10,
            bg="#ecf0f1"
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # ----- GA Parameters -----
        param_frame = tk.LabelFrame(
            left_frame, 
            text="Tham số GA", 
            padx=10, 
            pady=8,
            font=("Arial", 10, "bold"),
            bg="#ecf0f1"
        )
        param_frame.pack(fill=tk.X, pady=5)
        
        # Population size
        tk.Label(param_frame, text="Population Size:", bg="#ecf0f1").grid(
            row=0, column=0, sticky=tk.W, pady=4
        )
        self.pop_size_var = tk.StringVar(value="50")
        tk.Entry(param_frame, textvariable=self.pop_size_var, width=18).grid(
            row=0, column=1, pady=4, padx=5
        )
        
        # Generations
        tk.Label(param_frame, text="Generations:", bg="#ecf0f1").grid(
            row=1, column=0, sticky=tk.W, pady=4
        )
        self.generations_var = tk.StringVar(value="100")
        tk.Entry(param_frame, textvariable=self.generations_var, width=18).grid(
            row=1, column=1, pady=4, padx=5
        )
        
        # Crossover rate
        tk.Label(param_frame, text="Crossover Rate:", bg="#ecf0f1").grid(
            row=2, column=0, sticky=tk.W, pady=4
        )
        self.crossover_var = tk.StringVar(value="0.8")
        tk.Entry(param_frame, textvariable=self.crossover_var, width=18).grid(
            row=2, column=1, pady=4, padx=5
        )
        
        # Mutation rate
        tk.Label(param_frame, text="Mutation Rate:", bg="#ecf0f1").grid(
            row=3, column=0, sticky=tk.W, pady=4
        )
        self.mutation_var = tk.StringVar(value="0.01")
        tk.Entry(param_frame, textvariable=self.mutation_var, width=18).grid(
            row=3, column=1, pady=4, padx=5
        )
        
        # ----- Data Input -----
        data_frame = tk.LabelFrame(
            left_frame, 
            text="Dữ liệu Knapsack", 
            padx=10, 
            pady=8,
            font=("Arial", 10, "bold"),
            bg="#ecf0f1"
        )
        data_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Number of items + Random button
        item_control_frame = tk.Frame(data_frame, bg="#ecf0f1")
        item_control_frame.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=4)
        
        tk.Label(item_control_frame, text="Số lượng items:", bg="#ecf0f1").pack(side=tk.LEFT)
        self.num_items_var = tk.StringVar(value="10")
        tk.Entry(item_control_frame, textvariable=self.num_items_var, width=10).pack(
            side=tk.LEFT, padx=5
        )
        
        tk.Button(
            item_control_frame,
            text="🎲 Sinh ngẫu nhiên",
            command=self.generate_random_data,
            bg="#3498db",
            fg="white",
            font=("Arial", 9, "bold"),
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=5)
        
        # Weights input
        tk.Label(data_frame, text="Weights:", bg="#ecf0f1").grid(
            row=1, column=0, sticky=tk.NW, pady=4
        )
        self.weights_text = scrolledtext.ScrolledText(
            data_frame, 
            height=4, 
            width=35,
            font=("Courier", 9)
        )
        self.weights_text.grid(row=1, column=1, columnspan=2, pady=4, padx=5)
        
        # Values input
        tk.Label(data_frame, text="Values:", bg="#ecf0f1").grid(
            row=2, column=0, sticky=tk.NW, pady=4
        )
        self.values_text = scrolledtext.ScrolledText(
            data_frame, 
            height=4, 
            width=35,
            font=("Courier", 9)
        )
        self.values_text.grid(row=2, column=1, columnspan=2, pady=4, padx=5)
        
        # Capacity input
        tk.Label(data_frame, text="Capacity:", bg="#ecf0f1").grid(
            row=3, column=0, sticky=tk.W, pady=4
        )
        self.capacity_var = tk.StringVar(value="50")
        tk.Entry(data_frame, textvariable=self.capacity_var, width=18).grid(
            row=3, column=1, pady=4, padx=5, sticky=tk.W
        )
        
        # ----- RUN BUTTON -----
        tk.Button(
            left_frame,
            text="▶ CHẠY GENETIC ALGORITHM",
            command=self.run_ga,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            cursor="hand2"
        ).pack(fill=tk.X, pady=10)
        
        # ===== RIGHT PANEL - RESULTS =====
        right_frame = tk.LabelFrame(
            main_frame,
            text="📊 Kết quả",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10,
            bg="#ecf0f1"
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # ----- Results Text Area -----
        result_label = tk.Label(
            right_frame, 
            text="Kết quả chi tiết:",
            font=("Arial", 10, "bold"),
            bg="#ecf0f1"
        )
        result_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.result_text = scrolledtext.ScrolledText(
            right_frame,
            height=12,
            width=45,
            font=("Courier", 9),
            bg="#ffffff"
        )
        self.result_text.pack(fill=tk.X, pady=5)
        
        # ----- Plot Area -----
        if MATPLOTLIB_AVAILABLE:
            plot_label = tk.Label(
                right_frame, 
                text="Biểu đồ hội tụ:",
                font=("Arial", 10, "bold"),
                bg="#ecf0f1"
            )
            plot_label.pack(anchor=tk.W, pady=(10, 5))
            
            self.plot_frame = tk.Frame(right_frame, bg="#ecf0f1")
            self.plot_frame.pack(fill=tk.BOTH, expand=True, pady=5)
            
            # Create matplotlib figure
            self.fig = Figure(figsize=(5, 3.5), dpi=90)
            self.ax = self.fig.add_subplot(111)
            self.ax.set_title("Chưa có dữ liệu", fontsize=10)
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            tk.Label(
                right_frame,
                text="⚠ Cài đặt matplotlib để xem biểu đồ:\npip install matplotlib",
                fg="red",
                bg="#ecf0f1",
                font=("Arial", 10)
            ).pack(pady=20)
        
        # ----- Animation Controls -----
        animation_frame = tk.Frame(right_frame, bg="#ecf0f1")
        animation_frame.pack(fill=tk.X, pady=10)
        
        self.animate_btn = tk.Button(
            animation_frame,
            text="▶ Chạy Animation",
            command=self.start_animation,
            bg="#9b59b6",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            width=15
        )
        self.animate_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            animation_frame,
            text="■ Dừng",
            command=self.stop_animation,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            state=tk.DISABLED,
            width=10
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Generate default data khi khởi động
        self.generate_random_data()
    
    def generate_random_data(self):
        """Sinh dữ liệu Knapsack ngẫu nhiên"""
        try:
            n = int(self.num_items_var.get())
            if n <= 0 or n > 1000:
                messagebox.showerror("Lỗi", "Số lượng items phải từ 1 đến 1000")
                return
            
            # Sinh weights và values ngẫu nhiên
            weights = [random.randint(1, 20) for _ in range(n)]
            values = [random.randint(1, 30) for _ in range(n)]
            
            # Capacity = 40-60% tổng trọng lượng (để bài toán có ý nghĩa)
            total_weight = sum(weights)
            capacity = int(total_weight * random.uniform(0.4, 0.6))
            
            # Hiển thị lên GUI
            self.weights_text.delete(1.0, tk.END)
            self.weights_text.insert(1.0, ", ".join(map(str, weights)))
            
            self.values_text.delete(1.0, tk.END)
            self.values_text.insert(1.0, ", ".join(map(str, values)))
            
            self.capacity_var.set(str(capacity))
            
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng items không hợp lệ!")
    
    def parse_data(self):
        """
        Đọc và parse dữ liệu từ GUI
        Returns:
            True nếu dữ liệu hợp lệ, False nếu có lỗi
        """
        try:
            # Parse weights
            weights_str = self.weights_text.get(1.0, tk.END).strip()
            self.weights = [int(x.strip()) for x in weights_str.split(",") if x.strip()]
            
            # Parse values
            values_str = self.values_text.get(1.0, tk.END).strip()
            self.values = [int(x.strip()) for x in values_str.split(",") if x.strip()]
            
            # Parse capacity
            self.capacity = int(self.capacity_var.get())
            
            # Validate
            if len(self.weights) != len(self.values):
                raise ValueError("Số lượng weights và values phải bằng nhau!")
            
            if len(self.weights) == 0:
                raise ValueError("Phải có ít nhất 1 item!")
            
            if self.capacity <= 0:
                raise ValueError("Capacity phải lớn hơn 0!")
            
            if any(w < 0 for w in self.weights):
                raise ValueError("Weights phải là số không âm!")
            
            if any(v < 0 for v in self.values):
                raise ValueError("Values phải là số không âm!")
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Lỗi dữ liệu", str(e))
            return False
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc dữ liệu: {str(e)}")
            return False
    
    def run_ga(self):
        """Chạy thuật toán Genetic Algorithm"""
        # Validate dữ liệu
        if not self.parse_data():
            return
        
        try:
            # Parse parameters
            pop_size = int(self.pop_size_var.get())
            generations = int(self.generations_var.get())
            crossover_rate = float(self.crossover_var.get())
            mutation_rate = float(self.mutation_var.get())
            
            # Validate parameters
            if pop_size <= 0 or generations <= 0:
                raise ValueError("Population size và Generations phải > 0")
            
            if not (0 <= crossover_rate <= 1):
                raise ValueError("Crossover rate phải trong khoảng [0, 1]")
            
            if not (0 <= mutation_rate <= 1):
                raise ValueError("Mutation rate phải trong khoảng [0, 1]")
            
            # Clear previous results
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "⏳ Đang chạy Genetic Algorithm...\n")
            self.result_text.insert(tk.END, "Vui lòng đợi...\n")
            self.root.update()
            
            # Run GA
            self.best_solution, self.best_value, self.history = solve_ga(
                self.weights,
                self.values,
                self.capacity,
                pop_size=pop_size,
                generations=generations,
                crossover_rate=crossover_rate,
                mutation_rate=mutation_rate
            )
            
            # Display results
            self.display_results()
            
            # Plot convergence curve
            if MATPLOTLIB_AVAILABLE:
                self.plot_convergence()
            
            messagebox.showinfo("Thành công", "Đã chạy GA xong!")
            
        except ValueError as e:
            messagebox.showerror("Lỗi tham số", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi chạy GA:\n{str(e)}")
    
    def display_results(self):
        """Hiển thị kết quả lên text area"""
        self.result_text.delete(1.0, tk.END)
        
        # Header
        self.result_text.insert(tk.END, "=" * 45 + "\n")
        self.result_text.insert(tk.END, "   KẾT QUẢ GENETIC ALGORITHM\n")
        self.result_text.insert(tk.END, "=" * 45 + "\n\n")
        
        # Best solution
        self.result_text.insert(tk.END, "✓ Nghiệm tốt nhất:\n")
        self.result_text.insert(tk.END, f"  {self.best_solution}\n\n")
        
        # Best value
        self.result_text.insert(tk.END, f"✓ Giá trị đạt được: {self.best_value}\n\n")
        
        # Total weight
        total_weight = sum(self.best_solution[i] * self.weights[i] 
                          for i in range(len(self.best_solution)))
        self.result_text.insert(tk.END, f"✓ Tổng trọng lượng: {total_weight}/{self.capacity}\n")
        
        utilization = (total_weight / self.capacity * 100) if self.capacity > 0 else 0
        self.result_text.insert(tk.END, f"  (Sử dụng: {utilization:.1f}%)\n\n")
        
        # Selected items
        selected = [i for i in range(len(self.best_solution)) if self.best_solution[i] == 1]
        self.result_text.insert(tk.END, f"✓ Items được chọn ({len(selected)} items):\n")
        self.result_text.insert(tk.END, f"  {selected}\n\n")
        
        # Details of selected items
        self.result_text.insert(tk.END, "✓ Chi tiết items:\n")
        for idx in selected[:5]:  # Hiển thị tối đa 5 items đầu
            self.result_text.insert(
                tk.END, 
                f"  Item {idx}: w={self.weights[idx]}, v={self.values[idx]}\n"
            )
        if len(selected) > 5:
            self.result_text.insert(tk.END, f"  ... và {len(selected)-5} items khác\n")
        
        # Convergence info
        self.result_text.insert(tk.END, f"\n" + "-" * 45 + "\n")
        self.result_text.insert(tk.END, f"Số thế hệ chạy: {len(self.history)}\n")
        self.result_text.insert(tk.END, f"Fitness ban đầu: {self.history[0]}\n")
        self.result_text.insert(tk.END, f"Fitness cuối cùng: {self.history[-1]}\n")
        
        improvement = self.history[-1] - self.history[0]
        self.result_text.insert(tk.END, f"Cải thiện: +{improvement}\n")
    
    def plot_convergence(self):
        """Vẽ biểu đồ hội tụ của GA"""
        self.ax.clear()
        
        generations = range(1, len(self.history) + 1)
        
        # Vẽ đường hội tụ
        self.ax.plot(generations, self.history, 'b-', linewidth=2, label='Best Fitness')
        self.ax.fill_between(generations, 0, self.history, alpha=0.2)
        
        # Đánh dấu điểm đầu và cuối
        self.ax.plot(1, self.history[0], 'go', markersize=8, label='Start')
        self.ax.plot(len(self.history), self.history[-1], 'ro', markersize=8, label='End')
        
        self.ax.set_xlabel('Generation', fontsize=10, fontweight='bold')
        self.ax.set_ylabel('Fitness Value', fontsize=10, fontweight='bold')
        self.ax.set_title('GA Convergence Curve', fontsize=12, fontweight='bold')
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.legend(loc='lower right', fontsize=9)
        
        # Set limits
        self.ax.set_xlim(0, len(self.history) + 1)
        y_max = max(self.history) * 1.1 if max(self.history) > 0 else 10
        self.ax.set_ylim(0, y_max)
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def start_animation(self):
        """Bắt đầu animation hội tụ"""
        if len(self.history) == 0:
            messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu!\nHãy chạy GA trước khi xem animation.")
            return
        
        self.animation_running = True
        self.animation_index = 0
        self.animate_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.animate_step()
    
    def stop_animation(self):
        """Dừng animation"""
        self.animation_running = False
        self.animate_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        # Vẽ lại biểu đồ đầy đủ
        if len(self.history) > 0:
            self.plot_convergence()
    
    def animate_step(self):
        """Thực hiện một bước animation"""
        if not self.animation_running or self.animation_index >= len(self.history):
            self.stop_animation()
            return
        
        # Vẽ biểu đồ từ đầu đến index hiện tại
        self.ax.clear()
        
        current_gen = self.animation_index + 1
        x = range(1, current_gen + 1)
        y = self.history[:current_gen]
        
        # Vẽ đường
        self.ax.plot(x, y, 'b-', linewidth=2, marker='o', markersize=4)
        self.ax.fill_between(x, 0, y, alpha=0.2)
        
        # Đánh dấu điểm hiện tại
        self.ax.plot(current_gen, y[-1], 'ro', markersize=10)
        
        self.ax.set_xlabel('Generation', fontsize=10, fontweight='bold')
        self.ax.set_ylabel('Fitness Value', fontsize=10, fontweight='bold')
        self.ax.set_title(
            f'GA Convergence (Gen {current_gen}/{len(self.history)})', 
            fontsize=12, 
            fontweight='bold'
        )
        self.ax.grid(True, alpha=0.3, linestyle='--')
        
        # Fixed limits
        self.ax.set_xlim(0, len(self.history) + 1)
        y_max = max(self.history) * 1.1 if max(self.history) > 0 else 10
        self.ax.set_ylim(0, y_max)
        
        self.fig.tight_layout()
        self.canvas.draw()
        
        self.animation_index += 1
        
        # Tính delay (nhanh hơn nếu nhiều generations)
        if len(self.history) > 200:
            delay = 20
        elif len(self.history) > 100:
            delay = 50
        else:
            delay = 100
        
        # Schedule next step
        self.root.after(delay, self.animate_step)
    
    def run(self):
        """Chạy main loop của cửa sổ"""
        self.root.mainloop()


# ===== MAIN - Để test độc lập =====
def main():
    """Hàm main để test GUI độc lập"""
    print("Khởi động GUI Genetic Algorithm...")
    app = GAWindow()
    app.run()


if __name__ == "__main__":
    main()