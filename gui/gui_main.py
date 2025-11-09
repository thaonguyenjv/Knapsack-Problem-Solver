import tkinter as tk
from tkinter import messagebox
import os
import sys
sys.dont_write_bytecode = True

# Thêm thư mục gốc vào path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from gui.gui_ga import App as GAApp
from gui.gui_woa import App as WOAApp
from gui.gui_benchmark import App as BenchmarkApp

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Knapsack Problem Solver")
        self.root.geometry("600x650")
        self.root.configure(bg="#ecf0f1")
        self.root.resizable(False, False)
        
        # Căn giữa cửa sổ
        self.center_window()
        
        # ============ TIÊU ĐỀ ============
        title_label = tk.Label(
            self.root,
            text="KNAPSACK PROBLEM SOLVER",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#ecf0f1",
            pady=20
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            self.root,
            text="Genetic Algorithm vs Whale Optimization Algorithm",
            font=("Arial", 12),
            fg="#7f8c8d",
            bg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # ============ ICON TÚI ============
        icon_frame = tk.Frame(self.root, bg="#ecf0f1")
        icon_frame.pack(pady=40)
        
        icon_label = tk.Label(
            icon_frame,
            text="__🚚_",
            font=("Arial", 120),
            bg="#ecf0f1"
        )
        icon_label.pack()
        
        # ============ CÁC NÚT CHỨC NĂNG ============
        button_frame = tk.Frame(self.root, bg="#ecf0f1")
        button_frame.pack(pady=30)
        
        # Nút 1: Chạy GA
        btn_ga = tk.Button(
            button_frame,
            text="CHẠY GENETIC ALGORITHM",
            font=("Arial", 14, "bold"),
            bg="#e67e22",
            fg="white",
            width=30,
            height=2,
            command=self.open_ga,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3
        )
        btn_ga.pack(pady=10)
        btn_ga.bind("<Enter>", lambda e: btn_ga.config(bg="#d35400"))
        btn_ga.bind("<Leave>", lambda e: btn_ga.config(bg="#e67e22"))
        
        # Nút 2: Chạy WOA
        btn_woa = tk.Button(
            button_frame,
            text="CHẠY WHALE OPTIMIZATION",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            width=30,
            height=2,
            command=self.open_woa,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3
        )
        btn_woa.pack(pady=10)
        btn_woa.bind("<Enter>", lambda e: btn_woa.config(bg="#2980b9"))
        btn_woa.bind("<Leave>", lambda e: btn_woa.config(bg="#3498db"))
        
        # Nút 3: So sánh GA vs WOA
        btn_compare = tk.Button(
            button_frame,
            text="SO SÁNH GA vs WOA",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            width=30,
            height=2,
            command=self.open_benchmark,
            cursor="hand2",
            relief=tk.RAISED,
            bd=3
        )
        btn_compare.pack(pady=10)
        btn_compare.bind("<Enter>", lambda e: btn_compare.config(bg="#229954"))
        btn_compare.bind("<Leave>", lambda e: btn_compare.config(bg="#27ae60"))
    
    def center_window(self):
        self.root.update_idletasks()
        width = 600
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def open_ga(self):
        try:
            # Ẩn cửa sổ chính
            self.root.withdraw()
            ga_window = tk.Toplevel(self.root)
            GAApp(ga_window)
            # Hiện lại cửa sổ chính khi đóng cửa sổ con
            ga_window.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(ga_window))
        except ImportError as e:
            messagebox.showerror("Lỗi", f"Không tìm thấy gui_ga.py!\nChi tiết: {e}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở GA window:\n{str(e)}")
    
    def open_woa(self):
        try:
            # Ẩn cửa sổ chính
            self.root.withdraw()
            woa_window = tk.Toplevel(self.root)
            WOAApp(woa_window)
            # Hiện lại cửa sổ chính khi đóng cửa sổ con
            woa_window.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(woa_window))
        except ImportError as e:
            messagebox.showerror("Lỗi", f"Không tìm thấy gui_woa.py!\nChi tiết: {e}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở WOA window:\n{str(e)}")
    
    def open_benchmark(self):
        try:
            # Ẩn cửa sổ chính
            self.root.withdraw()
            benchmark_window = tk.Toplevel(self.root)
            BenchmarkApp(benchmark_window)
            # Hiện lại cửa sổ chính khi đóng cửa sổ con
            benchmark_window.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(benchmark_window))
        except ImportError as e:
            messagebox.showerror("Lỗi", f"Không tìm thấy gui_benchmark.py!\nChi tiết: {e}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở Benchmark window:\n{str(e)}")

    def on_child_close(self, child_window):
        """Xử lý khi đóng cửa sổ con"""
        child_window.destroy()
        self.root.deiconify()  # Hiện lại cửa sổ chính

def main():
    """Hàm main để chạy ứng dụng"""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()