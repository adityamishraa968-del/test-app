import streamlit as st
import math
import operator

# --- Helper: Safe evaluation environment ---
SAFE_DICT = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
# Add commonly used names
SAFE_DICT.update({
    'pi': math.pi,
    'e': math.e,
    'sqrt': math.sqrt,
    'ln': math.log,
    'log': lambda x, base=10: math.log(x, base),
    'fact': math.factorial,
    'factorial': math.factorial,
    'abs': abs,
    'pow': pow,
})

# basic operators allowed via eval string (Python operators are used)

# --- App UI and logic ---
st.set_page_config(page_title="Casio-like Scientific Calculator", layout="wide")

st.markdown("# Casio fx‑991 style — Scientific Calculator")
st.markdown("A Streamlit app that mimics a Casio fx‑991 style scientific calculator. Use the buttons or your keyboard to build expressions."
            )

# initialize session state
if 'expr' not in st.session_state:
    st.session_state.expr = ''
if 'ans' not in st.session_state:
    st.session_state.ans = ''
if 'mode' not in st.session_state:
    st.session_state.mode = 'DEG'  # or 'RAD'
if 'history' not in st.session_state:
    st.session_state.history = []

# Display panel
with st.container():
    st.subheader(f"Mode: {st.session_state.mode}")
    display_col, keypad_col = st.columns([2, 5])

    with display_col:
        st.text_area("Expression", value=st.session_state.expr, height=60, key='display_expr', disabled=True))
        st.markdown("**Result:**")
        st.write(st.session_state.ans)

        # History
        if st.button("Clear History"):
            st.session_state.history = []
        if st.session_state.history:
            st.markdown("**History (last 10)**")
            for item in st.session_state.history[-10:][::-1]:
                st.write(item)

    with keypad_col:
        # layout rows of buttons mimicking a scientific calculator
        def btn(label, key=None, append=True):
            if st.button(label, key=key or label):
                if label == 'C':
                    st.session_state.expr = ''
                elif label == 'DEL':
                    st.session_state.expr = st.session_state.expr[:-1]
                elif label == 'Ans':
                    st.session_state.expr += str(st.session_state.ans)
                elif label == 'Mode':
                    st.session_state.mode = 'RAD' if st.session_state.mode == 'DEG' else 'DEG'
                elif label == '=':
                    # evaluate
                    expr = st.session_state.expr.replace('^', '**')
                    try:
                        # handle degree/radian conversions for trig if needed
                        safe_locals = SAFE_DICT.copy()
                        if st.session_state.mode == 'DEG':
                            # wrap sin/cos/tan to convert degrees -> radians
                            safe_locals.update({
                                'sin': lambda x: math.sin(math.radians(x)),
                                'cos': lambda x: math.cos(math.radians(x)),
                                'tan': lambda x: math.tan(math.radians(x)),
                                'asin': lambda x: math.degrees(math.asin(x)),
                                'acos': lambda x: math.degrees(math.acos(x)),
                                'atan': lambda x: math.degrees(math.atan(x)),
                            })
                        else:
                            safe_locals.update({
                                'sin': math.sin,
                                'cos': math.cos,
                                'tan': math.tan,
                                'asin': math.asin,
                                'acos': math.acos,
                                'atan': math.atan,
                            })

                        # allow usage of percent symbol as /100
                        expr = expr.replace('%', '/100')

                        result = eval(expr, {"__builtins__": None}, safe_locals)
                        # format large floats
                        if isinstance(result, float):
                            if result.is_integer():
                                result = int(result)
                            else:
                                result = round(result, 12)
                        st.session_state.ans = result
                        st.session_state.history.append(f"{st.session_state.expr} = {result}")
                    except Exception as e:
                        st.session_state.ans = f"Error: {e}"
                else:
                    # append the label text (for e.g. 'sin(', '(', etc.)
                    if append:
                        st.session_state.expr += label
                    else:
                        # special behaviors
                        pass

        # Row 1
        r1 = st.columns([1,1,1,1,1,1])
        with r1[0]: btn('MODE', key='mode_btn')
        with r1[1]: btn('SHIFT', key='shift')
        with r1[2]: btn('ALPHA', key='alpha')
        with r1[3]: btn('(', key='(')
        with r1[4]: btn(')', key=')')
        with r1[5]: btn('DEL', key='del')

        # Row 2
        r2 = st.columns([1,1,1,1,1,1])
        with r2[0]: btn('sin(', key='sin')
        with r2[1]: btn('cos(', key='cos')
        with r2[2]: btn('tan(', key='tan')
        with r2[3]: btn('^', key='pow')
        with r2[4]: btn('sqrt(', key='sqrt')
        with r2[5]: btn('C', key='C')

        # Row 3
        r3 = st.columns([1,1,1,1,1,1])
        with r3[0]: btn('ln(', key='ln')
        with r3[1]: btn('log(', key='log')
        with r3[2]: btn('e', key='e')
        with r3[3]: btn('pi', key='pi')
        with r3[4]: btn('!', key='factorial')
        with r3[5]: btn('%', key='percent')

        # Row 4
        r4 = st.columns([1,1,1,1,1,1])
        with r4[0]: btn('7')
        with r4[1]: btn('8')
        with r4[2]: btn('9')
        with r4[3]: btn('/', key='div')
        with r4[4]: btn('Ans', key='ans')
        with r4[5]: btn('Mode', key='mode_toggle')

        # Row 5
        r5 = st.columns([1,1,1,1,1,1])
        with r5[0]: btn('4')
        with r5[1]: btn('5')
        with r5[2]: btn('6')
        with r5[3]: btn('*', key='mul')
        with r5[4]: btn('pi', key='pi2')
        with r5[5]: btn('EXP', key='exp')

        # Row 6
        r6 = st.columns([1,1,1,1,1,1])
        with r6[0]: btn('1')
        with r6[1]: btn('2')
        with r6[2]: btn('3')
        with r6[3]: btn('-', key='sub')
        with r6[4]: btn('0')
        with r6[5]: btn('.', key='dot')

        # Row 7
        r7 = st.columns([1,1,1,1,1,1])
        with r7[0]: btn('+/-', key='sign')
        with r7[1]: btn('0', key='zero')
        with r7[2]: btn('Ans', key='ans2')
        with r7[3]: btn('+', key='add')
        with r7[4]: btn('=', key='equals')
        with r7[5]: btn('C', key='c2')

        # Extra small controls
        st.markdown("---")
        colA, colB, colC = st.columns(3)
        with colA:
            if st.button('Deg/Rad'):
                st.session_state.mode = 'RAD' if st.session_state.mode == 'DEG' else 'DEG'
        with colB:
            if st.button('Copy Result'):
                st.write('Result copied to clipboard — use your browser copy.')
        with colC:
            if st.button('Clear'):
                st.session_state.expr = ''
                st.session_state.ans = ''

st.markdown('---')
st.markdown("""**Notes:**
- Use `^` for power (e.g., `2^3`) — the app converts it to Python `**`.
- Trig functions respect the selected mode (DEG/RAD).
- You can use `fact(5)` or `factorial(5)` for factorial.
- Use `%` to represent percent (e.g., `50%` becomes `50/100`).
""")

# EOF
