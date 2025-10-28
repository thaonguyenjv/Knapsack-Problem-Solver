import tkinter as tk
from tkinter import ttk, messagebox
import sys, os, threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import các module cùng cấp
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from woa_solver import WOA
from problem import weights, values, capacity, fitness
from utils import plot_convergence

class WOAGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Whale Optimization Algorithm - Knapsack Problem")
        self.root.geometry("950x700")
        self.root.resizable(False, False)

        # Biến trạng thái
        self.woa = None
        self.history = []
        self.is_running = False

        # Tạo giao diện
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # -------------------------------
    # 1. TẠO GIAO DIỆN
    # -------------------------------
    def create_widgets(self):
        # Tiêu đề
        tk.Label(self.root, text="WHALE OPTIMIZATION ALGORITHM (WOA)",
                 font=("Arial", 18, "bold"), bg="#2c3e50", fg="white",
                 height=2).pack(fill=tk.X)

        main = tk.Frame(self.root, bg="#ecf0f1")
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Khung trái – thông tin và điều khiển
        left = tk.LabelFrame(main, text="Cấu hình & Điều khiển",
                             font=("Arial", 12, "bold"), bg="#ecf0f1")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        # Thông tin bài toán
        tk.Label(left, text=f"Weights: {weights}", bg="#ecf0f1").pack(anchor="w")
        tk.Label(left, text=f"Values: {values}", bg="#ecf0f1").pack(anchor="w")
        tk.Label(left, text=f"Capacity: {capacity}", bg="#ecf0f1").pack(anchor="w", pady=(0,10))

        # Tham số WOA
        tk.Label(left, text="Số lượng cá voi:", bg="#ecf0f1").pack(anchor="w")
        self.num_whales = tk.IntVar(value=30)
        tk.Spinbox(left, from_=10, to=100, textvariable=self.num_whales, width=10).pack(anchor="w")

        tk.Label(left, text="Số vòng lặp:", bg="#ecf0f1").pack(anchor="w", pady=(8,0))
        self.num_iters = tk.IntVar(value=100)
        tk.Spinbox(left, from_=10, to=500, textvariable=self.num_iters, width=10).pack(anchor="w")

        # Nút điều khiển
        tk.Button(left, text="▶ Chạy WOA", bg="#27ae60", fg="white",
                  font=("Arial", 11, "bold"), command=self.start_woa).pack(fill=tk.X, pady=8)
        tk.Button(left, text="⬛ Dừng", bg="#e74c3c", fg="white",
                  font=("Arial", 11, "bold"), command=self.stop_woa).pack(fill=tk.X)

        # Thanh tiến trình
        self.progress_var = tk.StringVar(value="Chưa bắt đầu")
        tk.Label(left, textvariable=self.progress_var, bg="#ecf0f1").pack(anchor="w", pady=(10,0))
        self.progress_bar = ttk.Progressbar(left, mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=5)

        # Kết quả
        tk.Label(left, text="Kết quả tối ưu:", font=("Arial", 11, "bold"),
                 bg="#ecf0f1").pack(anchor="w", pady=(10,0))
        self.result_box = tk.Text(left, width=35, height=15,
                                  font=("Courier New", 9), wrap=tk.WORD)
        self.result_box.pack(fill=tk.BOTH, expand=True, pady=(5,10))

        # Khung phải – biểu đồ
        right = tk.LabelFrame(main, text="Biểu đồ hội tụ", font=("Arial", 12, "bold"), bg="#ecf0f1")
        right.grid(row=0, column=1, sticky="nsew")

        self.fig, self.ax = plt.subplots(figsize=(6,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Layout grid
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=2)
        main.grid_rowconfigure(0, weight=1)

        self.init_plot()

    # -------------------------------
    # 2. HÀM HIỂN THỊ
    # -------------------------------
    def init_plot(self):
        self.ax.clear()
        self.ax.set_title("Chưa có dữ liệu", fontsize=12)
        self.ax.set_xlabel("Iteration")
        self.ax.set_ylabel("Best Fitness")
        self.ax.grid(True)
        self.canvas.draw()

    def update_plot(self, history):
        self.ax.clear()
        self.ax.plot(history, color="#3498db", linewidth=2, marker="o", markersize=3)
        self.ax.set_title("WOA Convergence Curve", fontsize=12, fontweight="bold")
        self.ax.set_xlabel("Iteration")
        self.ax.set_ylabel("Best Fitness Value")
        self.ax.grid(True)
        self.canvas.draw()

    def show_results(self, best_solution, best_value):
        total_weight = sum(weights[i] * best_solution[i] for i in range(len(weights)))
        selected = [i+1 for i, x in enumerate(best_solution) if x == 1]

        result = "="*40 + "\nKẾT QUẢ WOA\n" + "="*40 + "\n"
        result += f"Nghiệm tốt nhất: {best_solution}\n"
        result += f"Vật được chọn: {selected}\n"
        result += f"Tổng giá trị: {best_value}\n"
        result += f"Tổng trọng lượng: {total_weight}/{capacity}\n"
        result += "="*40

        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, result)

        messagebox.showinfo("Hoàn tất", f"WOA hoàn thành!\nGiá trị tốt nhất: {best_value}")

    # -------------------------------
    # 3. XỬ LÝ CHẠY THUẬT TOÁN
    # -------------------------------
    def start_woa(self):
        if self.is_running:
            messagebox.showwarning("Cảnh báo", "Thuật toán đang chạy!")
            return

        self.is_running = True
        self.progress_var.set("Đang chạy...")
        self.progress_bar['value'] = 0
        self.result_box.delete(1.0, tk.END)
        self.init_plot()

        # Chạy trên thread riêng để GUI không bị đơ
        threading.Thread(target=self.run_woa, daemon=True).start()

    def run_woa(self):
        try:
            n_whales = self.num_whales.get()
            max_iter = self.num_iters.get()
            self.woa = WOA(n_whales=n_whales, max_iter=max_iter, dim=len(weights))

            # Chạy thuật toán WOA (trong file woa_solver.py)
            best_sol, best_val, history = self.woa.optimize()
            self.history = history

            # Cập nhật biểu đồ
            self.root.after(0, self.update_plot, history)
            self.root.after(0, self.show_results, best_sol, best_val)
            self.root.after(0, lambda: plot_convergence(history, "WOA"))  # Mở biểu đồ ngoài (nếu muốn)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

        finally:
            self.root.after(0, self.finish_woa)

    def stop_woa(self):
        if self.is_running:
            self.is_running = False
            self.progress_var.set("Đã dừng.")
            messagebox.showinfo("Dừng", "Đã dừng thuật toán.")

    def finish_woa(self):
        self.is_running = False
        self.progress_var.set("Hoàn thành!")
        self.progress_bar['value'] = 100

    # -------------------------------
    # 4. SỰ KIỆN HỆ THỐNG
    # -------------------------------
    def on_close(self):
        if self.is_running:
            if messagebox.askokcancel("Thoát", "Thuật toán đang chạy, thoát luôn?"):
                self.is_running = False
                plt.close("all")
                self.root.destroy()
        else:
            plt.close("all")
            self.root.destroy()


def main():
    root = tk.Tk()
    app = WOAGui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
