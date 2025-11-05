import streamlit as st
import math

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Casio fx-991 • Scientific Calculator", page_icon="🧮", layout="centered")

# ---- SESSION STATE ----
if "expr" not in st.session_state:
    st.session_state.expr = ""
if "mode" not in st.session_state:
    st.session_state.mode = "DEG"
if "memory" not in st.session_state:
    st.session_state.memory = 0.0
if "ans" not in st.session_state:
    st.session_state.ans = 0.0
if "history" not in st.session_state:
    st.session_state.history = []

# ---- FUNCTIONS ----
def append(value): 
    st.session_state.expr += value

def clear(): 
    st.session_state.expr = ""

def delete(): 
    st.session_state.expr = st.session_state.expr[:-1]

def tsin(x): 
    return math.sin(math.radians(x)) if st.session_state.mode=="DEG" else math.sin(x)

def tcos(x): 
    return math.cos(math.radians(x)) if st.session_state.mode=="DEG" else math.cos(x)

def ttan(x): 
    return math.tan(math.radians(x)) if st.session_state.mode=="DEG" else math.tan(x)

def nPr(n, r): 
    return math.factorial(int(n)) // math.factorial(int(n) - int(r))

def nCr(n, r): 
    return math.comb(int(n), int(r))

def evaluate_expression(expr: str):
    try:
        expr = expr.replace("×","*").replace("÷","/").replace("^","**").replace("%","/100")
        expr = expr.replace("√","math.sqrt").replace("π","math.pi").replace("e","math.e")
        expr = expr.replace("sin","tsin").replace("cos","tcos").replace("tan","ttan")
        expr = expr.replace("ln","math.log").replace("log","math.log10")
        expr = expr.replace("nPr","nPr").replace("nCr","nCr")
        expr = expr.replace("Ans", str(st.session_state.ans))
        result = eval(expr, {"math": math, "tsin": tsin, "tcos": tcos, "ttan": ttan, "nPr": nPr, "nCr": nCr})
        st.session_state.ans = result
        st.session_state.history.insert(0, (st.session_state.expr, result))
        st.session_state.expr = str(result)
    except Exception as e:
        st.error(f"Error: {e}")

# ---- HEADER ----
st.title("🧮 Casio fx-991 Style Scientific Calculator")

col1, col2 = st.columns([3,1])
with col1:
    st.text_input("Expression", key="expr", label_visibility="hidden")
with col2:
    if st.button(st.session_state.mode):
        st.session_state.mode = "RAD" if st.session_state.mode == "DEG" else "DEG"

st.caption(f"Memory: {round(st.session_state.memory,6)} | Ans: {round(st.session_state.ans,6)}")

# ---- BUTTON LAYOUT ----
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

# ---- BUTTON ACTIONS ----
def handle_button(label):
    if label == "AC":
        clear()
    elif label == "DEL":
        delete()
    elif label == "=":
        evaluate_expression(st.session_state.expr)
    elif label == "√":
        append("√(")
    elif label == "x²":
        append("**2")
    elif label == "±":
        append("(-")
    elif label == "!":
        append("math.factorial(")
    elif label == "M+":
        try:
            st.session_state.memory += float(eval(st.session_state.expr or "0"))
        except:
            pass
    elif label == "M-":
        try:
            st.session_state.memory -= float(eval(st.session_state.expr or "0"))
        except:
            pass
    elif label == "MR":
        append(str(st.session_state.memory))
    elif label == "MC":
        st.session_state.memory = 0
    else:
        append(label)

# ---- BUTTON GRID ----
for row in rows:
    cols = st.columns(5)
    for i, label in enumerate(row):
        if cols[i].button(label, use_container_width=True):
            handle_button(label)
            st.experimental_rerun()  # ✅ safer rerun than st.rerun()

# ---- HISTORY ----
with st.expander("🧾 History"):
    if not st.session_state.history:
        st.write("No calculations yet.")
    else:
        for expr, res in st.session_state.history[:20]:
            st.code(f"{expr} = {res}")

st.markdown("---")
st.markdown("""
**Features:**
- Fully browser-based (no Tkinter)
- `DEG/RAD` mode switch  
- Trig: `sin`, `cos`, `tan`, `ln`, `log`, `√`, `x²`, `%`, `π`, `e`, `!`, `nCr`, `nPr`, `Ans`  
- Memory keys: `M+`, `M-`, `MR`, `MC`  
- History (last 20 results)
""")
