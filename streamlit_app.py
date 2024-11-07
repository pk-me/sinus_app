# Streamlit app for interactive sine wave visualization with arc length calculation
import streamlit as st
import numpy as np
from scipy.integrate import quad
import plotly.graph_objs as go

# Title and description
st.title("Sine Wave Arc Length Calculator")
st.write(
    "This app calculates the arc length of a sine wave over a given interval and displays the wave interactively."
)

# Input parameters
A = st.sidebar.slider(
    "Amplitude (A) in µm", min_value=0.1, max_value=2.0, value=1.0, step=0.1
)
lamb = st.sidebar.slider(
    "Period (λ) in µm", min_value=1.0, max_value=10.0, value=2.0, step=0.1
)


#a = 0  # st.sidebar.slider("Start of Interval (a) in µm", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
#b = 1  # st.sidebar.slider("End of Interval (b) in µm", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
a = st.sidebar.number_input("Start of Interval (a) in µm", value=0.0)
b = st.sidebar.number_input("End of Interval (b) in µm", value=1.0)

# Define sine wave function
def sine_wave(x, A, lamb):
    return A/2 * np.sin(2*np.pi*x/lamb)


# Function to calculate arc length
def sine_wave_arc_length(A, lamb, a, b):
    def arc_length(x):
        return np.sqrt(1 + (np.pi * A * np.cos(2 * np.pi * x / lamb) / lamb) ** 2)

    arc_length_value, _ = quad(arc_length, a, b)
    return arc_length_value


# Generate x and y values
x_values = np.linspace(0, 2 * lamb, 500)
y_values = sine_wave(x_values, A, lamb)

# Plot sine wave using Plotly for interactivity
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=x_values, y=y_values, mode="lines", name="Sine Wave", line=dict(color="red")
    )
)
fig.update_layout(
    title="Sine Wave", xaxis_title="x (µm)", yaxis_title="y (µm)", showlegend=True
)

# Display the Plotly plot
st.plotly_chart(fig)

# Calculate arc length and display it
arc_length_value = sine_wave_arc_length(A, lamb, a, b)
flat_line_length = b - a
arc_length_ratio = arc_length_value * lamb / flat_line_length
linear_approx = 2 * np.sqrt(A**2 + lamb**2 / 4)

st.write(f"**Arc Length of Interval [{a}, {b}]:** {arc_length_value:.3f} µm")
st.write(f"**Ratio of Arc Length to Flat Line:** {arc_length_ratio:.3f}")
st.write(f"**Linear Approximation of Arc Length:** {linear_approx:.3f} µm")
