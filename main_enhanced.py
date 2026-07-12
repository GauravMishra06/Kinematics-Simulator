import streamlit as st
import numpy as np
import plotly.graph_objs as go
from simulation.kinematics_1d import Kinematics1D
from simulation.kinematics_2d import Kinematics2D
from visualization import AnimatedPlotter, MetricsCalculator, InteractiveWidgets, DataExporter

# Page configuration
st.set_page_config(
    page_title="Advanced Kinematics Simulator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🚀 Advanced Kinematics Simulator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Interactive Physics Simulation with Real-time Visualization & Analysis</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.markdown("## ⚙️ Simulation Settings")
    
    mode = st.radio("**Simulation Mode:**", ("1D Kinematics", "2D Kinematics"), horizontal=False)
    
    st.markdown("---")
    
    # Advanced settings
    settings = InteractiveWidgets.create_advanced_controls()
    
    st.markdown("---")
    
    # Help section
    InteractiveWidgets.create_help_section()
    
    # Unit converter
    InteractiveWidgets.create_unit_converter()

# Main content area
time_total = st.slider('⏱️ Total Simulation Time (seconds)', min_value=1, max_value=30, value=10)
num_points = 300
time_points = np.linspace(0, time_total, num_points)

# Create plotter instance
plotter = AnimatedPlotter(dark_mode=settings['dark_mode'])

st.markdown("---")

# ==================== 1D KINEMATICS MODE ====================
if mode == "1D Kinematics":
    st.markdown("## 📏 1D Kinematics Simulation")
    
    # Preset selector
    preset_name, preset_values = InteractiveWidgets.create_preset_selector(mode='1d')
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎛️ Input Parameters")
        
        if preset_values:
            x0 = st.number_input('Initial Position x₀ (m)', value=preset_values['x0'], format="%.2f")
            v0 = st.number_input('Initial Velocity v₀ (m/s)', value=preset_values['v0'], format="%.2f")
            a = st.number_input('Acceleration a (m/s²)', value=preset_values['a'], format="%.2f")
        else:
            x0 = st.number_input('Initial Position x₀ (m)', value=0.0, format="%.2f")
            v0 = st.number_input('Initial Velocity v₀ (m/s)', value=10.0, format="%.2f")
            a = st.number_input('Acceleration a (m/s²)', value=-2.0, format="%.2f")
    
    with col2:
        st.markdown("### 📐 Governing Equations")
        st.latex(r"x(t) = x_0 + v_0 t + \frac{1}{2} a t^2")
        st.latex(r"v(t) = v_0 + a t")
        st.latex(r"a(t) = \text{constant}")
    
    # Physics insights
    InteractiveWidgets.create_physics_insights(mode='1d', a=a, v0=v0, x0=x0)
    
    # Calculate kinematics
    kin1d = Kinematics1D(x0, v0, a)
    x = kin1d.position(time_points)
    v = kin1d.velocity(time_points)
    
    # Calculate metrics
    metrics = MetricsCalculator.calculate_1d_metrics(time_points, x, v, a)
    
    st.markdown("---")
    
    # Visualization tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Standard Plots", "🎬 Animated View", "🔄 Phase Space", 
                                             "📊 Metrics", "💾 Export Data"])
    
    with tab1:
        st.markdown("### Position vs Time")
        fig_pos = go.Figure()
        fig_pos.add_trace(go.Scatter(
            x=time_points, y=x, mode='lines',
            line=dict(color='#667eea', width=3),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.2)',
            name='Position'
        ))
        fig_pos.update_layout(
            xaxis_title="Time (s)",
            yaxis_title="Position (m)",
            template=plotter.template,
            hovermode='x unified'
        )
        st.plotly_chart(fig_pos, use_container_width=True)
        
        st.markdown("### Velocity vs Time")
        fig_vel = go.Figure()
        fig_vel.add_trace(go.Scatter(
            x=time_points, y=v, mode='lines',
            line=dict(color='#f093fb', width=3),
            fill='tozeroy',
            fillcolor='rgba(240, 147, 251, 0.2)',
            name='Velocity'
        ))
        fig_vel.update_layout(
            xaxis_title="Time (s)",
            yaxis_title="Velocity (m/s)",
            template=plotter.template,
            hovermode='x unified'
        )
        st.plotly_chart(fig_vel, use_container_width=True)
    
    with tab2:
        st.markdown("### 🎬 Animated Motion")
        anim_fig = plotter.create_animated_1d_trajectory(
            time_points, x, v,
            particle_size=settings['marker_size']
        )
        st.plotly_chart(anim_fig, use_container_width=True)
        st.info("💡 Click 'Play' to see the motion animate with velocity color mapping!")
    
    with tab3:
        st.markdown("### 🔄 Phase Space Diagram")
        phase_fig = plotter.create_phase_space_plot(x, v, time_points)
        st.plotly_chart(phase_fig, use_container_width=True)
        st.info("📍 Phase space shows the relationship between position and velocity over time")
    
    with tab4:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Max Position", f"{metrics['max_position']:.2f} m", delta=f"{metrics['total_displacement']:.2f} m")
        with col2:
            st.metric("Max Velocity", f"{metrics['max_velocity']:.2f} m/s")
        with col3:
            st.metric("Avg Speed", f"{metrics['avg_speed']:.2f} m/s")
        
        st.markdown(MetricsCalculator.format_metrics_display(metrics, mode='1d'))
    
    with tab5:
        df = DataExporter.prepare_1d_dataframe(time_points, x, v, a)
        DataExporter.create_export_section(df, mode='1d')
        
        report = DataExporter.create_report_generator(df, metrics, mode='1d')
        DataExporter.create_report_download(report, filename="1d_simulation_report.txt")
    
    # Kinematic calculator
    st.markdown("---")
    InteractiveWidgets.create_realtime_calculator()

# ==================== 2D KINEMATICS MODE ====================
elif mode == "2D Kinematics":
    st.markdown("## 🎯 2D Kinematics Simulation")
    
    # Preset selector
    preset_name, preset_values = InteractiveWidgets.create_preset_selector(mode='2d')
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎛️ Input Parameters")
        
        subcol1, subcol2 = st.columns(2)
        
        with subcol1:
            st.markdown("**Position & Velocity**")
            if preset_values:
                x0 = st.number_input('Initial X Position x₀ (m)', value=preset_values['x0'], format="%.2f")
                y0 = st.number_input('Initial Y Position y₀ (m)', value=preset_values['y0'], format="%.2f")
                vx0 = st.number_input('Initial X Velocity vx₀ (m/s)', value=preset_values['vx0'], format="%.2f")
                vy0 = st.number_input('Initial Y Velocity vy₀ (m/s)', value=preset_values['vy0'], format="%.2f")
            else:
                x0 = st.number_input('Initial X Position x₀ (m)', value=0.0, format="%.2f")
                y0 = st.number_input('Initial Y Position y₀ (m)', value=0.0, format="%.2f")
                vx0 = st.number_input('Initial X Velocity vx₀ (m/s)', value=15.0, format="%.2f")
                vy0 = st.number_input('Initial Y Velocity vy₀ (m/s)', value=20.0, format="%.2f")
        
        with subcol2:
            st.markdown("**Acceleration**")
            if preset_values:
                ax = st.number_input('X Acceleration ax (m/s²)', value=preset_values['ax'], format="%.2f")
                ay = st.number_input('Y Acceleration ay (m/s²)', value=preset_values['ay'], format="%.2f")
            else:
                ax = st.number_input('X Acceleration ax (m/s²)', value=0.0, format="%.2f")
                ay = st.number_input('Y Acceleration ay (m/s²)', value=-9.8, format="%.2f")
            
            # Show initial speed and angle
            v0_mag = np.sqrt(vx0**2 + vy0**2)
            v0_angle = np.arctan2(vy0, vx0) * 180 / np.pi
            st.info(f"Initial Speed: {v0_mag:.2f} m/s")
            st.info(f"Launch Angle: {v0_angle:.1f}°")
    
    with col2:
        st.markdown("### 📐 Governing Equations")
        st.latex(r"x(t) = x_0 + v_{x0} t + \frac{1}{2} a_x t^2")
        st.latex(r"y(t) = y_0 + v_{y0} t + \frac{1}{2} a_y t^2")
        st.latex(r"v_x(t) = v_{x0} + a_x t")
        st.latex(r"v_y(t) = v_{y0} + a_y t")
    
    # Physics insights
    InteractiveWidgets.create_physics_insights(mode='2d', ax=ax, ay=ay, vx0=vx0, vy0=vy0)
    
    # Predict landing point
    landing = MetricsCalculator.predict_landing_point(x0, y0, vx0, vy0, ax, ay, ground_level=0)
    if landing:
        st.success(f"🎯 **Predicted Landing:** x = {landing['x']:.2f} m at t = {landing['time']:.2f} s")
    
    # Calculate kinematics
    kin2d = Kinematics2D(x0, y0, vx0, vy0, ax, ay)
    x, y = kin2d.position(time_points)
    vx, vy = kin2d.velocity(time_points)
    
    # Calculate metrics
    metrics = MetricsCalculator.calculate_2d_metrics(time_points, x, y, vx, vy, ax, ay)
    
    st.markdown("---")
    
    # Visualization tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Trajectory", "🎬 Animation", "📊 Dashboard", 
        "🌊 Vector Field", "📈 Metrics", "💾 Export"
    ])
    
    with tab1:
        st.markdown("### 🎯 2D Trajectory Plot")
        
        # Interactive time slider
        t_view = st.slider("View trajectory up to time (s):", 0.0, float(time_total), float(time_total), step=0.1)
        mask = time_points <= t_view
        
        fig_traj = go.Figure()
        
        # Trail
        fig_traj.add_trace(go.Scatter(
            x=x[mask], y=y[mask],
            mode='lines+markers',
            marker=dict(
                size=6,
                color=time_points[mask],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Time (s)")
            ),
            line=dict(color='cyan', width=3),
            name='Trajectory'
        ))
        
        # Current position
        if mask.sum() > 0:
            fig_traj.add_trace(go.Scatter(
                x=[x[mask][-1]], y=[y[mask][-1]],
                mode='markers',
                marker=dict(size=settings['marker_size'], color='red', symbol='arrow'),
                name='Current Position'
            ))
            
            # Velocity vector
            if settings['show_velocity_vectors']:
                scale = 0.5
                idx = mask.sum() - 1
                fig_traj.add_trace(go.Scatter(
                    x=[x[idx], x[idx] + vx[idx]*scale],
                    y=[y[idx], y[idx] + vy[idx]*scale],
                    mode='lines',
                    line=dict(color='orange', width=4),
                    name='Velocity Vector'
                ))
        
        # Landing point marker
        if landing and landing['time'] <= time_total:
            fig_traj.add_trace(go.Scatter(
                x=[landing['x']], y=[landing['y']],
                mode='markers',
                marker=dict(size=15, color='green', symbol='star'),
                name='Landing Point'
            ))
        
        fig_traj.update_layout(
            xaxis=dict(title="X Position (m)", scaleanchor="y", scaleratio=1),
            yaxis=dict(title="Y Position (m)"),
            template=plotter.template,
            hovermode='closest',
            showlegend=True
        )
        
        st.plotly_chart(fig_traj, use_container_width=True)
        
        # Snapshot viewer
        snapshot_idx = InteractiveWidgets.create_snapshot_viewer(time_points, x, y, vx, vy)
    
    with tab2:
        st.markdown("### 🎬 Animated 2D Trajectory")
        anim_fig = plotter.create_2d_trajectory_animation(
            x, y, vx, vy, time_points,
            show_velocity_vectors=settings['show_velocity_vectors']
        )
        st.plotly_chart(anim_fig, use_container_width=True)
        st.info("💡 Click 'Play' to watch the motion with real-time velocity vectors and color-coded speed!")
    
    with tab3:
        st.markdown("### 📊 Comprehensive Dashboard")
        dashboard_fig = plotter.create_multi_panel_dashboard(time_points, x, y, vx, vy)
        st.plotly_chart(dashboard_fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 🌊 Acceleration Vector Field")
        
        # Determine plot range based on trajectory
        x_range = [min(x) - 5, max(x) + 5]
        y_range = [min(min(y), 0) - 5, max(y) + 5]
        
        field_fig = plotter.create_vector_field_plot(
            x_range, y_range, ax, ay,
            trajectory_x=x, trajectory_y=y
        )
        st.plotly_chart(field_fig, use_container_width=True)
        st.info("🧭 Arrows show the acceleration field. The trajectory follows this field!")
    
    with tab5:
        # Metrics display
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Max Height", f"{metrics['max_height']:.2f} m")
        with col2:
            st.metric("Range", f"{metrics['range']:.2f} m")
        with col3:
            st.metric("Max Speed", f"{metrics['max_speed']:.2f} m/s")
        with col4:
            st.metric("Total Distance", f"{metrics['total_distance']:.2f} m")
        
        st.markdown(MetricsCalculator.format_metrics_display(metrics, mode='2d'))
        
        # Position and velocity graphs
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pos = go.Figure()
            fig_pos.add_trace(go.Scatter(x=time_points, y=x, name='X Position', line=dict(width=3)))
            fig_pos.add_trace(go.Scatter(x=time_points, y=y, name='Y Position', line=dict(width=3)))
            fig_pos.update_layout(
                title="Position Components vs Time",
                xaxis_title="Time (s)",
                yaxis_title="Position (m)",
                template=plotter.template
            )
            st.plotly_chart(fig_pos, use_container_width=True)
        
        with col2:
            fig_vel = go.Figure()
            fig_vel.add_trace(go.Scatter(x=time_points, y=vx, name='Vx', line=dict(width=3)))
            fig_vel.add_trace(go.Scatter(x=time_points, y=vy, name='Vy', line=dict(width=3)))
            fig_vel.update_layout(
                title="Velocity Components vs Time",
                xaxis_title="Time (s)",
                yaxis_title="Velocity (m/s)",
                template=plotter.template
            )
            st.plotly_chart(fig_vel, use_container_width=True)
    
    with tab6:
        df = DataExporter.prepare_2d_dataframe(time_points, x, y, vx, vy, ax, ay)
        DataExporter.create_export_section(df, mode='2d')
        
        report = DataExporter.create_report_generator(df, metrics, mode='2d')
        DataExporter.create_report_download(report, filename="2d_simulation_report.txt")
        
        # Export configuration
        st.markdown("### ⚙️ Export Simulation Configuration")
        config = DataExporter.export_simulation_config({
            'x0': x0, 'y0': y0, 'vx0': vx0, 'vy0': vy0,
            'ax': ax, 'ay': ay, 'time_total': time_total,
            'preset': preset_name
        }, mode='2d')
        
        st.download_button(
            label="📋 Download Configuration (JSON)",
            data=config,
            file_name="simulation_config.json",
            mime="application/json"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
    <h3>🎓 About This Simulator</h3>
    <p>This advanced kinematics simulator provides real-time visualization, comprehensive analysis, 
    and interactive exploration of 1D and 2D motion. Perfect for students, educators, and physics enthusiasts!</p>
    <p><strong>Features:</strong> Animated trajectories • Phase space analysis • Vector fields • 
    Real-time metrics • Data export • Multiple presets</p>
    <p style='margin-top: 1rem; font-size: 0.9rem;'>
        💡 <strong>Pro Tip:</strong> Deploy to <a href='https://share.streamlit.io/' style='color: #ffd700;'>Streamlit Cloud</a> 
        and share with anyone!
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 1rem; color: #666; font-size: 0.85rem;'>
    Made with ❤️ using Streamlit • All graphs are interactive: Zoom, pan, and hover for details
</div>
""", unsafe_allow_html=True)