"""
investment_return_calculator.py
Professional Investment Return Calculator (Tkinter)
---------------------------------------------------
Features:
 - Calculates Simple Return, Annualized Return, and CAGR
 - Light/Dark Theme toggle
 - Matplotlib charts (Pie, Line, Bar)
 - Responsive / Resizable layout
 - CSV Export
 - Example Loader & Clear button
 - Works on Python 3.10 – 3.13 without errors
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import math

# --- Matplotlib Safe Import ---
try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from matplotlib.figure import Figure
    import numpy as np
    MPL_AVAILABLE = True
except Exception:
    MPL_AVAILABLE = False


# --- Helpers ---
def safe_float(s):
    try:
        return float(str(s).strip())
    except:
        return None


# --- Core Computation ---
def compute_returns():
    n = safe_float(ent_shares.get())
    bp = safe_float(ent_buy_price.get())
    bc = safe_float(ent_buy_comm.get())
    sp = safe_float(ent_sell_price.get())
    sc = safe_float(ent_sell_comm.get())
    dv = safe_float(ent_dividend.get())
    hp = safe_float(ent_holding.get())
    unit = holding_unit_var.get()

    # Validation
    missing = [name for name, val in [
        ("No. of shares", n), ("Purchase price", bp),
        ("Purchase commission", bc), ("Selling price", sp),
        ("Selling commission", sc), ("Dividend per share", dv),
        ("Holding period", hp)
    ] if val is None]
    if missing:
        messagebox.showerror("Input Error", "Please fill: " + ", ".join(missing))
        return
    if n <= 0 or bp < 0 or sp < 0 or hp <= 0:
        messagebox.showerror("Input Error", "Invalid numeric entries.")
        return

    years = hp / 12 if unit == "months" else hp
    months = hp if unit == "months" else hp * 12
    BV = n * bp + bc
    EV = n * sp - sc + n * dv

    if BV <= 0:
        messagebox.showerror("Error", "Beginning value cannot be zero.")
        return

    simple = (EV - BV) / BV
    annual = simple / months * 12 if months > 0 else 0
    cagr = (EV / BV) ** (1 / years) - 1 if years > 0 and EV > 0 and BV > 0 else 0

    lbl_bv.config(text=f"₹{BV:,.2f}")
    lbl_ev.config(text=f"₹{EV:,.2f}")
    lbl_simple.config(text=f"{simple*100:.2f}%")
    lbl_annual.config(text=f"{annual*100:.2f}%")
    lbl_cagr.config(text=f"{cagr*100:.2f}%")

    results = dict(
        BV=BV, EV=EV, n=n, bp=bp, sp=sp, bc=bc, sc=sc, dv=dv,
        months=months, years=years,
        simple=simple, annual=annual, cagr=cagr
    )
    if MPL_AVAILABLE:
        update_charts(results)


# --- Chart Rendering ---
def update_charts(r):
    for fig in [fig_pie, fig_line, fig_bar]:
        fig.clear()

    # PIE
    axp = fig_pie.add_subplot(111)
    labels = ["Beginning Value", "Profit" if r["EV"] >= r["BV"] else "Loss", "Dividends"]
    sizes = [r["BV"], abs(r["EV"] - r["BV"]), r["n"] * r["dv"]]
    axp.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    axp.set_title("Portfolio Breakdown")

    # LINE
    axl = fig_line.add_subplot(111)
    t = np.linspace(0, r["months"], 50)
    lin = r["BV"] + (r["EV"] - r["BV"]) * (t / r["months"])
    comp = r["BV"] * ((1 + r["cagr"]) ** (t / 12)) if r["cagr"] else lin
    axl.plot(t, lin, label="Linear")
    axl.plot(t, comp, label="Compound", linestyle="--")
    axl.set_title("Value Over Time")
    axl.legend()
    axl.grid(True, alpha=0.3)

    # BAR
    axb = fig_bar.add_subplot(111)
    lbls = ["Simple", "Annualized", "CAGR"]
    vals = [r["simple"] * 100, r["annual"] * 100, r["cagr"] * 100]
    axb.bar(lbls, vals)
    axb.set_title("Return Comparison")
    for i, v in enumerate(vals):
        axb.text(i, v, f"{v:.2f}%", ha="center", va="bottom")

    canvas_pie.draw()
    canvas_line.draw()
    canvas_bar.draw()


# --- CSV Export ---
def export_csv():
    if lbl_bv.cget("text") == "—":
        messagebox.showinfo("Nothing to export", "Please compute first.")
        return
    file = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if not file:
        return
    try:
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["BV", lbl_bv.cget("text")])
            writer.writerow(["EV", lbl_ev.cget("text")])
            writer.writerow(["Simple Return", lbl_simple.cget("text")])
            writer.writerow(["Annualized Return", lbl_annual.cget("text")])
            writer.writerow(["CAGR", lbl_cagr.cget("text")])
        messagebox.showinfo("Export Successful", f"Saved to:\n{file}")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))


# --- Utility ---
def load_example():
    ent_shares.delete(0, tk.END); ent_shares.insert(0, "150")
    ent_buy_price.delete(0, tk.END); ent_buy_price.insert(0, "25")
    ent_buy_comm.delete(0, tk.END); ent_buy_comm.insert(0, "20")
    ent_sell_price.delete(0, tk.END); ent_sell_price.insert(0, "30")
    ent_sell_comm.delete(0, tk.END); ent_sell_comm.insert(0, "20")
    ent_dividend.delete(0, tk.END); ent_dividend.insert(0, "1")
    ent_holding.delete(0, tk.END); ent_holding.insert(0, "15")
    holding_unit_var.set("months")
    compute_returns()


def clear_all():
    for e in [ent_shares, ent_buy_price, ent_buy_comm, ent_sell_price, ent_sell_comm, ent_dividend, ent_holding]:
        e.delete(0, tk.END)
    holding_unit_var.set("months")
    for l in [lbl_bv, lbl_ev, lbl_simple, lbl_annual, lbl_cagr]:
        l.config(text="—")
    if MPL_AVAILABLE:
        for fig in [fig_pie, fig_line, fig_bar]:
            fig.clear()
        for c in [canvas_pie, canvas_line, canvas_bar]:
            c.draw()


def toggle_theme():
    if theme_var.get() == "Light":
        style.theme_use("alt")
        theme_var.set("Dark")
    else:
        style.theme_use("clam")
        theme_var.set("Light")


# --- GUI Setup ---
root = tk.Tk()
root.title("Investment Return Calculator — Tkinter Edition")
root.geometry("1100x700")
root.minsize(900, 600)
style = ttk.Style(root)
style.theme_use("clam")

# --- Layout ---
main = ttk.Frame(root, padding=10)
main.pack(fill="both", expand=True)

left = ttk.Frame(main)
left.pack(side="left", fill="y", padx=(0, 10))

right = ttk.Frame(main)
right.pack(side="right", fill="both", expand=True)

# --- Inputs ---
ttk.Label(left, text="Inputs", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 6))

def add_input(label):
    ttk.Label(left, text=label).pack(anchor="w")
    ent = ttk.Entry(left, width=20)
    ent.pack(anchor="w", pady=(0, 4))
    return ent

ent_shares = add_input("No. of shares")
ent_buy_price = add_input("Purchase price/share (₹)")
ent_buy_comm = add_input("Purchase commission (₹)")
ent_sell_price = add_input("Selling price/share (₹)")
ent_sell_comm = add_input("Selling commission (₹)")
ent_dividend = add_input("Dividend/share (₹)")

ttk.Label(left, text="Holding period").pack(anchor="w")
ent_holding = ttk.Entry(left, width=10)
ent_holding.pack(side="left")
holding_unit_var = tk.StringVar(value="months")
ttk.OptionMenu(left, holding_unit_var, "months", "months", "years").pack(side="left", padx=4)

# Buttons
ttk.Button(left, text="Compute", command=compute_returns).pack(fill="x", pady=3)
ttk.Button(left, text="Load Example", command=load_example).pack(fill="x", pady=3)
ttk.Button(left, text="Clear", command=clear_all).pack(fill="x", pady=3)

# --- Results ---
ttk.Separator(left, orient="horizontal").pack(fill="x", pady=10)
ttk.Label(left, text="Results", font=("Segoe UI", 12, "bold")).pack(anchor="w")

def result_row(label):
    ttk.Label(left, text=label).pack(anchor="w")
    val = ttk.Label(left, text="—")
    val.pack(anchor="w", pady=(0, 3))
    return val

lbl_bv = result_row("Beginning Value (BV):")
lbl_ev = result_row("Ending Value (EV):")
lbl_simple = result_row("Simple Return:")
lbl_annual = result_row("Annualized Return:")
lbl_cagr = result_row("CAGR:")

# Export + Theme
theme_var = tk.StringVar(value="Light")
ttk.Button(left, text="Export CSV", command=export_csv).pack(fill="x", pady=4)
ttk.Button(left, text="Toggle Theme", command=toggle_theme).pack(fill="x")

# --- Charts ---
if MPL_AVAILABLE:
    nb = ttk.Notebook(right)
    nb.pack(fill="both", expand=True)

    tab1 = ttk.Frame(nb)
    tab2 = ttk.Frame(nb)
    tab3 = ttk.Frame(nb)
    nb.add(tab1, text="Breakdown (Pie)")
    nb.add(tab2, text="Growth (Line)")
    nb.add(tab3, text="Comparison (Bar)")

    fig_pie, fig_line, fig_bar = Figure(figsize=(4, 3), dpi=100), Figure(figsize=(5, 3), dpi=100), Figure(figsize=(4, 3), dpi=100)
    canvas_pie = FigureCanvasTkAgg(fig_pie, tab1)
    canvas_pie.get_tk_widget().pack(fill="both", expand=True)
    NavigationToolbar2Tk(canvas_pie, tab1).update()

    canvas_line = FigureCanvasTkAgg(fig_line, tab2)
    canvas_line.get_tk_widget().pack(fill="both", expand=True)
    NavigationToolbar2Tk(canvas_line, tab2).update()

    canvas_bar = FigureCanvasTkAgg(fig_bar, tab3)
    canvas_bar.get_tk_widget().pack(fill="both", expand=True)
    NavigationToolbar2Tk(canvas_bar, tab3).update()
else:
    ttk.Label(right, text="Matplotlib not available — charts disabled.", foreground="red").pack(fill="both", expand=True)

# --- Footer ---
ttk.Label(root, text="Formulas: Simple=(EV−BV)/BV, Annualized=Simple×(12/months), CAGR=(EV/BV)^(1/years)−1",
          font=("Segoe UI", 8), wraplength=900).pack(pady=(4, 6))

# Start clean
clear_all()
root.mainloop()
