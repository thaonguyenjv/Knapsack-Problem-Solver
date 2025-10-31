import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys, os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ga_solver import solve_ga
from problem import weights, values, capacity, get_problem_info
from utils import plot_convergence


class GAGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Genetic Algorithm - Knapsack Problem")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        self.is_running = False
        self.history = []
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ==================== UI LAYOUT ====================
    def create_widgets(self):
        # Tiêu đề
        tk.Label(
            self.root,
            text="GENETIC ALGORITHM - KNAPSACK SOLVER",
            font=("Arial", 18, "bold"),
            fg="#2c3e50",
            bg="#ecf0f1",
            pady=10
        ).pack(fill=tk.X)

        main = tk.Frame(self.root, bg="#ecf0f1")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --------- LEFT PANEL (Parameters + Data) ---------
        left_frame = tk.LabelFrame(
            main, text="⚙ Tham số và Dữ liệu",
            font=("Arial", 12, "bold"), bg="#ecf0f1"
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        # === Tham số GA ===
        param_frame = tk.LabelFrame(
            left_frame, text="Tham số GA",
            font=("Arial", 11, "bold"), bg="#ecf0f1"
        )
        param_frame.pack(fill=tk.X, padx=10, pady=8)

        tk.Label(param_frame, text="Population size:", bg="#ecf0f1").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.pop_size = tk.IntVar(value=50)
        tk.Entry(param_frame, textvariable=self.pop_size, width=15).grid(row=0, column=1, pady=4, padx=5)

        tk.Label(param_frame, text="Generations:", bg="#ecf0f1").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.generations = tk.IntVar(value=100)
        tk.Entry(param_frame, textvariable=self.generations, width=15).grid(row=1, column=1, pady=4, padx=5)

        tk.Label(param_frame, text="Crossover rate:", bg="#ecf0f1").grid(row=2, column=0, sticky=tk.W, pady=4)
        self.crossover_rate = tk.DoubleVar(value=0.8)
        tk.Entry(param_frame, textvariable=self.crossover_rate, width=15).grid(row=2, column=1, pady=4, padx=5)

        tk.Label(param_frame, text="Mutation rate:", bg="#ecf0f1").grid(row=3, column=0, sticky=tk.W, pady=4)
        self.mutation_rate = tk.DoubleVar(value=0.05)
        tk.Entry(param_frame, textvariable=self.mutation_rate, width=15).grid(row=3, column=1, pady=4, padx=5)

        # === Dữ liệu hiện tại ===
        data_frame = tk.LabelFrame(
            left_frame, text="Dữ liệu Knapsack",
            font=("Arial", 11, "bold"), bg="#ecf0f1"
        )
        data_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        tk.Label(data_frame, text=get_problem_info(), bg="#ecf0f1",
                 font=("Courier New", 9), justify="left").pack(anchor="w", pady=5)

        # === Nút chạy ===
        tk.Button(
            left_frame,
            text="▶ CHẠY GA",
            bg="#27ae60",
            fg="white",
            font=("Arial", 13, "bold"),
            height=2,
            cursor="hand2",
            command=self.start_ga
        ).pack(fill=tk.X, padx=10, pady=15)

        # --------- RIGHT PANEL (Result + Chart) ---------
        right_frame = tk.LabelFrame(
            main, text="📊 Kết quả",
            font=("Arial", 12, "bold"), bg="#ecf0f1"
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

        # Kết quả chi tiết
        result_frame = tk.Frame(right_frame, bg="#ecf0f1")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(result_frame, text="Kết quả chi tiết:", font=("Arial", 11, "bold"),
                 bg="#ecf0f1").pack(anchor="w")

        self.result_box = tk.Text(result_frame, width=50, height=10,
                                  font=("Courier New", 9), wrap=tk.WORD)
        self.result_box.pack(fill=tk.BOTH, expand=True, pady=(5, 10))

        # Biểu đồ hội tụ
        chart_frame = tk.Frame(right_frame, bg="#ecf0f1")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(chart_frame, text="Biểu đồ hội tụ:",
                 font=("Arial", 11, "bold"), bg="#ecf0f1").pack(anchor="w")

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Progress bar
        self.progress_var = tk.StringVar(value="Chưa bắt đầu")
        self.progress_label = tk.Label(left_frame, textvariable=self.progress_var, bg="#ecf0f1", font=("Arial", 10))
        self.progress_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.progress_bar = ttk.Progressbar(left_frame, mode="determinate")
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)

        self.init_plot()

    # ==================== CHẠY THUẬT TOÁN ====================
    def init_plot(self):
        self.ax.clear()
        self.ax.set_title("Chưa có dữ liệu", fontsize=12)
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Fitness Value")
        self.ax.grid(True)
        self.canvas.draw()

    def update_plot(self, history):
        self.ax.clear()
        self.ax.plot(history, color="#e67e22", linewidth=2)
        self.ax.scatter(0, history[0], color="green", s=50, label="Start")
        self.ax.scatter(len(history) - 1, history[-1], color="red", s=50, label="End")
        self.ax.set_title("GA Convergence Curve", fontsize=12, fontweight="bold")
        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Best Fitness Value")
        self.ax.legend(loc="lower right")
        self.ax.grid(True)
        self.canvas.draw()

    def show_results(self, best_solution, best_value):
        total_weight = sum(weights[i] * best_solution[i] for i in range(len(weights)))
        selected = [i + 1 for i, x in enumerate(best_solution) if x == 1]

        result = "=" * 45 + "\nKẾT QUẢ GA\n" + "=" * 45 + "\n"
        result += f"Nghiệm tốt nhất: {best_solution}\n"
        result += f"Vật được chọn: {selected}\n"
        result += f"Tổng giá trị đạt được: {best_value}\n"
        result += f"Tổng trọng lượng: {total_weight}/{capacity}\n"

        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, result)

        messagebox.showinfo("Hoàn tất", f"GA hoàn thành!\nGiá trị tốt nhất: {best_value}")

    def start_ga(self):
        if self.is_running:
            messagebox.showwarning("Cảnh báo", "GA đang chạy!")
            return

        self.is_running = True
        self.progress_var.set("Đang chạy...")
        self.progress_bar["value"] = 0
        self.result_box.delete(1.0, tk.END)
        self.init_plot()

        threading.Thread(target=self.run_ga, daemon=True).start()

    def run_ga(self):
        try:
            pop_size = self.pop_size.get()
            generations = self.generations.get()
            crossover_rate = self.crossover_rate.get()
            mutation_rate = self.mutation_rate.get()

            best_sol, best_val, history = solve_ga(
                weights, values, capacity,
                pop_size=pop_size,
                generations=generations,
                crossover_rate=crossover_rate,
                mutation_rate=mutation_rate
            )
            self.history = history

            self.root.after(0, self.update_plot, history)
            self.root.after(0, self.show_results, best_sol, best_val)
            self.root.after(0, lambda: plot_convergence(history, "GA"))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
        finally:
            self.root.after(0, self.finish_ga)

    def finish_ga(self):
        self.is_running = False
        self.progress_var.set("Hoàn thành!")
        self.progress_bar["value"] = 100

    def on_close(self):
        plt.close("all")
        self.root.destroy()


def main():
    root = tk.Tk()
    app = GAGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
