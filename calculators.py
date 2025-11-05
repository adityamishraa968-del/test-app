import tkinter as tk
from tkinter import ttk, messagebox
import math

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Casio fx-991 • Scientific Calculator")
        self.geometry("420x620")
        self.resizable(False, False)
        self.configure(bg="#1b1f23")

        self.expression = tk.StringVar(value="")
        self.mode = "DEG"
        self.memory = 0
        self.ans = 0

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 12), padding=6)
        style.configure("Disp.TLabel", background="#1b1f23", foreground="#00ff99", font=("Consolas", 18))

        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")

        info = ttk.Frame(top)
        info.pack(fill="x")
        self.mode_label = ttk.Label(info, text=f"{self.mode}", foreground="#aaa")
        self.mode_label.pack(side="left")
        self.mem_label = ttk.Label(info, text=f"M:{self.memory}", foreground="#aaa")
        self.mem_label.pack(side="right")

        disp = ttk.Label(top, textvariable=self.expression, style="Disp.TLabel", anchor="e")
        disp.pack(fill="x", ipady=18)

        grid = ttk.Frame(self, padding=8)
        grid.pack(expand=True, fill="both")

        buttons = [
            ["AC","DEL","(",")","%"],
            ["sin","cos","tan","ln","log"],
            ["7","8","9","÷","√"],
            ["4","5","6","×","x²"],
            ["1","2","3","-","^"],
            ["0",".","+/-","+","="],
            ["π","e","M+","M-","MR"],
            ["MC","RAD/DEG","Ans","nCr","nPr"]
        ]

        for row in buttons:
            fr = ttk.Frame(grid)
            fr.pack(fill="x", pady=3)
            for label in row:
                b = ttk.Button(fr, text=label, command=lambda t=label: self.click(t))
                b.pack(side="left", expand=True, fill="x", padx=3)

    # ---------- Logic ----------
    def click(self, key):
        if key == "AC":
            self.expression.set("")
        elif key == "DEL":
            self.expression.set(self.expression.get()[:-1])
        elif key == "=":
            self.calculate()
        elif key == "RAD/DEG":
            self.toggle_mode()
        elif key == "√":
            self.append("sqrt(")
        elif key == "x²":
            self.append("**2")
        elif key == "+/-":
            self.append("(-")
        elif key == "π":
            self.append(str(math.pi))
        elif key == "e":
            self.append(str(math.e))
        elif key == "M+":
            self.memory_add()
        elif key == "M-":
            self.memory_sub()
        elif key == "MR":
            self.append(str(self.memory))
        elif key == "MC":
            self.memory_clear()
        elif key == "Ans":
            self.append(str(self.ans))
        elif key in ("sin","cos","tan","ln","log","nCr","nPr"):
            self.append(f"{key}(")
        else:
            self.append(key)

    def append(self, value):
        self.expression.set(self.expression.get() + value)

    def toggle_mode(self):
        self.mode = "RAD" if self.mode == "DEG" else "DEG"
        self.mode_label.config(text=self.mode)

    def calculate(self):
        try:
            expr = self.expression.get()
            expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**").replace("%", "/100")
            expr = expr.replace("√", "math.sqrt")
            result = self.safe_eval(expr)
            self.ans = result
            self.expression.set(str(result))
            self.mem_label.config(text=f"M:{self.memory}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def memory_add(self):
        try:
            val = float(eval(self.expression.get() or "0"))
            self.memory += val
            self.mem_label.config(text=f"M:{self.memory}")
        except:
            pass

    def memory_sub(self):
        try:
            val = float(eval(self.expression.get() or "0"))
            self.memory -= val
            self.mem_label.config(text=f"M:{self.memory}")
        except:
            pass

    def memory_clear(self):
        self.memory = 0
        self.mem_label.config(text=f"M:{self.memory}")

    def safe_eval(self, expr):
        expr = expr.replace("sin", "self.trig_sin")
        expr = expr.replace("cos", "self.trig_cos")
        expr = expr.replace("tan", "self.trig_tan")
        expr = expr.replace("ln", "math.log")
        expr = expr.replace("log", "math.log10")
        expr = expr.replace("nCr", "math.comb")
        expr = expr.replace("nPr", "self.nPr")
        return eval(expr, {"math": math, "self": self})

    def trig_sin(self, x):
        return math.sin(math.radians(x)) if self.mode == "DEG" else math.sin(x)
    def trig_cos(self, x):
        return math.cos(math.radians(x)) if self.mode == "DEG" else math.cos(x)
    def trig_tan(self, x):
        return math.tan(math.radians(x)) if self.mode == "DEG" else math.tan(x)
    def nPr(self, n, r):
        return math.factorial(int(n)) // math.factorial(int(n) - int(r))

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()
