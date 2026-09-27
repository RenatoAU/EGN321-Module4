import streamlit as st

from iteration import solve


st.set_page_config(page_title="Tank Diameter Sizing", layout="wide")
st.title("Cylindrical Tank Diameter Sizing")
st.write(
    "Find a tank's internal diameter for a target volume and fixed height. "
    "This tool is based on the Module 4 training workbook."
)
st.caption(
    "Volume = π × diameter² × height / 4. The program adjusts the diameter "
    "using a bounded search and checks the absolute volume error at each attempt."
)

st.subheader("Calculation inputs")
left, right = st.columns(2)

with left:
    target = st.number_input("Target volume (ft³)", value=100.0, step=1.0)
    tank_height = st.number_input("Tank height (ft)", value=5.0, step=0.5)
    initial_guess = st.number_input(
        "Starting diameter (ft)", value=3.0, step=0.5
    )

with right:
    tolerance = st.number_input(
        "Volume tolerance (ft³)",
        value=0.05,
        step=0.01,
        format="%.6f",
    )
    max_iterations = st.number_input(
        "Maximum iterations", value=50, step=1
    )

st.caption(
    "Inputs and tolerance must be positive. "
    "Maximum iterations must be at least 1."
)

if st.button("Run calculation", type="primary"):
    answer = solve(
        target=target,
        tank_height=tank_height,
        initial_guess=initial_guess,
        tolerance=tolerance,
        max_iterations=max_iterations,
    )

    st.subheader("Calculation result")
    status = answer["status"]

    if status == "converged":
        st.success("CONVERGED — the calculated volume is within tolerance.")
    elif status == "not_converged":
        st.warning(
            "NOT CONVERGED — no valid solution was found within the limits."
        )
    else:
        st.error("INVALID INPUT — " + answer["message"])

    col1, col2, col3 = st.columns(3)

    with col1:
        diameter = answer["solution"]
        st.metric(
            "Valid diameter",
            f"{diameter:.9g} ft" if diameter is not None else "None",
        )

    with col2:
        volume = answer["result"]
        st.metric(
            "Last calculated volume",
            f"{volume:.9g} ft³" if volume is not None else "—",
        )

    with col3:
        st.metric("Iterations performed", answer["iterations"])

    error = answer["error"]
    st.write(
        "**Final absolute volume error:** "
        + (f"{error:.9g} ft³" if error is not None else "Not available")
    )
    st.write(answer["message"])

    if answer["history"]:
        st.subheader("Iteration history")

        rows = [
            {
                "Iteration": item["iteration"],
                "Diameter guess (ft)": item["guess"],
                "Calculated volume (ft³)": item["result"],
                "Target volume (ft³)": item["target"],
                "Absolute error (ft³)": item["error"],
                "Lower bound (ft)": item["lower_bound"],
                "Upper bound (ft)": item["upper_bound"],
            }
            for item in answer["history"]
        ]

        st.dataframe(rows, hide_index=True)
    else:
        st.info("No iterations ran because the input was invalid.")
