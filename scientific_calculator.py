import streamlit as st
import math

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Casio fx-991EX • Scientific Calculator", page_icon="🧮", layout="centered")

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

# ---- SAFE STATE ACCESS ----
def get_expr():
    return st.session_state.expr

def set_expr(val):
    st.session_state.expr = val

# ---- MATH FUNCTIONS ----
def tsin(x): return math.sin(math.radians(x)) if st.session_state.mode=="DEG" else math.sin(x)
def tcos(x): return math.cos(math.radians(x)) if st.session_state.mode=="DEG" else math.cos(x)
def ttan(x): return math.tan(math.radians(x)) if st.session_state.mode=="DEG" else math.tan(x)
def nPr(n, r): return math.factorial(int(n)) // math.factorial(int(n) - int(r))
def nCr(n, r): return math.comb(int(n), int(r))

def evaluate_expression(expr):
    try:
        expr = expr.replace("×","*").replace("÷","/").replace("^","**").replace("%","/100")
        expr = expr.replace("√","math.sqrt").replace("π","math.pi").replace("e","math.e")
        expr = expr.replace("sin","tsin").replace("cos","tcos").replace("tan","ttan")
        expr = expr.replace("ln","math.log").replace("log","math.log10")
        expr = expr.replace("nPr","nPr").replace("nCr","nCr")
        expr = expr.replace("Ans", str(st.session_state.ans))
        result = eval(expr, {
            "math": math, "tsin": tsin, "tcos": tcos, "ttan": ttan,
            "nPr": nPr, "nCr": nCr
        })
        st.session_state.ans = result
        st.session_state.history.insert(0, (expr, result))
        set_expr(str(result))
    except Exception as e:
        st.error(f"Error: {e}")

# ---- CUSTOM CSS FOR CASIO LOOK ----
st.markdown("""
<style>
body {
    background-color: #1a1a1d;
}
h1 {
    text-align: center;
    color: #00ffaa;
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 1px;
}
.stTextInput>div>div>input {
    background-color: #2c2c34;
    color: #00ff99;
    font-family: 'Consolas', monospace;
    font-size: 22px;
    text-align: right;
    border-radius: 8px;
    border: 1px solid #444;
}
div[data-testid="stButton"] > button {
    background: linear-gradient(180deg, #444, #222);
    color: white;
    border: 1px solid #555;
    border-radius: 10px;
    font-weight: bold;
    font-size: 18px;
    transition: 0.1s;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(180deg, #00aaff, #005577);
    color: white;
}
.orange-btn button {
    background: linear-gradient(180deg, #ff9933, #cc6600) !important;
}
.blue-btn button {
    background: linear-gradient(180deg, #66b3ff, #0066cc) !important;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown("<h1>Casio fx-991EX Scientific Calculator</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([3,1])
with col1:
    st.text_input("Expression", key="expr", label_visibility="hidden")
with col2:
    if st.button(st.session_state.mode):
        st.session_state.mode = "RAD" if st.session_state.mode == "DEG" else "DEG"

st.caption(f"Memory: {round(st.session_state.memory,6)} | Ans: {round(st.session_state.ans,6)}")

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

def handle_button(label):
    expr = get_expr()
    if label == "AC": expr = ""
    elif label == "DEL": expr = expr[:-1]
    elif label == "=": evaluate_expression(expr); return
    elif label == "√": expr += "√("
    elif label == "x²": expr += "**2"
    elif label == "±": expr += "(-"
    elif label == "!": expr += "math.factorial("
    elif label == "M+": 
        try: st.session_state.memory += float(eval(expr or "0"))
        except: pass
    elif label == "M-": 
        try: st.session_state.memory -= float(eval(expr or "0"))
        except: pass
    elif label == "MR": expr += str(st.session_state.memory)
    elif label == "MC": st.session_state.memory = 0
    else: expr += label
    set_expr(expr)

# ---- DISPLAY BUTTONS ----
for row in rows:
    cols = st.columns(5)
    for i, label in enumerate(row):
        btn_class = "orange-btn" if label in ["AC","DEL"] else "blue-btn" if label in ["sin","cos","tan","ln","log"] else ""
        with cols[i]:
            st.markdown(f"<div class='{btn_class}'>", unsafe_allow_html=True)
            if st.button(label, use_container_width=True):
                handle_button(label)
            st.markdown("</div>", unsafe_allow_html=True)

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
- Casio fx-991EX inspired design 🎨  
- `DEG/RAD` toggle for trig  
- Functions: `sin`, `cos`, `tan`, `ln`, `log`, `√`, `x²`, `%`, `π`, `e`, `nCr`, `nPr`, `Ans`, factorial `!`  
- Memory: `M+`, `M-`, `MR`, `MC`  
- History (last 20 results)
""")
