import streamlit as st
import numpy as np
import plotly.graph_objs as go
from simulation.kinematics_1d import Kinematics1D
from simulation.kinematics_2d import Kinematics2D

st.set_page_config(page_title="Kinematics Simulator", layout="wide")

st.title('🚀 Professional Kinematics Simulator (1D & 2D with Animation)')

mode = st.radio("Choose Simulation Type:", ("1D Kinematics", "2D Kinematics"), horizontal=True)
st.markdown("---")

time_total = st.slider('Total Simulation Time (seconds)', min_value=1, max_value=20, value=5)
num_points = 200
time_points = np.linspace(0, time_total, num_points)

if mode == "1D Kinematics":
    col1, col2 = st.columns(2)
    with col1:
        st.header("1D Parameter Inputs")
        x0 = st.number_input('Initial Position x₀ (m)', value=0.0)
        v0 = st.number_input('Initial Velocity v₀ (m/s)', value=5.0)
        a = st.number_input('Acceleration a (m/s²)', value=0.0)
    with col2:
        st.write("#### Equation Used")
        st.latex("x = x_0 + v_0 t + \\frac{1}{2} a t^2")
        st.latex("v = v_0 + a t")
        
    kin1d = Kinematics1D(x0, v0, a)
    x = kin1d.position(time_points)
    v = kin1d.velocity(time_points)

    st.markdown("### 📈 Position & Velocity Graphs (Interactive)")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=time_points, y=x, mode='lines', name='Position x'))
    fig1.update_layout(title="Position vs Time (1D)", xaxis_title="Time (s)", yaxis_title="x (m)", margin=dict(l=40,r=40,b=40,t=40))
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(" ")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=time_points, y=v, mode='lines', name='Velocity v', line=dict(color='orange')))
    fig2.update_layout(title="Velocity vs Time (1D)", xaxis_title="Time (s)", yaxis_title="v (m/s)", margin=dict(l=40,r=40,b=40,t=40))
    st.plotly_chart(fig2, use_container_width=True)

elif mode == "2D Kinematics":
    col1, col2 = st.columns(2)
    with col1:
        st.header("2D Parameter Inputs")
        x0 = st.number_input('Initial X Position x₀ (m)', value=0.0)
        y0 = st.number_input('Initial Y Position y₀ (m)', value=0.0)
        vx0 = st.number_input('Initial Velocity vx₀ (m/s)', value=10.0)
        vy0 = st.number_input('Initial Velocity vy₀ (m/s)', value=15.0)
        ax = st.number_input('Acceleration ax (m/s²)', value=0.0)
        ay = st.number_input('Acceleration ay (m/s²)', value=-9.8)
    with col2:
        st.write("#### Equations Used")
        st.latex("x = x_0 + v_{x0} t + \\frac{1}{2} a_x t^2")
        st.latex("y = y_0 + v_{y0} t + \\frac{1}{2} a_y t^2")
        st.latex("v_x = v_{x0} + a_x t")
        st.latex("v_y = v_{y0} + a_y t")

    kin2d = Kinematics2D(x0, y0, vx0, vy0, ax, ay)
    x, y = kin2d.position(time_points)
    vx, vy = kin2d.velocity(time_points)

    st.markdown("### 🎬 Animated Trajectory Visualization")

    # Animation slider
    t_slider = st.slider("Show Trajectory up to Time (seconds)", 0.0, float(time_total), float(time_total), step=0.1)
    mask = time_points <= t_slider
    trace = go.Scatter(x=x[mask], y=y[mask], mode='lines+markers', marker_color='blue', name="Trajectory")
    current_point = go.Scatter(x=[x[mask][-1]], y=[y[mask][-1]], mode='markers', marker=dict(size=12, color='red'), name="Current Position")
    layout = go.Layout(
        title="Object Trajectory (X vs Y)",
        xaxis_title="X Position (m)",
        yaxis_title="Y Position (m)",
        showlegend=False,
        width=800, height=400,
        margin=dict(l=40, r=40, b=40, t=40),
        yaxis=dict(scaleanchor="x", scaleratio=1)
    )
    fig_traj = go.Figure([trace, current_point], layout)
    st.plotly_chart(fig_traj, use_container_width=True)
    st.markdown(" ")

    st.markdown("### 📈 Position and Velocity Graphs (Interactive)")
    fig_pos = go.Figure()
    fig_pos.add_trace(go.Scatter(x=time_points, y=x, name='X Position'))
    fig_pos.add_trace(go.Scatter(x=time_points, y=y, name='Y Position'))
    fig_pos.update_layout(title="Position vs Time (2D)", xaxis_title="Time (s)", yaxis_title="Position (m)", margin=dict(l=40,r=40,b=40,t=40))
    st.plotly_chart(fig_pos, use_container_width=True)

    fig_vel = go.Figure()
    fig_vel.add_trace(go.Scatter(x=time_points, y=vx, name='Vx'))
    fig_vel.add_trace(go.Scatter(x=time_points, y=vy, name='Vy'))
    fig_vel.update_layout(title="Velocity vs Time (2D)", xaxis_title="Time (s)", yaxis_title="Velocity (m/s)", margin=dict(l=40,r=40,b=40,t=40))
    st.plotly_chart(fig_vel, use_container_width=True)

st.info("✨ All graphs are interactive: Zoom, pan and hover for details. Adjust parameters or use the time slider to animate the motion in 2D mode.")

st.markdown("---")
st.markdown("**Pro Tip:** When you finish, you can deploy this app to [Streamlit Community Cloud](https://share.streamlit.io/) and share the link with anyone—no setup needed on their system!")

