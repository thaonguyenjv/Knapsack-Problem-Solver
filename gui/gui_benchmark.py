import os, sys, threading, tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from problem import load_knapsack_from_csv
from benchmark import run_single

class App:  
    def __init__(self, root):
        self.root = root
        self.root.title("GA vs WOA - So sánh hiệu năng")
        self.root.geometry("1600x950")
        self.root.configure(bg="#ecf0f1")
        self.data = []

        tk.Label(
            self.root,
            text="SO SÁNH HIỆU NĂNG GA vs WOA",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#ecf0f1",
            pady=15
        ).pack(fill=tk.X)

        nb = ttk.Notebook(self.root)
        nb.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        tab_th1 = tk.Frame(nb, bg="#ecf0f1")
        tab_th2 = tk.Frame(nb, bg="#ecf0f1")
        nb.add(tab_th1, text="QUẢN LÝ ĐƠN HÀNG")
        nb.add(tab_th2, text="LỰA CHỌN LOẠI XE")
        self.build_th1(tab_th1)
        self.build_th2(tab_th2)

    # ====================== TH1 ======================
    def build_th1(self, parent):
        left = tk.LabelFrame(parent, text="Tham số & Dữ liệu", font=("Arial", 14, "bold"), fg="#2c3e50", bg="#ecf0f1")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # TẢI FILE
        top = tk.Frame(left, bg="#ecf0f1"); top.pack(fill=tk.X, pady=5)
        tk.Label(top, text="Chọn file data:", font=("Arial", 12), bg="#ecf0f1").pack(side=tk.LEFT, padx=8)
        self.file1 = tk.StringVar(value="100")
        ttk.Combobox(top, textvariable=self.file1, values=["100","500","1000"], width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Tải dữ liệu", bg="#2980b9", fg="white", font=("Arial", 14, "bold"),
                  command=self.load_th1).pack(side=tk.LEFT, padx=5)

        # ====== NÚT THÊM/SỬA/XÓA ======
        btns = tk.Frame(left, bg="#ecf0f1"); btns.pack(fill=tk.X, pady=6)
        for txt, cmd in [("THÊM", self.add1), ("SỬA", self.edit1), ("XÓA", self.del1)]:
            tk.Button(btns, text=txt, bg="#bdc3c7", fg="black", width=9,
                      font=("Arial", 10, "bold"), command=cmd).pack(side=tk.LEFT, padx=4)

        # ====== PHẠM VI & LẦN CHẠY ======
        cfg = tk.LabelFrame(left, text="Cấu hình Benchmark", font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50")
        cfg.pack(fill=tk.X, pady=8)
        tk.Label(cfg, text="Số lần chạy:", font=("Arial", 12), bg="#ecf0f1").pack(anchor='w', padx=12)
        self.runs1 = tk.StringVar(value="5")
        tk.Entry(cfg, textvariable=self.runs1, width=18).pack(padx=12, pady=4)

        tk.Label(cfg, text="Phạm vi (start-end):", font=("Arial", 12), bg="#ecf0f1").pack(anchor='w', padx=12)
        f = tk.Frame(cfg, bg="#ecf0f1"); f.pack(padx=12, pady=4)
        self.start1 = tk.StringVar(value="0")
        self.end1 = tk.StringVar(value="100")
        tk.Entry(f, textvariable=self.start1, width=12).pack(side=tk.LEFT)
        tk.Label(f, text="-", font=("Arial", 14, "bold"), bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        tk.Entry(f, textvariable=self.end1, width=12).pack(side=tk.LEFT)

        # ====== NÚT CHẠY ======
        tk.Button(left, text="▶ CHẠY", bg="#27ae60", fg="white",
                  font=("Arial", 14, "bold"), height=2, command=self.run_th1_full).pack(fill=tk.X, padx=10, pady=15)
        
        # ====== THANH TRẠNG THÁI TH1 ======
        self.progress_var = tk.StringVar(value="Chưa bắt đầu")
        self.progress_label = tk.Label(left, textvariable=self.progress_var, bg="#ecf0f1", font=("Arial", 12), fg="#2c3e50")
        self.progress_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.progress_bar = ttk.Progressbar(left, mode="determinate")
        self.progress_bar.pack(fill=tk.X, padx=12, pady=5)

        # ====== BẢNG DỮ LIỆU ======
        tbl = tk.LabelFrame(left, text="Danh sách kiện hàng (Click để sửa/xóa)", font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50")
        tbl.pack(fill=tk.BOTH, expand=True, pady=10)
        cols = ("Tên", "Giá trị", "Trọng lượng")
        self.tree1 = ttk.Treeview(tbl, columns=cols, show="headings", height=14)
        for c in cols:
            self.tree1.heading(c, text=c)
            self.tree1.column(c, anchor="center", width=150)
        scrollbar = ttk.Scrollbar(tbl, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree1.pack(fill=tk.BOTH, expand=True)

        right = tk.LabelFrame(parent, text="", font=("Arial", 14, "bold"), fg="#2c3e50", bg="#ecf0f1")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # ====== KHUNG KẾT QUẢ ======
        self.result_frame1 = tk.LabelFrame(right, text="Kết quả", font=("Arial", 14, "bold"), fg="#2c3e50", bg="#ecf0f1")
        self.result_frame1.pack(fill=tk.X, pady=(0, 10))
        self.tree_result1 = ttk.Treeview(
            self.result_frame1, columns=("Algorithm", "Value", "Time", "Conv Speed", "Win"), show="headings", height=4
        )
        for c in ("Algorithm", "Value", "Time", "Conv Speed", "Win"):
            self.tree_result1.heading(c, text=c)
            self.tree_result1.column(c, anchor="center", width=120)
        self.tree_result1.pack(fill=tk.X, padx=12, pady=6)

        # BIỂU ĐỒ
        chart_frame = tk.Frame(right, bg="#ecf0f1")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(chart_frame, text="So sánh hiệu năng:", font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(anchor="w")

        plot_container = tk.Frame(chart_frame, bg="#ecf0f1")
        plot_container.pack(fill=tk.BOTH, expand=True)

        # Biểu đồ cột(thời gian + giá trị tb)
        left_plot = tk.Frame(plot_container, width=380, bg="#ecf0f1")
        left_plot.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.fig_bar = plt.Figure(figsize=(3.8, 6))
        self.ax_value = self.fig_bar.add_subplot(211)
        self.ax_time = self.fig_bar.add_subplot(212)
        self.can_bar = FigureCanvasTkAgg(self.fig_bar, left_plot)
        self.can_bar.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # biểu đồ hội tụ
        self.fig_conv = plt.Figure(figsize=(9, 6))
        self.ax_conv_plot = self.fig_conv.add_subplot(111)
        self.can_conv = FigureCanvasTkAgg(self.fig_conv, plot_container)
        self.can_conv.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # ====== HÀM LOAD FILE & XỬ LÝ ======
    def load_th1(self):
        try:
            size = self.file1.get()
            path = os.path.join(BASE_DIR, "data", f"data_{size}_unique.csv")
            w, v, _ = load_knapsack_from_csv(path)
            self.data = [(f"Hàng {i+1}", v[i], w[i]) for i in range(len(w))]
            self.end1.set(str(len(w)))
            self.refresh_tree1()
            messagebox.showinfo("Thành công", f"Đã tải {len(self.data)} kiện hàng!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải file: {str(e)}")

    def refresh_tree1(self):
        for i in self.tree1.get_children(): self.tree1.delete(i)
        for row in self.data: self.tree1.insert("", "end", values=row)
    # ====== CRUD ======
    def add1(self):
        n = simpledialog.askstring("THÊM", "Tên:")
        v = simpledialog.askinteger("THÊM", "Giá trị:")
        w = simpledialog.askinteger("THÊM", "Trọng lượng:")
        if n and v is not None and w is not None:
            self.data.append((n, v, w))
            self.refresh_tree1()

    def edit1(self):
        sel = self.tree1.selection()
        if not sel: return messagebox.showwarning("", "Chọn 1 dòng!")
        idx = self.tree1.index(sel[0])
        old = self.data[idx]
        n = simpledialog.askstring("SỬA", "Tên:", initialvalue=old[0])
        v = simpledialog.askinteger("SỬA", "Giá trị:", initialvalue=old[1])
        w = simpledialog.askinteger("SỬA", "Trọng lượng:", initialvalue=old[2])
        if n and v is not None and w is not None:
            self.data[idx] = (n, v, w)
            self.refresh_tree1()

    def del1(self):
        sel = self.tree1.selection()
        if sel and messagebox.askyesno("XÁC NHẬN", "Xóa dòng này?"):
            idx = self.tree1.index(sel[0])
            del self.data[idx]
            self.refresh_tree1()
    # ====== CHẠY BENCHMARK TH1 ======
    def run_th1_full(self):
        if not self.data:
            return messagebox.showerror("Lỗi", "Vui lòng tải dữ liệu trước khi chạy!")
        try:
            start = int(self.start1.get())
            end = int(self.end1.get())
            if start < 0:
                return messagebox.showerror("Lỗi", "Start phải >= 0!")
            if end <= start:
                return messagebox.showerror("Lỗi", "End phải lớn hơn Start!")
            if start >= len(self.data):
                return messagebox.showerror("Lỗi", f"Start không được >= {len(self.data)}!")
            if end > len(self.data):
                return messagebox.showerror("Lỗi", f"End không được vượt quá {len(self.data)} (tổng số items)!")
            runs = int(self.runs1.get())
            if runs < 1:
                return messagebox.showerror("Lỗi", "Số lần chạy phải >= 1!")
            self.progress_var.set("Đang chạy...")
            self.progress_bar["maximum"] = runs
            self.progress_bar["value"] = 0
        except ValueError:
            return messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
        threading.Thread(target=self.exec_th1_full, args=(start, end, runs), daemon=True).start()

    def exec_th1_full(self, start, end, runs):
        w = [x[2] for x in self.data[start:end]]
        v = [x[1] for x in self.data[start:end]]
        # trọng lượng là 50% tổng trọng lượng các kiện
        c = int(sum(w) * 0.5)

        ga_vals, ga_times, woa_vals, woa_times = [], [], [], []
        ga_hist_all, woa_hist_all = [], []

        for run_idx in range(runs):
            gv, gt, g_hist = run_single('GA', w, v, c, return_convergence=True)
            wv, wt, w_hist = run_single('WOA', w, v, c, return_convergence=True)
            ga_vals.append(gv); ga_times.append(gt); ga_hist_all.append(g_hist)
            woa_vals.append(wv); woa_times.append(wt); woa_hist_all.append(w_hist)
            
            # Cập nhật thanh tiến trình
            self.root.after(0, self.update_progress1, run_idx + 1, runs)

        max_len = max(len(h) for h in ga_hist_all + woa_hist_all if h)
        ga_hist_padded = [np.pad(h, (0, max_len - len(h)), constant_values=h[-1] if h else 0) if len(h) < max_len else h for h in ga_hist_all]
        woa_hist_padded = [np.pad(h, (0, max_len - len(h)), constant_values=h[-1] if h else 0) if len(h) < max_len else h for h in woa_hist_all]
        avg_ga_hist = np.mean(ga_hist_padded, axis=0) if ga_hist_padded else []
        avg_woa_hist = np.mean(woa_hist_padded, axis=0) if woa_hist_padded else []

        ga_conv_speeds = []
        woa_conv_speeds = []
        for g_hist, w_hist in zip(ga_hist_all, woa_hist_all):
            max_fitness = max(max(g_hist) if g_hist else 0, max(w_hist) if w_hist else 0)
            threshold = 0.95 * max_fitness if max_fitness > 0 else 0
            ga_gen = next((i for i, v in enumerate(g_hist) if v >= threshold), len(g_hist)) if g_hist else 0
            woa_gen = next((i for i, v in enumerate(w_hist) if v >= threshold), len(w_hist)) if w_hist else 0
            ga_conv_speeds.append(ga_gen)
            woa_conv_speeds.append(woa_gen)

        result = {
            'items': f"{start}-{end-1} ({len(w)} kiện)",
            'ga_val': np.mean(ga_vals), 'ga_time': np.mean(ga_times),
            'woa_val': np.mean(woa_vals), 'woa_time': np.mean(woa_times),
            'ga_conv_speed': np.mean(ga_conv_speeds), 'woa_conv_speed': np.mean(woa_conv_speeds),
            'ga_hist': avg_ga_hist, 'woa_hist': avg_woa_hist,
            'max_fitness': max(np.max(avg_ga_hist), np.max(avg_woa_hist)) if avg_ga_hist.size and avg_woa_hist.size else 0,
            'runs': runs
        }
        self.root.after(0, self.show_th1_result, result)

    def update_progress1(self, current, total):
        self.progress_bar["value"] = current
        self.progress_var.set(f"Đang chạy: {current}/{total} lần")

    def show_th1_result(self, r):
        self.progress_var.set(f"Hoàn thành! ({r['runs']} lần chạy)")
        
        for i in self.tree_result1.get_children(): self.tree_result1.delete(i)
        self.tree_result1.insert("", "end", values=(
            "GA", f"{r['ga_val']:,.0f}", f"{r['ga_time']:.3f}", f"{r['ga_conv_speed']:.1f}",
            'GA' if r['ga_val'] > r['woa_val'] else 'WOA' if r['woa_val'] > r['ga_val'] else 'Hòa'
        ))
        self.tree_result1.insert("", "end", values=(
            "WOA", f"{r['woa_val']:,.0f}", f"{r['woa_time']:.3f}", f"{r['woa_conv_speed']:.1f}",
            'WOA' if r['woa_val'] > r['ga_val'] else 'GA' if r['ga_val'] > r['woa_val'] else 'Hòa'
        ))

        self.ax_value.clear()
        self.ax_time.clear()
        self.ax_conv_plot.clear()

        bars_val = self.ax_value.bar(['GA', 'WOA'], [r['ga_val'], r['woa_val']], color=["#e67e22", "#3498db"], width=1, edgecolor='black')
        self.ax_value.set_title("Giá trị trung bình", fontsize=10, fontweight='bold')
        self.ax_value.set_ylabel("Giá trị")
        for bar in bars_val:
            h = bar.get_height()
            self.ax_value.text(bar.get_x() + bar.get_width()/2, h + h*0.02, f"{h:,.0f}", ha='center', fontsize=10, fontweight='bold')

        bars_time = self.ax_time.bar(['GA', 'WOA'], [r['ga_time'], r['woa_time']], color=["#e67e22", "#3498db"], width=1, edgecolor='black')
        self.ax_time.set_title("Thời gian trung bình (giây)", fontsize=10, fontweight='bold')
        self.ax_time.set_ylabel("Giây")
        for bar in bars_time:
            h = bar.get_height()
            self.ax_time.text(bar.get_x() + bar.get_width()/2, h + h*0.02, f"{h:.3f}", ha='center', fontsize=10, fontweight='bold')

        self.fig_bar.tight_layout()
        self.can_bar.draw()

        gens = range(len(r['ga_hist']))
        self.ax_conv_plot.plot(gens, r['ga_hist'], label='GA', color="#e67e22", linewidth=3)
        self.ax_conv_plot.plot(gens, r['woa_hist'], label='WOA', color="#3498db", linewidth=3)

        if r['max_fitness'] > 0:
            self.ax_conv_plot.axhline(y=0.95 * r['max_fitness'], color='red', linestyle='--', linewidth=2, label='95% tối ưu')

        self.ax_conv_plot.set_title(f"Biểu đồ hội tụ trung bình {r['items']}", fontsize=10, fontweight='bold', pad=15)
        self.ax_conv_plot.set_xlabel("Thế hệ")
        self.ax_conv_plot.set_ylabel("Giá trị tốt nhất")
        self.ax_conv_plot.legend(fontsize=10, loc='lower right')
        self.ax_conv_plot.grid(True, alpha=0.3)
        self.fig_conv.tight_layout()
        self.can_conv.draw()

    # ====================== TH2 ======================
    def build_th2(self, parent):
        left = tk.LabelFrame(parent, text="Tham số & Cấu hình", font=("Arial", 14, "bold"), fg="#2c3e50", bg="#ecf0f1")
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), pady=15)

        cfg = tk.Frame(left, bg="#ecf0f1"); cfg.pack(fill=tk.X, pady=10)
        tk.Label(cfg, text="File:", font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50").pack(anchor='w', padx=12, pady=2)
        self.file2 = tk.StringVar(value="100")
        ttk.Combobox(cfg, textvariable=self.file2, values=["100","500","1000"], width=15).pack(padx=12, pady=2)

        tk.Label(cfg, text="Tỷ lệ loại xe(%):", font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50").pack(anchor='w', padx=12, pady=2)
        self.ratio2 = tk.StringVar(value="30,50,70")
        tk.Entry(cfg, textvariable=self.ratio2, width=20).pack(padx=12, pady=2)

        tk.Label(cfg, text="Số lần chạy:", font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50").pack(anchor='w', padx=12, pady=2)
        self.runs2 = tk.StringVar(value="5")
        tk.Entry(cfg, textvariable=self.runs2, width=15).pack(padx=12, pady=2)

        tk.Button(cfg, text="▶ CHẠY", bg="#27ae60", fg="white",
                  font=("Arial", 12, "bold"), command=self.run_th2_full).pack(fill=tk.X, pady=15, padx=12)

        # ====== THANH TRẠNG THÁI TH2 ======
        self.progress_var2 = tk.StringVar(value="Chưa bắt đầu")
        self.progress_label2 = tk.Label(left, textvariable=self.progress_var2, bg="#ecf0f1", font=("Arial", 12), fg="#2c3e50")
        self.progress_label2.pack(anchor="w", padx=12, pady=(10, 0))
        self.progress_bar2 = ttk.Progressbar(left, mode="determinate")
        self.progress_bar2.pack(fill=tk.X, padx=12, pady=5)

        right = tk.LabelFrame(parent, text="", font=("Arial", 14, "bold"), fg="#2c3e50", bg="#ecf0f1")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))

        self.result_frame2 = tk.LabelFrame(right, text="Kết quả", font=("Arial", 14, "bold"), fg="#2c3e50", bg="#ecf0f1")
        self.result_frame2.pack(fill=tk.X, pady=(0, 10))
        self.tree_result2 = ttk.Treeview(
            self.result_frame2,
            columns=("Xe", "GA Val", "WOA Val", "GA Time", "WOA Time", "GA Conv", "WOA Conv", "Thắng"),
            show="headings", height=3
        )
        for c in ("Xe", "GA Val", "WOA Val", "GA Time", "WOA Time", "GA Conv", "WOA Conv", "Thắng"):
            self.tree_result2.heading(c, text=c)
            self.tree_result2.column(c, anchor="center", width=100)
        self.tree_result2.pack(fill=tk.X, padx=12, pady=6)

        chart_frame2 = tk.Frame(right, bg="#ecf0f1")
        chart_frame2.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        tk.Label(chart_frame2, text="So sánh hiệu năng:", font=("Arial", 14, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(anchor="w")

        plot_container2 = tk.Frame(chart_frame2, bg="#ecf0f1")
        plot_container2.pack(fill=tk.BOTH, expand=True)

        left_plot2 = tk.Frame(plot_container2, width=380, bg="#ecf0f1")
        left_plot2.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.fig_bar2 = plt.Figure(figsize=(3.8, 6))
        self.ax_value2 = self.fig_bar2.add_subplot(211)
        self.ax_time2 = self.fig_bar2.add_subplot(212)
        self.can_bar2 = FigureCanvasTkAgg(self.fig_bar2, left_plot2)
        self.can_bar2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # BIỂU ĐỒ HỘI TỤ - Sử dụng subplot để hiển thị nhiều xe
        self.fig_conv2 = plt.Figure(figsize=(9, 6))
        self.can_conv2 = FigureCanvasTkAgg(self.fig_conv2, plot_container2)
        self.can_conv2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def run_th2_full(self):
        try:
            file = self.file2.get()
            ratio_str = self.ratio2.get().strip()
            ratios = [int(x.strip()) for x in ratio_str.split(',') if x.strip().isdigit()]
            if not ratios or not 1 <= max(ratios) <= 99:
                raise ValueError
            runs = int(self.runs2.get())
            self.progress_var2.set("Đang chạy...")
            self.progress_bar2["maximum"] = len(ratios) * runs
            self.progress_bar2["value"] = 0
        except:
            messagebox.showerror("Lỗi", "Nhập đúng: File, Tỷ lệ (30,50,70), Số lần!")
            return
        threading.Thread(target=self.exec_th2_full, args=(file, ratios, runs), daemon=True).start()

    def exec_th2_full(self, file, ratios, runs):
        path = os.path.join(BASE_DIR, "data", f"data_{file}_unique.csv")
        w, v, _ = load_knapsack_from_csv(path)
        total_weight = sum(w)
        results = []
        total_progress = 0

        for idx, r in enumerate(ratios):
            c = int(total_weight * r / 100)
            name = 'Xe nhỏ' if r == 30 else 'Xe vừa' if r == 50 else 'Xe lớn' if r == 70 else f'Xe {r}%'
            print(f"TH2 | {name}: Capacity = {c} ({r}% của {total_weight})")
            ga_vals, ga_times, woa_vals, woa_times = [], [], [], []
            ga_hist_all, woa_hist_all = [], []

            for run_idx in range(runs):
                gv, gt, g_hist = run_single('GA', w, v, c, return_convergence=True)
                wv, wt, w_hist = run_single('WOA', w, v, c, return_convergence=True)
                ga_vals.append(gv); ga_times.append(gt); ga_hist_all.append(g_hist)
                woa_vals.append(wv); woa_times.append(wt); woa_hist_all.append(w_hist)
                
                # Cập nhật thanh tiến trình
                total_progress += 1
                self.root.after(0, self.update_progress2, total_progress, len(ratios) * runs, idx + 1, len(ratios), run_idx + 1, runs)

            max_len = max(len(h) for h in ga_hist_all + woa_hist_all if h)
            ga_hist_padded = [np.pad(h, (0, max_len - len(h)), constant_values=h[-1] if h else 0) if len(h) < max_len else h for h in ga_hist_all]
            woa_hist_padded = [np.pad(h, (0, max_len - len(h)), constant_values=h[-1] if h else 0) if len(h) < max_len else h for h in woa_hist_all]
            avg_ga_hist = np.mean(ga_hist_padded, axis=0) if ga_hist_padded else []
            avg_woa_hist = np.mean(woa_hist_padded, axis=0) if woa_hist_padded else []

            ga_conv_speeds, woa_conv_speeds = [], []
            for g_hist, w_hist in zip(ga_hist_all, woa_hist_all):
                max_f = max(max(g_hist), max(w_hist)) if g_hist and w_hist else 0
                threshold = 0.95 * max_f if max_f > 0 else 0
                ga_gen = next((i for i, v in enumerate(g_hist) if v >= threshold), len(g_hist))
                woa_gen = next((i for i, v in enumerate(w_hist) if v >= threshold), len(w_hist))
                ga_conv_speeds.append(ga_gen); woa_conv_speeds.append(woa_gen)

            results.append({
                'name': name,
                'ga_val': np.mean(ga_vals), 'woa_val': np.mean(woa_vals),
                'ga_time': np.mean(ga_times), 'woa_time': np.mean(woa_times),
                'ga_conv': np.mean(ga_conv_speeds), 'woa_conv': np.mean(woa_conv_speeds),
                'ga_hist': avg_ga_hist, 'woa_hist': avg_woa_hist,
                'max_fitness': max(np.max(avg_ga_hist), np.max(avg_woa_hist)) if avg_ga_hist.size and avg_woa_hist.size else 0
            })

        self.root.after(0, self.show_th2_result, results)

    def update_progress2(self, current, total, car_idx, total_cars, run_idx, runs_per_car):
        self.progress_bar2["value"] = current
        self.progress_var2.set(f"Xe {car_idx}/{total_cars} - Lần {run_idx}/{runs_per_car} (Tổng: {current}/{total})")

    def show_th2_result(self, results):
        self.progress_var2.set(f"Hoàn thành! ({len(results)} loại xe)")
        
        # CẬP NHẬT BẢNG KẾT QUẢ
        for i in self.tree_result2.get_children(): self.tree_result2.delete(i)
        for r in results:
            winner = 'GA' if r['ga_val'] > r['woa_val'] else 'WOA' if r['woa_val'] > r['ga_val'] else 'Hòa'
            self.tree_result2.insert("", "end", values=(
                r['name'], f"{r['ga_val']:,.0f}", f"{r['woa_val']:,.0f}",
                f"{r['ga_time']:.3f}", f"{r['woa_time']:.3f}",
                f"{r['ga_conv']:.1f}", f"{r['woa_conv']:.1f}", winner
            ))

        # TÍNH TRUNG BÌNH TẤT CẢ CÁC XE 
        avg_ga_val = np.mean([r['ga_val'] for r in results])
        avg_woa_val = np.mean([r['woa_val'] for r in results])
        avg_ga_time = np.mean([r['ga_time'] for r in results])
        avg_woa_time = np.mean([r['woa_time'] for r in results])

        
        self.ax_value2.clear()
        self.ax_time2.clear()

        bars_val = self.ax_value2.bar(['GA', 'WOA'], [avg_ga_val, avg_woa_val], 
                                     color=["#e67e22", "#3498db"], width=0.6, edgecolor='black')
        self.ax_value2.set_title("Giá trị trung bình (Tất cả xe)", fontsize=10, fontweight='bold')
        self.ax_value2.set_ylabel("Giá trị")
        for bar in bars_val:
            h = bar.get_height()
            self.ax_value2.text(bar.get_x() + bar.get_width()/2, h + h*0.02, f"{h:,.0f}", ha='center', fontsize=10, fontweight='bold')

        bars_time = self.ax_time2.bar(['GA', 'WOA'], [avg_ga_time, avg_woa_time], 
                                      color=["#e67e22", "#3498db"], width=1, edgecolor='black')
        self.ax_time2.set_title("Thời gian trung bình (giây)", fontsize=10, fontweight='bold')
        self.ax_time2.set_ylabel("Giây")
        for bar in bars_time:
            h = bar.get_height()
            self.ax_time2.text(bar.get_x() + bar.get_width()/2, h + h*0.02, f"{h:.3f}", ha='center', fontsize=10, fontweight='bold')

        self.fig_bar2.tight_layout()
        self.can_bar2.draw()

        # BIỂU ĐỒ HỘI TỤ - HIỂN THỊ TẤT CẢ CÁC XE
        self.fig_conv2.clear()
        
        # Xác định số lượng subplot dựa vào số xe
        num_cars = len(results)
        
        if num_cars == 1:
            # Chỉ 1 xe: hiển thị 1 biểu đồ lớn
            ax = self.fig_conv2.add_subplot(111)
            self._plot_convergence(ax, results[0], f"Biểu đồ hội tụ - {results[0]['name']}")
            
        elif num_cars == 2:
            # 2 xe: hiển thị 1 hàng 2 cột
            for i, r in enumerate(results):
                ax = self.fig_conv2.add_subplot(1, 2, i+1)
                self._plot_convergence(ax, r, f"{r['name']}")
                
        else:
            # 3+ xe: hiển thị 1 hàng 3 cột 
            cols = min(3, num_cars)  # Tối đa 3 cột
            rows = (num_cars + cols - 1) // cols  # Tính số hàng cần thiết
            
            for i, r in enumerate(results):
                ax = self.fig_conv2.add_subplot(rows, cols, i+1)
                self._plot_convergence(ax, r, f"{r['name']}")

        self.fig_conv2.tight_layout(pad=2.0)
        self.can_conv2.draw()

    def _plot_convergence(self, ax, result, title):
        """Hàm helper để vẽ biểu đồ hội tụ cho 1 loại xe"""
        gens = range(len(result['ga_hist']))
        
        ax.plot(gens, result['ga_hist'], label='GA', color="#e67e22", linewidth=2.5)
        ax.plot(gens, result['woa_hist'], label='WOA', color="#3498db", linewidth=2.5)

        # Đường 95% tối ưu
        if result['max_fitness'] > 0:
            ax.axhline(y=0.95 * result['max_fitness'], color='red', 
                      linestyle='--', linewidth=1.5, label='95% tối ưu', alpha=0.7)

        ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
        ax.set_xlabel("Thế hệ", fontsize=9)
        ax.set_ylabel("Giá trị tốt nhất", fontsize=9)
        ax.legend(fontsize=8, loc='lower right', frameon=True, fancybox=True, shadow=True)
        ax.grid(True, alpha=0.3)
        ax.tick_params(labelsize=8)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()