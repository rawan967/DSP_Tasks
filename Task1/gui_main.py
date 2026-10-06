import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dsp_operations import ReadSignalFile, AddSignals, MultiplySignal

class LightDSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DSP Signal Processing Framework")
        self.root.geometry("1200x780")
        self.root.configure(bg="#f8fafc")  # Light Slate Background

        # dict(name: (indices, samples))
        self.signals_dict = {}
        
        self.setup_styles()
        self.create_layout()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Soft Light Color Palette
        bg_main = "#f8fafc"       
        card_bg = "#ffffff"        
        card_border = "#e2e8f0"   
        
        text_dark = "#1e293b"     
        text_muted = "#64748b"    
        accent_blue = "#0284c7"    
        
        # General Styles
        self.style.configure("TFrame", background=bg_main)
        self.style.configure("Card.TFrame", background=card_bg, relief="flat")
        
        # Labels
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=text_dark, background=bg_main)
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 9), foreground=text_muted, background=bg_main)
        self.style.configure("Section.TLabel", font=("Segoe UI", 10, "bold"), foreground=accent_blue, background=card_bg)
        self.style.configure("CardText.TLabel", font=("Segoe UI", 9), foreground=text_dark, background=card_bg)
        
        # Dropdowns (Comboboxes)
        self.style.configure("TCombobox", 
                             fieldbackground="#f1f5f9", 
                             background="#e2e8f0", 
                             foreground=text_dark, 
                             arrowcolor=accent_blue,
                             bordercolor="#cbd5e1",
                             lightcolor="#cbd5e1",
                             darkcolor="#cbd5e1")
        self.style.map("TCombobox", fieldbackground=[("readonly", "#f1f5f9")], foreground=[("readonly", text_dark)])

        # Soft Colored Buttons with Dark Clear Text
        self.style.configure("Blue.TButton", font=("Segoe UI", 9, "bold"), background="#0284c7", foreground="#ffffff", borderwidth=0)
        self.style.map("Blue.TButton", background=[("active", "#0369a1")])

        self.style.configure("Green.TButton", font=("Segoe UI", 9, "bold"), background="#10b981", foreground="#ffffff", borderwidth=0)
        self.style.map("Green.TButton", background=[("active", "#059669")])

        self.style.configure("Purple.TButton", font=("Segoe UI", 9, "bold"), background="#8b5cf6", foreground="#ffffff", borderwidth=0)
        self.style.map("Purple.TButton", background=[("active", "#7c3aed")])

        self.style.configure("Red.TButton", font=("Segoe UI", 9, "bold"), background="#ef4444", foreground="#ffffff", borderwidth=0)
        self.style.map("Red.TButton", background=[("active", "#dc2626")])

    def create_layout(self):
        # Main Container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=18, pady=18)

        # Left Control Sidebar
        sidebar = ttk.Frame(main_container, width=370)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 18))
        sidebar.pack_propagate(False)

        # App Header
        ttk.Label(sidebar, text="DSP SIGNAL PROCESSING", style="Header.TLabel").pack(anchor=tk.W)
        ttk.Label(sidebar, text="Digital Signal Processing Tool • Task 1 Framework", style="SubHeader.TLabel").pack(anchor=tk.W, pady=(0, 15))

        # --- Card 1: Signal Management ---
        card_load = ttk.Frame(sidebar, style="Card.TFrame", padding=12)
        card_load.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(card_load, text="SIGNAL MANAGEMENT", style="Section.TLabel").pack(anchor=tk.W, pady=(0, 6))
        
        btn_load = ttk.Button(card_load, text="📁 Load Signal File (.txt)", style="Blue.TButton", command=self.load_signal_file)
        btn_load.pack(fill=tk.X, pady=2)
        
        self.lbl_loaded_count = ttk.Label(card_load, text="Loaded Signals: 0", style="CardText.TLabel")
        self.lbl_loaded_count.pack(anchor=tk.W, pady=(4, 0))

        # --- Card 2: Single Signal Display ---
        card_disp = ttk.Frame(sidebar, style="Card.TFrame", padding=12)
        card_disp.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(card_disp, text="SINGLE SIGNAL DISPLAY", style="Section.TLabel").pack(anchor=tk.W, pady=(0, 6))
        
        ttk.Label(card_disp, text="Select Signal:", style="CardText.TLabel").pack(anchor=tk.W)
        self.combo_single = ttk.Combobox(card_disp, state="readonly")
        self.combo_single.pack(fill=tk.X, pady=(3, 8))

        btn_disp_single = ttk.Button(card_disp, text="Display Signal (Continuous & Discrete)", style="Blue.TButton", command=self.action_display_single)
        btn_disp_single.pack(fill=tk.X)

        # --- Card 3: Display Two Signals ---
        card_two = ttk.Frame(sidebar, style="Card.TFrame", padding=12)
        card_two.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(card_two, text="DISPLAY TWO SIGNALS", style="Section.TLabel").pack(anchor=tk.W, pady=(0, 6))
        
        f_combos = ttk.Frame(card_two, style="Card.TFrame")
        f_combos.pack(fill=tk.X, pady=(0, 6))
        
        self.combo_two_1 = ttk.Combobox(f_combos, state="readonly", width=14)
        self.combo_two_1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        
        self.combo_two_2 = ttk.Combobox(f_combos, state="readonly", width=14)
        self.combo_two_2.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(3, 0))

        btn_disp_two = ttk.Button(card_two, text="Compare Selected Two Signals", style="Blue.TButton", command=self.action_display_two)
        btn_disp_two.pack(fill=tk.X)

        # --- Card 4: Add Signals ---
        card_add = ttk.Frame(sidebar, style="Card.TFrame", padding=12)
        card_add.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(card_add, text="ARITHMETIC: ADD SIGNALS", style="Section.TLabel").pack(anchor=tk.W, pady=(0, 4))
        ttk.Label(card_add, text="Adds all loaded signals element-wise", style="CardText.TLabel").pack(anchor=tk.W, pady=(0, 6))
        
        btn_add = ttk.Button(card_add, text="➕ Add All Loaded Signals", style="Green.TButton", command=self.action_add)
        btn_add.pack(fill=tk.X)

        # --- Card 5: Multiply by Constant ---
        card_mult = ttk.Frame(sidebar, style="Card.TFrame", padding=12)
        card_mult.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(card_mult, text="ARITHMETIC: MULTIPLY BY CONSTANT", style="Section.TLabel").pack(anchor=tk.W, pady=(0, 4))
        
        btn_mult = ttk.Button(card_mult, text="✖ Multiply Selected Signal", style="Purple.TButton", command=self.action_multiply)
        btn_mult.pack(fill=tk.X)

        # Clear Canvas Button
        btn_clear = ttk.Button(sidebar, text="🗑 Clear Plot Canvas", style="Red.TButton", command=self.clear_canvas)
        btn_clear.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))

        # Right Visualization Area
        self.plot_container = ttk.Frame(main_container, style="Card.TFrame", padding=12)
        self.plot_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas = None

    # ------------------ Handlers ------------------

    def load_signal_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                indices, samples = ReadSignalFile(file_path)
                filename = file_path.replace("\\", "/").split("/")[-1]
                self.signals_dict[filename] = (indices, samples)
                
                signal_names = list(self.signals_dict.keys())
                self.combo_single['values'] = signal_names
                self.combo_two_1['values'] = signal_names
                self.combo_two_2['values'] = signal_names
                
                self.combo_single.set(filename)
                if len(signal_names) >= 2:
                    self.combo_two_1.set(signal_names[-2])
                    self.combo_two_2.set(signal_names[-1])

                self.lbl_loaded_count.config(text=f"Loaded Signals: {len(self.signals_dict)}")
                messagebox.showinfo("Success", f"Signal '{filename}' loaded successfully!")
                self.plot_single(indices, samples, f"Signal: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read signal file:\n{str(e)}")

    def action_display_single(self):
        selected = self.combo_single.get()
        if not selected or selected not in self.signals_dict:
            messagebox.showwarning("Warning", "Please select a signal from dropdown first!")
            return
        idx, samples = self.signals_dict[selected]
        self.plot_single(idx, samples, f"Signal: {selected}")

    def action_display_two(self):
        s1_name = self.combo_two_1.get()
        s2_name = self.combo_two_2.get()
        if not s1_name or not s2_name or s1_name not in self.signals_dict or s2_name not in self.signals_dict:
            messagebox.showwarning("Warning", "Please select two valid signals to compare!")
            return
        
        idx1, sam1 = self.signals_dict[s1_name]
        idx2, sam2 = self.signals_dict[s2_name]
        self.plot_two(idx1, sam1, s1_name, idx2, sam2, s2_name)

    def action_add(self):
        if len(self.signals_dict) < 2:
            messagebox.showwarning("Warning", "Please load at least 2 signals to perform Addition!")
            return
        
        # تحويل القيم المحفوظة في الـ Dictionary إلى List لنتمكن من جمعها
        signals_data = list(self.signals_dict.values())
        res_idx, res_sam = AddSignals(signals_data)
        self.plot_single(res_idx, res_sam, "Result of Adding Loaded Signals")

    def action_multiply(self):
        selected = self.combo_single.get()
        if not selected or selected not in self.signals_dict:
            messagebox.showwarning("Warning", "Please select a signal from dropdown first!")
            return
        
        const_val = simpledialog.askfloat("Multiply Constant", f"Enter constant factor for '{selected}':")
        if const_val is not None:
            idx, samples = self.signals_dict[selected]
            # تمرير قيم العينات فقط لضربها في الثابت
            new_samples = MultiplySignal(samples, const_val)
            self.plot_single(idx, new_samples, f"Multiplied: {selected} x {const_val}")

    # ------------------ High Quality Light Plotting ------------------

    def plot_single(self, indices, samples, title="Signal"):
        self.clear_canvas()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5.2), dpi=100)
        fig.patch.set_facecolor('#ffffff')
        
        # Continuous Plot
        ax1.plot(indices, samples, color='#0284c7', linewidth=1.6)
        ax1.set_title(f"{title}\n(Continuous)", color='#1e293b', fontsize=10, fontweight='bold', pad=8)
        ax1.set_xlabel("Index (n)", color='#64748b', fontsize=8)
        ax1.set_ylabel("Amplitude", color='#64748b', fontsize=8)
        ax1.tick_params(colors='#334155', labelsize=8)
        ax1.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
        ax1.set_facecolor('#f8fafc')
        
        # Discrete Stem Plot
        marker, stem, base = ax2.stem(indices, samples, linefmt='#ef4444', markerfmt='ro', basefmt='k-')
        plt.setp(marker, markersize=1, color='#ef4444')
        plt.setp(stem, linewidth=0.4, color='#ef4444')
        plt.setp(base, linewidth=0.8, color='#64748b')
        
        ax2.set_title(f"{title}\n(Discrete)", color='#1e293b', fontsize=10, fontweight='bold', pad=8)
        ax2.set_xlabel("Index (n)", color='#64748b', fontsize=8)
        ax2.set_ylabel("Amplitude", color='#64748b', fontsize=8)
        ax2.tick_params(colors='#334155', labelsize=8)
        ax2.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
        ax2.set_facecolor('#f8fafc')
        
        fig.tight_layout()
        self.render_canvas(fig)

    def plot_two(self, idx1, sam1, name1, idx2, sam2, name2):
        self.clear_canvas()
        fig, ax = plt.subplots(figsize=(9, 5.2), dpi=100)
        fig.patch.set_facecolor('#ffffff')
        
        m1, s1, _ = ax.stem(idx1, sam1, linefmt='#0284c7', markerfmt='bo', label=name1)
        plt.setp(m1, markersize=1, color='#0284c7')
        plt.setp(s1, linewidth=0.4, color='#0284c7')
        
        m2, s2, _ = ax.stem(idx2, sam2, linefmt='#10b981', markerfmt='go', label=name2)
        plt.setp(m2, markersize=1, color='#10b981')
        plt.setp(s2, linewidth=0.4, color='#10b981')
        
        ax.set_title(f"Comparing: {name1} vs {name2}", color='#1e293b', fontsize=11, fontweight='bold', pad=10)
        ax.set_xlabel("Index (n)", color='#64748b', fontsize=8)
        ax.set_ylabel("Amplitude", color='#64748b', fontsize=8)
        ax.tick_params(colors='#334155', labelsize=8)
        ax.legend(facecolor='#ffffff', edgecolor='#cbd5e1', labelcolor='#1e293b')
        ax.grid(True, linestyle='--', alpha=0.5, color='#cbd5e1')
        ax.set_facecolor('#f8fafc')
        
        fig.tight_layout()
        self.render_canvas(fig)

    def render_canvas(self, fig):
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def clear_canvas(self):
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

if __name__ == "__main__":
    root = tk.Tk()
    app = LightDSPApp(root)
    root.mainloop()