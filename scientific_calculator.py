import streamlit as st
import math

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Casio fx-991EX • Scientific Calculator", page_icon="🧮", layout="centered")

# ---- SAFE SESSION INIT ----
expr = st.session_state.get("expr", "")
mode = st.session_state.get("mode", "DEG")
memory = st.session_state.get("memory", 0.0)
ans = st.session_state.get("ans", 0.0)
history = st.session_state.get("history", [])

# ---- MATH FUNCTIONS ----
def tsin(x): return math.sin(math.radians(x)) if mode == "DEG" else math.sin(x)
def tcos(x): return math.cos(math.radians(x)) if mode == "DEG" else math.cos(x)
def ttan(x): return math.tan(math.radians(x)) if mode == "DEG" else math.tan(x)
def nPr(n, r): return math.factorial(int(n)) // math.factorial(int(n) - int(r))
def nCr(n, r): return math.comb(int(n), int(r))

# ---- CALCULATE ----
def evaluate_expression(expr):
    try:
        expr = expr.replace("×","*").replace("÷","/").replace("^","**").replace("%","/100")
        expr = expr.replace("√","math.sqrt").replace("π","math.pi").replace("e","math.e")
        expr = expr.replace("sin","tsin").replace("cos","tcos").replace("tan","ttan")
        expr = expr.replace("ln","math.log").replace("log","math.log10")
        expr = expr.replace("nPr","nPr").replace("nCr","nCr")
        expr = expr.replace("Ans", str(ans))
        result = eval(expr, {
            "math": math, "tsin": tsin, "tcos": tcos, "ttan": ttan, "nPr": nPr, "nCr": nCr
        })
        return result
    except Exception as e:
        st.error(f"Error: {e}")
        return expr

# ---- UI HEADER ----
st.markdown("<h1 style='text-align:center;color:#00ffaa;'>Casio fx-991EX Scientific Calculator</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([3,1])
with col1:
    new_expr = st.text_input("Expression", expr, label_visibility="hidden")
with col2:
    if st.button(mode):
        mode = "RAD" if mode == "DEG" else "DEG"

st.caption(f"Memory: {round(memory,6)} | Ans: {round(ans,6)}")

# ---- BUTTON GRID ----
rows = [
    ["AC","DEL","(",")","%"],
    ["sin","cos","tan","ln","log"],
    ["7","8","9","÷","√"],
    ["4","5","6","×","-"],
    ["1","2","3","+","="],
    ["0",".","Ans","π","e"],
    ["M+","M-","MR","MC","±"],
    ["nCr","nPr","x²","^","!"]
]

# ---- BUTTON LOGIC ----
def process_input(label, expr, memory, ans, history):
    if label == "AC": expr = ""
    elif label == "DEL": expr = expr[:-1]
    elif label == "=":
        result = evaluate_expression(expr)
        if isinstance(result, (int, float)):
            ans = result
            history.insert(0, (expr, result))
            expr = str(result)
    elif label == "√": expr += "√("
    elif label == "x²": expr += "**2"
    elif label == "±": expr += "(-"
    elif label == "!": expr += "math.factorial("
    elif label == "M+": 
        try: memory += float(eval(expr or "0"))
        except: pass
    elif label == "M-":
        try: memory -= float(eval(expr or "0"))
        except: pass
    elif label == "MR": expr += str(memory)
    elif label == "MC": memory = 0
    else: expr += label
    return expr, memory, ans, history

# ---- DISPLAY BUTTONS ----
for row in rows:
    cols = st.columns(5)
    for i, label in enumerate(row):
        if cols[i].button(label, use_container_width=True):
            expr, memory, ans, history = process_input(label, expr, memory, ans, history)
            st.session_state.expr = expr
            st.session_state.memory = memory
            st.session_state.ans = ans
            st.session_state.history = history
            st.session_state.mode = mode
            st.rerun()

# ---- HISTORY ----
with st.expander("🧾 History"):
    if not history:
        st.write("No calculations yet.")
    else:
        for e, r in history[:20]:
            st.code(f"{e} = {r}")

# 🟢 Features section removed completely
