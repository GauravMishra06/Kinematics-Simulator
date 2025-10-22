import pandas as pd
import json
import numpy as np
from io import BytesIO
import streamlit as st

class DataExporter:
    """Handle data export in various formats"""
    
    @staticmethod
    def prepare_1d_dataframe(time_points, positions, velocities, acceleration):
        """
        Prepare 1D kinematics data as DataFrame
        """
        # Calculate additional metrics
        accelerations = np.full_like(time_points, acceleration)
        kinetic_energy = 0.5 * velocities**2
        
        df = pd.DataFrame({
            'Time (s)': time_points,
            'Position (m)': positions,
            'Velocity (m/s)': velocities,
            'Acceleration (m/s²)': accelerations,
            'Kinetic Energy (J)': kinetic_energy,
            'Distance from Origin (m)': np.abs(positions)
        })
        
        return df
    
    @staticmethod
    def prepare_2d_dataframe(time_points, x, y, vx, vy, ax, ay):
        """
        Prepare 2D kinematics data as DataFrame
        """
        # Calculate derived quantities
        speed = np.sqrt(vx**2 + vy**2)
        velocity_angle = np.arctan2(vy, vx) * 180 / np.pi
        distance_from_origin = np.sqrt(x**2 + y**2)
        kinetic_energy = 0.5 * speed**2
        
        # Cumulative distance
        distances = np.concatenate([[0], np.sqrt(np.diff(x)**2 + np.diff(y)**2)])
        cumulative_distance = np.cumsum(distances)
        
        df = pd.DataFrame({
            'Time (s)': time_points,
            'X Position (m)': x,
            'Y Position (m)': y,
            'X Velocity (m/s)': vx,
            'Y Velocity (m/s)': vy,
            'Speed (m/s)': speed,
            'Velocity Angle (°)': velocity_angle,
            'X Acceleration (m/s²)': np.full_like(time_points, ax),
            'Y Acceleration (m/s²)': np.full_like(time_points, ay),
            'Distance from Origin (m)': distance_from_origin,
            'Cumulative Distance (m)': cumulative_distance,
            'Kinetic Energy (J)': kinetic_energy
        })
        
        return df
    
    @staticmethod
    def export_to_csv(df, filename="kinematics_data.csv"):
        """
        Export DataFrame to CSV
        """
        csv = df.to_csv(index=False)
        return csv
    
    @staticmethod
    def export_to_excel(df, filename="kinematics_data.xlsx"):
        """
        Export DataFrame to Excel
        """
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Kinematics Data')
        
        return output.getvalue()
    
    @staticmethod
    def export_to_json(df, filename="kinematics_data.json"):
        """
        Export DataFrame to JSON
        """
        return df.to_json(orient='records', indent=2)
    
    @staticmethod
    def create_export_section(df, mode='1d'):
        """
        Create comprehensive export section in Streamlit
        """
        st.markdown("### 💾 Export Simulation Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = DataExporter.export_to_csv(df)
            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name=f"kinematics_{mode}_data.csv",
                mime="text/csv",
                help="Download data in CSV format"
            )
        
        with col2:
            excel_data = DataExporter.export_to_excel(df)
            st.download_button(
                label="📊 Download Excel",
                data=excel_data,
                file_name=f"kinematics_{mode}_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download data in Excel format"
            )
        
        with col3:
            json_data = DataExporter.export_to_json(df)
            st.download_button(
                label="📋 Download JSON",
                data=json_data,
                file_name=f"kinematics_{mode}_data.json",
                mime="application/json",
                help="Download data in JSON format"
            )
        
        # Show preview
        with st.expander("👀 Preview Data"):
            st.dataframe(df, use_container_width=True)
            st.info(f"Total data points: {len(df)}")
    
    @staticmethod
    def export_simulation_config(params, mode='1d'):
        """
        Export simulation configuration as JSON
        """
        config = {
            'mode': mode,
            'parameters': params,
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        return json.dumps(config, indent=2)
    
    @staticmethod
    def create_report_generator(df, metrics, mode='1d'):
        """
        Generate comprehensive text report
        """
        report = f"""
KINEMATICS SIMULATION REPORT
{'='*50}
Mode: {mode.upper()}
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY STATISTICS:
{'='*50}
"""
        
        if mode == '1d':
            report += f"""
Total Displacement: {metrics['total_displacement']:.3f} m
Total Distance: {metrics['total_distance']:.3f} m
Maximum Position: {metrics['max_position']:.3f} m
Minimum Position: {metrics['min_position']:.3f} m

Maximum Velocity: {metrics['max_velocity']:.3f} m/s
Minimum Velocity: {metrics['min_velocity']:.3f} m/s
Average Velocity: {metrics['avg_velocity']:.3f} m/s

Acceleration: {metrics['acceleration']:.3f} m/s²
Turning Points: {metrics['turning_points']}

Initial KE: {metrics['initial_kinetic_energy']:.3f} J
Final KE: {metrics['final_kinetic_energy']:.3f} J
"""
        else:  # 2D
            report += f"""
Total Displacement: {metrics['total_displacement']:.3f} m
Displacement Angle: {metrics['displacement_angle']:.1f}°
Total Distance: {metrics['total_distance']:.3f} m
Horizontal Range: {metrics['range']:.3f} m

Maximum Speed: {metrics['max_speed']:.3f} m/s
Average Speed: {metrics['avg_speed']:.3f} m/s
Final Speed: {metrics['final_speed']:.3f} m/s

Acceleration Magnitude: {metrics['acceleration_magnitude']:.3f} m/s²
Acceleration Direction: {metrics['acceleration_angle']:.1f}°

Maximum Height: {metrics['max_height']:.3f} m
"""
            
            if 'apex_time' in metrics:
                report += f"""
PROJECTILE MOTION DETAILS:
Apex Time: {metrics['apex_time']:.3f} s
Apex Height: {metrics['apex_height']:.3f} m
Apex X Position: {metrics['apex_x_position']:.3f} m
"""
        
        report += f"""

DATA SUMMARY:
{'='*50}
Number of Data Points: {len(df)}
Time Range: {df['Time (s)'].min():.2f} - {df['Time (s)'].max():.2f} s

First 5 Data Points:
{df.head().to_string()}

Last 5 Data Points:
{df.tail().to_string()}
"""
        
        return report
    
    @staticmethod
    def create_report_download(report_text, filename="simulation_report.txt"):
        """
        Create download button for text report
        """
        st.download_button(
            label="📝 Download Full Report",
            data=report_text,
            file_name=filename,
            mime="text/plain",
            help="Download complete simulation report"
        )