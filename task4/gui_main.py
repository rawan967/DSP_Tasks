"""Task 4 - DSP framework GUI with the 'Time Domain' menu."""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import dsp_operations as ops

# ---- colour palette: white / black / navy / gray ----
WHITE = "#FFFFFF"
BLACK = "#111111"
NAVY = "#14284B"
NAVY_HOVER = "#1F3A6E"
GRAY = "#6B7280"
GRAY_LIGHT = "#E5E7EB"
GRAY_BG = "#F4F5F7"


class ShiftDialog(simpledialog.Dialog):
    """Ask for k and for delay / advance."""

    def __init__(self, parent, title):
        self.k = None
        self.direction = None
        super().__init__(parent, title)

    def body(self, master):
        self.configure(bg=WHITE)
        master.configure(bg=WHITE)
        ttk.Label(master, text="Number of steps (k):").grid(row=0, column=0, sticky="w", pady=4)
        self.k_var = tk.StringVar(value="1")
        self.entry = ttk.Entry(master, textvariable=self.k_var, width=10)
        self.entry.grid(row=0, column=1, padx=6)
        self.dir_var = tk.StringVar(value="delay")
        ttk.Radiobutton(master, text="Delay   (y(n) = x(n-k))", variable=self.dir_var,
                        value="delay").grid(row=1, column=0, columnspan=2, sticky="w")
        ttk.Radiobutton(master, text="Advance (y(n) = x(n+k))", variable=self.dir_var,
                        value="advance").grid(row=2, column=0, columnspan=2, sticky="w")
        return self.entry

    def validate(self):
        try:
            self.k = int(self.k_var.get())
            if self.k < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "k must be a non-negative integer.", parent=self)
            return False
        return True

    def apply(self):
        self.direction = self.dir_var.get()


class App:
    PLOT_STEM_LIMIT = 100          # use stem plot for short signals, line plot for long ones

    def __init__(self, root):
        self.root = root
        root.title("DSP Framework - Task 4 (Time Domain)")
        root.geometry("1150x700")
        root.configure(bg=WHITE)
        self._apply_style()

        self.signal = None         # (indices, samples)
        self.result = None         # (indices, samples, title)

        self._build_menu()
        self._build_layout()
        self.load_manual()         # start with the default demo signal

    # ------------------------------------------------------------ style
    def _apply_style(self):
        st = ttk.Style()
        st.theme_use("clam")
        st.configure(".", background=WHITE, foreground=BLACK, font=("Segoe UI", 10))
        st.configure("TFrame", background=WHITE)
        st.configure("TLabel", background=WHITE, foreground=BLACK)
        st.configure("TLabelframe", background=WHITE, bordercolor=GRAY_LIGHT, relief="solid")
        st.configure("TLabelframe.Label", background=WHITE, foreground=NAVY,
                     font=("Segoe UI", 10, "bold"))
        st.configure("TSeparator", background=GRAY_LIGHT)
        st.configure("TEntry", fieldbackground=WHITE, foreground=BLACK,
                     bordercolor=GRAY, lightcolor=WHITE, darkcolor=WHITE, padding=4)
        st.configure("TRadiobutton", background=WHITE, foreground=BLACK)
        st.map("TRadiobutton", background=[("active", WHITE)], indicatorcolor=[("selected", NAVY)])
        # solid navy button
        st.configure("Accent.TButton", background=NAVY, foreground=WHITE, bordercolor=NAVY,
                     focusthickness=0, padding=(10, 6), font=("Segoe UI", 10, "bold"))
        st.map("Accent.TButton", background=[("active", NAVY_HOVER), ("pressed", BLACK)])
        # outlined gray button for the operation list
        st.configure("Op.TButton", background=WHITE, foreground=NAVY, bordercolor=GRAY,
                     focusthickness=0, padding=(10, 5), anchor="w")
        st.map("Op.TButton", background=[("active", NAVY), ("pressed", BLACK)],
               foreground=[("active", WHITE)], bordercolor=[("active", NAVY)])

    def _menu(self, parent):
        return tk.Menu(parent, tearoff=0, bg=WHITE, fg=BLACK, activebackground=NAVY,
                       activeforeground=WHITE, bd=0, relief="flat")

    # ------------------------------------------------------------ menus
    def _build_menu(self):
        bar = tk.Menu(self.root)
        self.root.config(menu=bar)

        file_m = self._menu(bar)
        file_m.add_command(label="Load Signal from File...", command=self.load_file)
        file_m.add_command(label="Save Result to File...", command=self.save_result)
        file_m.add_command(label="Use Result as Input", command=self.result_to_input)
        file_m.add_separator()
        file_m.add_command(label="Exit", command=self.root.destroy)
        bar.add_cascade(label="File", menu=file_m)

        td = self._menu(bar)
        td.add_command(label="Smoothing (Moving Average)...", command=self.do_smoothing)
        sharp = self._menu(td)
        sharp.add_command(label="First Derivative   y(n)=x(n)-x(n-1)", command=self.do_first_derivative)
        sharp.add_command(label="Second Derivative  y(n)=x(n+1)-2x(n)+x(n-1)", command=self.do_second_derivative)
        td.add_cascade(label="Sharpening", menu=sharp)
        td.add_command(label="Delay / Advance by k...", command=self.do_shift)
        td.add_command(label="Fold", command=self.do_fold)
        td.add_command(label="Delay / Advance Folded Signal...", command=self.do_shift_folded)
        td.add_separator()
        td.add_command(label="Remove DC Component", command=self.do_remove_dc)
        bar.add_cascade(label="Time Domain", menu=td)

    # ----------------------------------------------------------- layout
    def _build_layout(self):
        header = tk.Frame(self.root, bg=NAVY)
        header.pack(side="top", fill="x")
        tk.Label(header, text="DSP Framework", bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 15, "bold")).pack(side="left", padx=14, pady=8)
        tk.Label(header, text="Time Domain Processing", bg=NAVY, fg="#B8C0D0",
                 font=("Segoe UI", 10)).pack(side="left", pady=8)
        tk.Frame(self.root, bg=GRAY_LIGHT, height=2).pack(side="top", fill="x")

        left = ttk.Frame(self.root, padding=8)
        left.pack(side="left", fill="y")

        box = ttk.LabelFrame(left, text="1) Input signal", padding=8)
        box.pack(fill="x")
        ttk.Button(box, text="Load from file...", style="Accent.TButton",
                   command=self.load_file).pack(fill="x")
        ttk.Separator(box).pack(fill="x", pady=6)
        ttk.Label(box, text="or type samples (comma / space separated):").pack(anchor="w")
        self.values_var = tk.StringVar(value="1, 2, 3, 4, 5, 4, 3, 2, 1")
        ttk.Entry(box, textvariable=self.values_var, width=34).pack(fill="x", pady=2)
        row = ttk.Frame(box)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text="First index n:").pack(side="left")
        self.start_var = tk.StringVar(value="0")
        ttk.Entry(row, textvariable=self.start_var, width=6).pack(side="left", padx=4)
        ttk.Button(row, text="Set signal", style="Accent.TButton",
                   command=self.load_manual).pack(side="right")
        self.info_var = tk.StringVar()
        ttk.Label(box, textvariable=self.info_var, foreground=NAVY).pack(anchor="w", pady=(6, 0))

        ops_box = ttk.LabelFrame(left, text="2) Time Domain operations", padding=8)
        ops_box.pack(fill="x", pady=8)
        for text, cmd in (
            ("Smoothing (Moving Average)", self.do_smoothing),
            ("Sharpening: First Derivative", self.do_first_derivative),
            ("Sharpening: Second Derivative", self.do_second_derivative),
            ("Delay / Advance by k", self.do_shift),
            ("Fold", self.do_fold),
            ("Delay / Advance Folded", self.do_shift_folded),
            ("Remove DC Component", self.do_remove_dc),
        ):
            ttk.Button(ops_box, text=text, style="Op.TButton", command=cmd).pack(fill="x", pady=2)

        res = ttk.LabelFrame(left, text="3) Result", padding=8)
        res.pack(fill="both", expand=True)
        self.res_title = tk.StringVar(value="(no operation yet)")
        ttk.Label(res, textvariable=self.res_title, font=("Segoe UI", 10, "bold"),
                  foreground=NAVY, wraplength=280).pack(anchor="w")
        self.res_text = tk.Text(res, width=34, height=10, state="disabled", bg=GRAY_BG, fg=BLACK,
                                relief="flat", bd=0, highlightthickness=1,
                                highlightbackground=GRAY_LIGHT, font=("Consolas", 9))
        self.res_text.pack(fill="both", expand=True, pady=4)
        btns = ttk.Frame(res)
        btns.pack(fill="x")
        ttk.Button(btns, text="Save result", style="Accent.TButton",
                   command=self.save_result).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ttk.Button(btns, text="Use as input", style="Accent.TButton",
                   command=self.result_to_input).pack(side="left", expand=True, fill="x", padx=(3, 0))

        right = ttk.Frame(self.root)
        right.pack(side="right", fill="both", expand=True)
        self.fig = Figure(figsize=(7, 6), dpi=100, facecolor=WHITE)
        self.ax_in = self.fig.add_subplot(211)
        self.ax_out = self.fig.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        NavigationToolbar2Tk(self.canvas, right).update()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ------------------------------------------------------ signal input
    def _set_signal(self, idx, s):
        self.signal = (list(idx), list(s))
        self.info_var.set("N = %d samples, n from %d to %d" % (len(s), idx[0], idx[-1]))
        self.result = None
        self.res_title.set("(no operation yet)")
        self._show_text("")
        self._plot(self.ax_in, idx, s, "Input signal x(n)")
        self.ax_out.clear()
        self.ax_out.set_facecolor(WHITE)
        self.ax_out.set_title("Output (choose an operation from the Time Domain menu)",
                              color=GRAY, fontsize=11, loc="left")
        self.ax_out.tick_params(colors=GRAY)
        for sp in self.ax_out.spines.values():
            sp.set_color(GRAY_LIGHT)
        self.ax_out.grid(True, color=GRAY_LIGHT, linewidth=0.8)
        self._redraw()

    def load_manual(self):
        try:
            s = [float(v) for v in self.values_var.get().replace(",", " ").split()]
            n0 = int(self.start_var.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Samples must be numbers and the first index an integer.")
            return
        if not s:
            messagebox.showerror("Invalid input", "Enter at least one sample.")
            return
        self._set_signal(list(range(n0, n0 + len(s))), s)

    def load_file(self):
        path = filedialog.askopenfilename(title="Open signal file",
                                          filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        try:
            idx, s = ops.ReadSignalFileM(path)
            if not s:
                raise ValueError("no samples found")
        except Exception as e:
            messagebox.showerror("Cannot read file", str(e))
            return
        self._set_signal(idx, s)

    def save_result(self):
        if not self.result:
            messagebox.showinfo("Save result", "There is no result to save yet.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            ops.WriteSignalFile(path, self.result[0], self.result[1])

    def result_to_input(self):
        if not self.result:
            messagebox.showinfo("Use result", "There is no result yet.")
            return
        self._set_signal(self.result[0], self.result[1])

    # --------------------------------------------------------- operations
    def _need_signal(self):
        if not self.signal:
            messagebox.showwarning("No signal", "Load or enter an input signal first.")
            return False
        return True

    def _finish(self, title, idx, s):
        self.result = (idx, s, title)
        self.res_title.set("%s  (%d samples)" % (title, len(s)))
        lines = ["n\ty(n)"] + ["%d\t%.4f" % (i, v) for i, v in list(zip(idx, s))[:200]]
        if len(s) > 200:
            lines.append("... (%d more)" % (len(s) - 200))
        self._show_text("\n".join(lines))
        self._plot(self.ax_out, idx, s, title)
        self._redraw()

    def do_smoothing(self):
        if not self._need_signal():
            return
        n = len(self.signal[1])
        M = simpledialog.askinteger("Smoothing", "Number of points in the average (1 - %d):" % n,
                                    parent=self.root, minvalue=1, maxvalue=n)
        if M is None:
            return
        idx, s = ops.MovingAverage(*self.signal, M)
        self._finish("Moving average, M = %d" % M, idx, s)

    def do_first_derivative(self):
        if self._need_signal():
            if len(self.signal[1]) < 2:
                return messagebox.showwarning("Too short", "Need at least 2 samples.")
            self._finish("First derivative  y(n)=x(n)-x(n-1)", *ops.FirstDerivative(*self.signal))

    def do_second_derivative(self):
        if self._need_signal():
            if len(self.signal[1]) < 3:
                return messagebox.showwarning("Too short", "Need at least 3 samples.")
            self._finish("Second derivative  y(n)=x(n+1)-2x(n)+x(n-1)", *ops.SecondDerivative(*self.signal))

    def do_shift(self):
        if not self._need_signal():
            return
        d = ShiftDialog(self.root, "Delay / Advance")
        if d.k is None:
            return
        idx, s = ops.ShiftSignal(*self.signal, d.k, d.direction)
        self._finish("%s by %d" % (d.direction.capitalize(), d.k), idx, s)

    def do_fold(self):
        if self._need_signal():
            self._finish("Folded signal  y(n)=x(-n)", *ops.FoldSignal(*self.signal))

    def do_shift_folded(self):
        if not self._need_signal():
            return
        d = ShiftDialog(self.root, "Delay / Advance Folded Signal")
        if d.k is None:
            return
        idx, s = ops.ShiftFoldedSignal(*self.signal, d.k, d.direction)
        self._finish("Folded signal, %s by %d" % (d.direction, d.k), idx, s)

    def do_remove_dc(self):
        if self._need_signal():
            idx, s = ops.RemoveDCTime(*self.signal)
            mean = sum(self.signal[1]) / len(self.signal[1])
            self._finish("DC removed (mean = %.4f)" % mean, idx, s)

    # ------------------------------------------------------------ drawing
    def _plot(self, ax, idx, s, title):
        ax.clear()
        # input signal in gray, results in navy
        color = GRAY if title.startswith("Input") else NAVY
        ax.set_facecolor(WHITE)
        if len(s) <= self.PLOT_STEM_LIMIT:
            marker, stems, base = ax.stem(idx, s)
            marker.set_color(color)
            marker.set_markersize(5)
            stems.set_color(color)
            stems.set_linewidth(1.2)
            base.set_color(BLACK)
            base.set_linewidth(0.8)
        else:
            ax.plot(idx, s, color=color, linewidth=1.4)
        ax.set_title(title, color=NAVY, fontsize=11, fontweight="bold", loc="left")
        ax.set_xlabel("n", color=BLACK)
        ax.tick_params(colors=GRAY)
        for sp in ax.spines.values():
            sp.set_color(GRAY_LIGHT)
        ax.grid(True, color=GRAY_LIGHT, linewidth=0.8)

    def _redraw(self):
        self.fig.tight_layout()
        self.canvas.draw()

    def _show_text(self, text):
        self.res_text.config(state="normal")
        self.res_text.delete("1.0", "end")
        self.res_text.insert("1.0", text)
        self.res_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()