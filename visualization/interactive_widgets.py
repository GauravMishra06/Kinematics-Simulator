import streamlit as st
import numpy as np
import plotly.graph_objs as go

class InteractiveWidgets:
    """Advanced interactive widgets for the kinematics simulator"""
    
    @staticmethod
    def create_preset_selector(mode='1d'):
        """
        Create preset scenarios for quick experimentation
        """
        if mode == '1d':
            presets = {
                'Free Fall': {'x0': 100, 'v0': 0, 'a': -9.8},
                'Constant Velocity': {'x0': 0, 'v0': 10, 'a': 0},
                'Accelerating Car': {'x0': 0, 'v0': 0, 'a': 2.5},
                'Braking Vehicle': {'x0': 0, 'v0': 30, 'a': -5},
                'Oscillation': {'x0': 0, 'v0': 10, 'a': -2},
                'Custom': None
            }
        else:  # 2D
            presets = {
                'Projectile Motion': {'x0': 0, 'y0': 0, 'vx0': 20, 'vy0': 20, 'ax': 0, 'ay': -9.8},
                'Horizontal Launch': {'x0': 0, 'y0': 50, 'vx0': 15, 'vy0': 0, 'ax': 0, 'ay': -9.8},
                'Vertical Launch': {'x0': 0, 'y0': 0, 'vx0': 0, 'vy0': 30, 'ax': 0, 'ay': -9.8},
                'Parabolic Path': {'x0': 0, 'y0': 0, 'vx0': 10, 'vy0': 15, 'ax': 0, 'ay': -9.8},
                'Circular Motion (approx)': {'x0': 10, 'y0': 0, 'vx0': 0, 'vy0': 5, 'ax': -2, 'ay': 0},
                'Wind Effect': {'x0': 0, 'y0': 0, 'vx0': 15, 'vy0': 20, 'ax': 2, 'ay': -9.8},
                'Custom': None
            }
        
        preset_name = st.selectbox('🎯 Quick Presets', list(presets.keys()))
        return preset_name, presets[preset_name]
    
    @staticmethod
    def create_comparison_mode():
        """
        Widget for comparing multiple scenarios
        """
        st.markdown("### 🔬 Comparison Mode")
        compare = st.checkbox("Enable Scenario Comparison", value=False)
        
        if compare:
            num_scenarios = st.slider("Number of scenarios to compare", 2, 4, 2)
            return True, num_scenarios
        return False, 1
    
    @staticmethod
    def create_realtime_calculator():
        """
        Real-time kinematic equation calculator
        """
        st.markdown("### 🧮 Kinematic Equation Calculator")
        calc_mode = st.selectbox(
            "What do you want to find?",
            ["Final Velocity (v = v₀ + at)", 
             "Displacement (s = v₀t + ½at²)",
             "Time to reach velocity",
             "Velocity at position"]
        )
        
        results = {}
        
        if calc_mode == "Final Velocity (v = v₀ + at)":
            col1, col2, col3 = st.columns(3)
            with col1:
                v0 = st.number_input("v₀ (m/s)", value=10.0)
            with col2:
                a = st.number_input("a (m/s²)", value=-2.0)
            with col3:
                t = st.number_input("t (s)", value=5.0)
            
            v_final = v0 + a*t
            results['Final Velocity'] = v_final
            st.success(f"**Final Velocity:** {v_final:.3f} m/s")
        
        elif calc_mode == "Displacement (s = v₀t + ½at²)":
            col1, col2, col3 = st.columns(3)
            with col1:
                v0 = st.number_input("v₀ (m/s)", value=10.0)
            with col2:
                a = st.number_input("a (m/s²)", value=-2.0)
            with col3:
                t = st.number_input("t (s)", value=5.0)
            
            displacement = v0*t + 0.5*a*t**2
            results['Displacement'] = displacement
            st.success(f"**Displacement:** {displacement:.3f} m")
        
        elif calc_mode == "Time to reach velocity":
            col1, col2, col3 = st.columns(3)
            with col1:
                v0 = st.number_input("v₀ (m/s)", value=10.0)
            with col2:
                v_target = st.number_input("v_target (m/s)", value=0.0)
            with col3:
                a = st.number_input("a (m/s²)", value=-2.0)
            
            if abs(a) < 0.001:
                st.warning("Acceleration too small!")
            else:
                t_required = (v_target - v0) / a
                results['Time'] = t_required
                if t_required >= 0:
                    st.success(f"**Time Required:** {t_required:.3f} s")
                else:
                    st.error(f"Target velocity cannot be reached (would require negative time)")
        
        elif calc_mode == "Velocity at position":
            col1, col2, col3 = st.columns(3)
            with col1:
                v0 = st.number_input("v₀ (m/s)", value=10.0)
            with col2:
                a = st.number_input("a (m/s²)", value=-2.0)
            with col3:
                s = st.number_input("displacement (m)", value=20.0)
            
            # v² = v₀² + 2as
            v_squared = v0**2 + 2*a*s
            if v_squared >= 0:
                v = np.sqrt(v_squared)
                results['Velocity'] = v
                st.success(f"**Velocity at position:** {v:.3f} m/s")
            else:
                st.error("Object doesn't reach this position!")
        
        return results
    
    @staticmethod
    def create_export_options(fig, data_dict, filename_prefix="kinematics"):
        """
        Create export options for plots and data
        """
        st.markdown("### 💾 Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Download Plot as HTML"):
                fig.write_html(f"{filename_prefix}_plot.html")
                st.success("Plot saved as HTML!")
        
        with col2:
            if st.button("📄 Download Data as CSV"):
                import pandas as pd
                df = pd.DataFrame(data_dict)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{filename_prefix}_data.csv",
                    mime="text/csv"
                )
    
    @staticmethod
    def create_unit_converter():
        """
        Unit conversion widget for international users
        """
        with st.expander("🔄 Unit Converter"):
            conversion_type = st.selectbox(
                "Convert:",
                ["m/s to km/h", "km/h to m/s", "m to ft", "ft to m", "m/s² to g-force"]
            )
            
            value = st.number_input("Value:", value=10.0)
            
            if conversion_type == "m/s to km/h":
                result = value * 3.6
                st.info(f"{value} m/s = **{result:.2f} km/h**")
            elif conversion_type == "km/h to m/s":
                result = value / 3.6
                st.info(f"{value} km/h = **{result:.2f} m/s**")
            elif conversion_type == "m to ft":
                result = value * 3.28084
                st.info(f"{value} m = **{result:.2f} ft**")
            elif conversion_type == "ft to m":
                result = value / 3.28084
                st.info(f"{value} ft = **{result:.2f} m**")
            elif conversion_type == "m/s² to g-force":
                result = value / 9.8
                st.info(f"{value} m/s² = **{result:.3f} g**")
    
    @staticmethod
    def create_help_section():
        """
        Interactive help and tutorial section
        """
        with st.expander("❓ Help & Examples"):
            st.markdown("""
            ### 📚 Quick Guide
            
            **1D Kinematics:**
            - Simulates motion along a straight line
            - Perfect for: free fall, car acceleration, vertical motion
            - Key equations: x = x₀ + v₀t + ½at²
            
            **2D Kinematics:**
            - Simulates motion in a plane (x-y)
            - Perfect for: projectile motion, parabolic trajectories
            - Independent motion in x and y directions
            
            **Tips:**
            - Use negative acceleration for deceleration
            - For gravity, use a = -9.8 m/s²
            - Watch the animated trajectory in real-time
            - Hover over graphs for detailed values
            
            **Example Scenarios:**
            1. **Projectile**: vx₀=20, vy₀=20, ay=-9.8
            2. **Free Fall**: v₀=0, a=-9.8
            3. **Braking Car**: v₀=30, a=-5
            """)
    
    @staticmethod
    def create_advanced_controls():
        """
        Advanced simulation controls
        """
        with st.expander("⚙️ Advanced Settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                show_grid = st.checkbox("Show Grid", value=True)
                show_velocity_vectors = st.checkbox("Show Velocity Vectors", value=True)
                dark_mode = st.checkbox("Dark Mode", value=False)
            
            with col2:
                animation_speed = st.slider("Animation Speed", 1, 10, 5)
                trail_length = st.slider("Trail Length (%)", 0, 100, 100)
                marker_size = st.slider("Marker Size", 5, 30, 15)
            
            return {
                'show_grid': show_grid,
                'show_velocity_vectors': show_velocity_vectors,
                'dark_mode': dark_mode,
                'animation_speed': animation_speed,
                'trail_length': trail_length,
                'marker_size': marker_size
            }
    
    @staticmethod
    def create_physics_insights(mode='1d', **params):
        """
        Display physics insights based on parameters
        """
        st.markdown("### 💡 Physics Insights")
        
        if mode == '1d':
            a = params.get('a', 0)
            v0 = params.get('v0', 0)
            
            insights = []
            
            if abs(a) < 0.01:
                insights.append("✓ **Uniform Motion**: Object moves with constant velocity")
            elif a > 0:
                if v0 >= 0:
                    insights.append("✓ **Accelerating**: Object speeds up in positive direction")
                else:
                    insights.append("✓ **Decelerating then Reversing**: Object slows down, stops, then speeds up")
            elif a < 0:
                if v0 > 0:
                    insights.append("✓ **Decelerating**: Object slows down (may reverse direction)")
                else:
                    insights.append("✓ **Accelerating Backward**: Object speeds up in negative direction")
            
            if abs(a - (-9.8)) < 0.5:
                insights.append("🌍 **Gravitational Acceleration**: Similar to Earth's gravity")
            
            for insight in insights:
                st.info(insight)
        
        else:  # 2D mode
            ax = params.get('ax', 0)
            ay = params.get('ay', 0)
            vx0 = params.get('vx0', 0)
            vy0 = params.get('vy0', 0)
            
            insights = []
            
            if abs(ax) < 0.01 and abs(ay - (-9.8)) < 0.5:
                insights.append("🎯 **Classic Projectile Motion**: Parabolic trajectory under gravity")
            
            if abs(ax) < 0.01 and abs(ay) < 0.01:
                insights.append("✈️ **Uniform Motion**: Constant velocity (straight line)")
            
            if vy0 > 0 and ay < 0:
                insights.append("⬆️ **Upward Launch**: Object rises then falls")
                apex_time = -vy0 / ay
                insights.append(f"📍 Peak reached at t ≈ {apex_time:.2f} s")
            
            if abs(vy0) < 0.01 and abs(ay - (-9.8)) < 0.5:
                insights.append("➡️ **Horizontal Launch**: Dropped while moving horizontally")
            
            if ax != 0:
                insights.append("💨 **Non-zero horizontal acceleration**: Wind or thrust effect")
            
            for insight in insights:
                st.info(insight)
    
    @staticmethod
    def create_snapshot_viewer(time_points, x, y, vx, vy):
        """
        Create a snapshot viewer at specific time points
        """
        st.markdown("### 📸 Snapshot Viewer")
        
        snapshot_time = st.select_slider(
            "Select time for detailed view:",
            options=time_points,
            format_func=lambda t: f"{t:.2f} s"
        )
        
        idx = np.argmin(np.abs(time_points - snapshot_time))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Position", f"({x[idx]:.2f}, {y[idx]:.2f}) m")
        with col2:
            speed = np.sqrt(vx[idx]**2 + vy[idx]**2)
            st.metric("Speed", f"{speed:.2f} m/s")
        with col3:
            angle = np.arctan2(vy[idx], vx[idx]) * 180 / np.pi
            st.metric("Direction", f"{angle:.1f}°")
        
        return idx