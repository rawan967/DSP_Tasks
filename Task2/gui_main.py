
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from dsp_operations import (
    ReadSignalFileM,
    AddSignals,
    MultiplySignal,
    SubSignals,
    SquaringSignal,
    NormalizeSignal,
    AccumulationSignal
)


class LightDSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DSP Studio | Signal Processing")
        self.root.geometry("1200x780")
        self.root.minsize(900, 600)
        self.root.configure(bg="#0f172a")

        # Store signals: name -> (indices, samples)
        self.signals_dict = {}
        self.canvas = None

        self.setup_styles()
        self.create_layout()

    # ================== STYLES ==================

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.bg = "#0f172a"
        self.panel = "#1e293b"
        self.card = "#273449"
        self.text = "#f1f5f9"
        self.muted = "#94a3b8"
        self.accent = "#2dd4bf"

        self.style.configure(
            "TFrame",
            background=self.bg
        )

        self.style.configure(
            "Panel.TFrame",
            background=self.panel
        )

        self.style.configure(
            "Header.TLabel",
            background=self.bg,
            foreground=self.text,
            font=("Segoe UI", 21, "bold")
        )

        self.style.configure(
            "SubHeader.TLabel",
            background=self.bg,
            foreground=self.muted,
            font=("Segoe UI", 9)
        )

        self.style.configure(
            "Section.TLabel",
            background=self.panel,
            foreground=self.accent,
            font=("Segoe UI", 10, "bold")
        )

        self.style.configure(
            "TCombobox",
            fieldbackground="#334155",
            background="#334155",
            foreground=self.text,
            arrowcolor=self.accent,
            bordercolor="#475569"
        )

        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", "#334155")],
            foreground=[("readonly", self.text)]
        )

        button_styles = {
            "Teal": "#0d9488",
            "Blue": "#2563eb",
            "Purple": "#7c3aed",
            "Red": "#dc2626"
        }

        for name, color in button_styles.items():
            self.style.configure(
                f"{name}.TButton",
                background=color,
                foreground="#ffffff",
                font=("Segoe UI", 9, "bold"),
                padding=8,
                borderwidth=0
            )

            self.style.map(
                f"{name}.TButton",
                background=[
                    ("active", color),
                    ("pressed", color)
                ]
            )

    # ================== LAYOUT ==================

    def create_layout(self):
        main = ttk.Frame(self.root)
        main.pack(
            fill=tk.BOTH,
            expand=True,
            padx=18,
            pady=15
        )

        # Header
        header = ttk.Frame(main)
        header.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(
            header,
            text="DSP STUDIO",
            style="Header.TLabel"
        ).pack(side=tk.LEFT)

        ttk.Label(
            header,
            text="DIGITAL SIGNAL PROCESSING WORKSPACE",
            style="SubHeader.TLabel"
        ).pack(side=tk.RIGHT, pady=12)

        # Main body
        body = ttk.Frame(main)
        body.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        sidebar = ttk.Frame(
            body,
            style="Panel.TFrame",
            width=285
        )
        sidebar.pack(
            side=tk.LEFT,
            fill=tk.Y,
            padx=(0, 15)
        )
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="CONTROL PANEL",
            bg=self.panel,
            fg=self.accent,
            font=("Segoe UI", 12, "bold")
        ).pack(fill=tk.X, pady=12)

        # Scrollable sidebar
        scroll_frame = tk.Frame(
            sidebar,
            bg=self.panel
        )
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        self.sidebar_canvas = tk.Canvas(
            scroll_frame,
            bg=self.panel,
            highlightthickness=0,
            width=265
        )

        scrollbar = ttk.Scrollbar(
            scroll_frame,
            orient=tk.VERTICAL,
            command=self.sidebar_canvas.yview
        )

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.sidebar_canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        self.sidebar_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.sidebar_content = tk.Frame(
            self.sidebar_canvas,
            bg=self.panel
        )

        self.sidebar_window = self.sidebar_canvas.create_window(
            (0, 0),
            window=self.sidebar_content,
            anchor="nw"
        )

        self.sidebar_content.bind(
            "<Configure>",
            lambda event: self.sidebar_canvas.configure(
                scrollregion=self.sidebar_canvas.bbox("all")
            )
        )

        self.sidebar_canvas.bind(
            "<Configure>",
            lambda event: self.sidebar_canvas.itemconfigure(
                self.sidebar_window,
                width=event.width
            )
        )

        self.sidebar_canvas.bind(
            "<Enter>",
            lambda event: self.sidebar_canvas.bind_all(
                "<MouseWheel>",
                self.on_mousewheel
            )
        )

        self.sidebar_canvas.bind(
            "<Leave>",
            lambda event: self.sidebar_canvas.unbind_all(
                "<MouseWheel>"
            )
        )

        # ---- Signal Management ----

        self.add_section("SIGNAL MANAGEMENT")

        ttk.Button(
            self.sidebar_content,
            text="+ Load Signal File (.txt)",
            style="Teal.TButton",
            command=self.load_signal_file
        ).pack(fill=tk.X, padx=10, pady=4)

        self.lbl_loaded_count = tk.Label(
            self.sidebar_content,
            text="Loaded Signals: 0",
            bg=self.panel,
            fg=self.muted,
            font=("Segoe UI", 9)
        )
        self.lbl_loaded_count.pack(
            anchor=tk.W,
            padx=12,
            pady=5
        )

        # ---- Single Signal ----

        self.add_section("SINGLE SIGNAL")

        self.combo_single = ttk.Combobox(
            self.sidebar_content,
            state="readonly"
        )
        self.combo_single.pack(
            fill=tk.X,
            padx=10,
            pady=4
        )

        ttk.Button(
            self.sidebar_content,
            text="Display Signal",
            style="Blue.TButton",
            command=self.action_display_single
        ).pack(fill=tk.X, padx=10, pady=4)

        # ---- Compare Signals ----

        self.add_section("COMPARE SIGNALS")

        self.combo_two_1 = ttk.Combobox(
            self.sidebar_content,
            state="readonly"
        )
        self.combo_two_1.pack(
            fill=tk.X,
            padx=10,
            pady=4
        )

        self.combo_two_2 = ttk.Combobox(
            self.sidebar_content,
            state="readonly"
        )
        self.combo_two_2.pack(
            fill=tk.X,
            padx=10,
            pady=4
        )

        ttk.Button(
            self.sidebar_content,
            text="Compare Signals",
            style="Blue.TButton",
            command=self.action_display_two
        ).pack(fill=tk.X, padx=10, pady=4)

        # ---- Arithmetic ----

        self.add_section("ARITHMETIC")

        ttk.Button(
            self.sidebar_content,
            text="Add All Loaded Signals",
            style="Teal.TButton",
            command=self.action_add
        ).pack(fill=tk.X, padx=10, pady=4)

        ttk.Button(
            self.sidebar_content,
            text="Subtract All Loaded Signals",
            style="Blue.TButton",
            command=self.action_subtract
        ).pack(fill=tk.X, padx=10, pady=4)

        ttk.Button(
            self.sidebar_content,
            text="Multiply by Constant",
            style="Purple.TButton",
            command=self.action_multiply
        ).pack(fill=tk.X, padx=10, pady=4)

        # ---- Signal Transformations ----

        self.add_section("SIGNAL TRANSFORMATIONS")

        ttk.Button(
            self.sidebar_content,
            text="Square Signal",
            style="Purple.TButton",
            command=self.action_square
        ).pack(fill=tk.X, padx=10, pady=4)

        ttk.Button(
            self.sidebar_content,
            text="Normalize Signal",
            style="Teal.TButton",
            command=self.action_normalize
        ).pack(fill=tk.X, padx=10, pady=4)

        ttk.Button(
            self.sidebar_content,
            text="Accumulation",
            style="Blue.TButton",
            command=self.action_accumulation
        ).pack(fill=tk.X, padx=10, pady=4)

        # Clear visualization
        ttk.Button(
            sidebar,
            text="Clear Visualization",
            style="Red.TButton",
            command=self.clear_canvas
        ).pack(fill=tk.X, padx=10, pady=10)

        # ---- Visualization Workspace ----

        workspace = ttk.Frame(
            body,
            style="Panel.TFrame",
            padding=15
        )
        workspace.pack(
            side=tk.RIGHT,
            fill=tk.BOTH,
            expand=True
        )

        ttk.Label(
            workspace,
            text="SIGNAL VISUALIZATION",
            background=self.panel,
            foreground=self.text,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor=tk.W, pady=(0, 4))

        ttk.Label(
            workspace,
            text="Load a signal or choose an operation to view its result.",
            background=self.panel,
            foreground=self.muted,
            font=("Segoe UI", 9)
        ).pack(anchor=tk.W, pady=(0, 12))

        self.plot_container = tk.Frame(
            workspace,
            bg="#ffffff"
        )
        self.plot_container.pack(
            fill=tk.BOTH,
            expand=True
        )

    def add_section(self, title):
        tk.Label(
            self.sidebar_content,
            text=title,
            bg=self.panel,
            fg=self.accent,
            font=("Segoe UI", 9, "bold"),
            anchor="w"
        ).pack(
            fill=tk.X,
            padx=12,
            pady=(15, 5)
        )

    def on_mousewheel(self, event):
        self.sidebar_canvas.yview_scroll(
            int(-event.delta / 120),
            "units"
        )

    # ================== HELPERS ==================

    def refresh_signal_lists(self):
        names = list(self.signals_dict.keys())

        self.combo_single["values"] = names
        self.combo_two_1["values"] = names
        self.combo_two_2["values"] = names

        self.lbl_loaded_count.config(
            text=f"Loaded Signals: {len(names)}"
        )

    def get_selected_signal(self):
        name = self.combo_single.get()

        if not name or name not in self.signals_dict:
            messagebox.showwarning(
                "Warning",
                "Please load and select a signal first!"
            )
            return None

        return name, self.signals_dict[name]

    def get_two_selected_signals(self):
        name1 = self.combo_two_1.get()
        name2 = self.combo_two_2.get()

        if (
            name1 not in self.signals_dict
            or name2 not in self.signals_dict
        ):
            messagebox.showwarning(
                "Warning",
                "Please select two valid signals!"
            )
            return None

        if name1 == name2:
            messagebox.showwarning(
                "Warning",
                "Please select two different signals!"
            )
            return None

        return name1, name2

    # ================== LOAD SIGNAL ==================

    def load_signal_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Signal File",
            filetypes=[("Text Files", "*.txt")]
        )

        if not file_path:
            return

        try:
            indices, samples = ReadSignalFileM(file_path)

            if not indices or not samples:
                messagebox.showerror(
                    "Error",
                    "The selected file contains no valid samples."
                )
                return

            filename = file_path.replace("\\", "/").split("/")[-1]
            name = filename
            counter = 2

            # Avoid replacing a signal with the same filename
            while name in self.signals_dict:
                name = f"{filename} ({counter})"
                counter += 1

            self.signals_dict[name] = (indices, samples)

            self.refresh_signal_lists()
            self.combo_single.set(name)

            names = list(self.signals_dict.keys())

            if len(names) >= 2:
                self.combo_two_1.set(names[-2])
                self.combo_two_2.set(names[-1])
            else:
                self.combo_two_1.set(name)
                self.combo_two_2.set("")

            self.plot_single(
                indices,
                samples,
                f"Signal: {name}"
            )

            messagebox.showinfo(
                "Success",
                f"Signal '{name}' loaded successfully!"
            )

        except Exception as error:
            messagebox.showerror(
                "Load Error",
                str(error)
            )

    # ================== TASK 1 ==================

    def action_display_single(self):
        selected = self.get_selected_signal()

        if selected is None:
            return

        name, (indices, samples) = selected

        self.plot_single(
            indices,
            samples,
            f"Signal: {name}"
        )

    def action_display_two(self):
        selected = self.get_two_selected_signals()

        if selected is None:
            return

        name1, name2 = selected

        idx1, samples1 = self.signals_dict[name1]
        idx2, samples2 = self.signals_dict[name2]

        self.plot_two(
            idx1, samples1, name1,
            idx2, samples2, name2
        )

    def action_add(self):
        if len(self.signals_dict) < 2:
            messagebox.showwarning(
                "Warning",
                "Load at least two signals first!"
            )
            return

        signals_data = list(self.signals_dict.values())

        try:
            # Pass every signal as a separate argument
            result_indices, result_samples = AddSignals(signals_data)

            self.plot_single(
                result_indices,
                result_samples,
                "Addition Result"
            )

        except Exception as error:
            messagebox.showerror(
                "Addition Error",
                str(error)
            )

    def action_subtract(self):
        if len(self.signals_dict) < 2:
            messagebox.showwarning(
                "Warning",
                "Load at least two signals first!"
            )
            return

        signals_data = list(self.signals_dict.values())

        try:
            # Subtract signals in loading order:
            # Signal1 - Signal2 - Signal3 - ...
            result_indices, result_samples = SubSignals(signals_data)

            self.plot_single(
                result_indices,
                result_samples,
                "Subtraction Result"
            )

        except Exception as error:
            messagebox.showerror(
                "Subtraction Error",
                str(error)
            )

    def action_multiply(self):
        selected = self.get_selected_signal()

        if selected is None:
            return

        name, (indices, samples) = selected

        constant = simpledialog.askfloat(
            "Multiply Constant",
            f"Enter the constant for '{name}':",
            parent=self.root
        )

        if constant is None:
            return

        try:
            result = MultiplySignal(samples, constant)

            self.plot_single(
                indices,
                result,
                f"{name} x {constant}"
            )

        except Exception as error:
            messagebox.showerror(
                "Multiplication Error",
                str(error)
            )

    # ================== TASK 2 ==================

    def action_square(self):
        selected = self.get_selected_signal()

        if selected is None:
            return

        name, (indices, samples) = selected

        try:
            result = SquaringSignal(samples)

            self.plot_single(
                indices,
                result,
                f"Squared: {name}"
            )

        except Exception as error:
            messagebox.showerror(
                "Squaring Error",
                str(error)
            )

    def action_normalize(self):
        selected = self.get_selected_signal()

        if selected is None:
            return

        name, (indices, samples) = selected

        target_range = simpledialog.askstring(
            "Normalization",
            "Enter normalization range:\n\n"
            "0_to_1\n"
            "-1_to_1",
            parent=self.root
        )

        if target_range is None:
            return

        target_range = target_range.strip()

        if target_range not in ("0_to_1", "-1_to_1"):
            messagebox.showerror(
                "Invalid Range",
                "Enter exactly 0_to_1 or -1_to_1."
            )
            return

        try:
            result = NormalizeSignal(samples, target_range)

            self.plot_single(
                indices,
                result,
                f"Normalized: {name}"
            )

        except Exception as error:
            messagebox.showerror(
                "Normalization Error",
                str(error)
            )

    def action_accumulation(self):
        selected = self.get_selected_signal()

        if selected is None:
            return

        name, (indices, samples) = selected

        try:
            result = AccumulationSignal(samples)

            self.plot_single(
                indices,
                result,
                f"Accumulation: {name}"
            )

        except Exception as error:
            messagebox.showerror(
                "Accumulation Error",
                str(error)
            )

    # ================== PLOTTING ==================

    def plot_single(self, indices, samples, title="Signal"):
        if len(indices) != len(samples):
            messagebox.showerror(
                "Plot Error",
                "Indices and samples must have the same length."
            )
            return

        self.clear_canvas()

        fig, (ax1, ax2) = plt.subplots(
            1, 2,
            figsize=(10, 5),
            dpi=100
        )

        fig.patch.set_facecolor("#ffffff")

        # Continuous representation
        ax1.plot(
            indices,
            samples,
            color="#0d9488",
            linewidth=1.8,
            marker="o",
            markersize=3
        )

        ax1.set_title(
            f"{title}\nContinuous Signal",
            color="#0f172a",
            fontsize=10,
            fontweight="bold"
        )

        ax1.set_xlabel("Index (n)", color="#475569")
        ax1.set_ylabel("Amplitude", color="#475569")
        ax1.tick_params(colors="#475569", labelsize=8)

        ax1.grid(
            True,
            linestyle="--",
            alpha=0.5,
            color="#cbd5e1"
        )

        ax1.set_facecolor("#f8fafc")

        # Discrete representation
        marker, stem, base = ax2.stem(
            indices,
            samples,
            linefmt="b-",
            markerfmt="bo",
            basefmt="k-"
        )

        plt.setp(marker, markersize=3, color="#2563eb")
        plt.setp(stem, linewidth=1, color="#2563eb")
        plt.setp(base, linewidth=0.8, color="#94a3b8")

        ax2.set_title(
            f"{title}\nDiscrete Signal",
            color="#0f172a",
            fontsize=10,
            fontweight="bold"
        )

        ax2.set_xlabel("Index (n)", color="#475569")
        ax2.set_ylabel("Amplitude", color="#475569")
        ax2.tick_params(colors="#475569", labelsize=8)

        ax2.grid(
            True,
            linestyle="--",
            alpha=0.5,
            color="#cbd5e1"
        )

        ax2.set_facecolor("#f8fafc")

        fig.tight_layout()
        self.render_canvas(fig)

    def plot_two(
        self,
        idx1, samples1, name1,
        idx2, samples2, name2
    ):
        self.clear_canvas()

        fig, ax = plt.subplots(
            figsize=(9, 5),
            dpi=100
        )

        fig.patch.set_facecolor("#ffffff")

        marker1, stem1, _ = ax.stem(
            idx1,
            samples1,
            linefmt="b-",
            markerfmt="bo",
            basefmt="k-",
            label=name1
        )

        plt.setp(marker1, markersize=3, color="#10641C")
        plt.setp(stem1, linewidth=1, color="#10641C")

        marker2, stem2, _ = ax.stem(
            idx2,
            samples2,
            linefmt="g-",
            markerfmt="go",
            basefmt="k-",
            label=name2
        )

        plt.setp(marker2, markersize=3, color="#183E79")
        plt.setp(stem2, linewidth=1, color="#183E79")

        ax.set_title(
            f"Comparing: {name1} vs {name2}",
            color="#0f172a",
            fontsize=11,
            fontweight="bold"
        )

        ax.set_xlabel("Index (n)", color="#475569")
        ax.set_ylabel("Amplitude", color="#475569")
        ax.tick_params(colors="#475569", labelsize=8)

        ax.legend(
            facecolor="#ffffff",
            edgecolor="#cbd5e1"
        )

        ax.grid(
            True,
            linestyle="--",
            alpha=0.5,
            color="#cbd5e1"
        )

        ax.set_facecolor("#f8fafc")

        fig.tight_layout()
        self.render_canvas(fig)

    def render_canvas(self, fig):
        self.canvas = FigureCanvasTkAgg(
            fig,
            master=self.plot_container
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

    def clear_canvas(self):
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        plt.close("all")


# ================== RUN APP ==================

if __name__ == "__main__":
    root = tk.Tk()
    app = LightDSPApp(root)
    root.mainloop()
