import plotly.graph_objs as go
import numpy as np
from plotly.subplots import make_subplots

class AdvancedVisualizations:
    """Advanced visualization tools for kinematics including 3D plots"""
    
    @staticmethod
    def create_3d_trajectory_plot(x, y, time_points, height_scale=1.0):
        """
        Create 3D visualization with time as the third dimension
        """
        z = time_points * height_scale
        speed = np.sqrt(np.gradient(x)**2 + np.gradient(y)**2) / np.gradient(time_points)
        
        fig = go.Figure()
        
        # 3D trajectory
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines+markers',
            marker=dict(
                size=5,
                color=speed,
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(title="Speed (m/s)", x=1.15)
            ),
            line=dict(color='cyan', width=4),
            name='Trajectory'
        ))
        
        # Start and end markers
        fig.add_trace(go.Scatter3d(
            x=[x[0]], y=[y[0]], z=[z[0]],
            mode='markers',
            marker=dict(size=10, color='green', symbol='diamond'),
            name='Start'
        ))
        
        fig.add_trace(go.Scatter3d(
            x=[x[-1]], y=[y[-1]], z=[z[-1]],
            mode='markers',
            marker=dict(size=10, color='red', symbol='x'),
            name='End'
        ))
        
        fig.update_layout(
            scene=dict(
                xaxis_title="X Position (m)",
                yaxis_title="Y Position (m)",
                zaxis_title="Time (s)",
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.2)
                )
            ),
            title="3D Space-Time Trajectory"
        )
        
        return fig
    
    @staticmethod
    def create_energy_analysis_plot(time_points, vx, vy, y, ay, mass=1.0):
        """
        Create comprehensive energy analysis plot
        """
        # Calculate energies
        speed = np.sqrt(vx**2 + vy**2)
        ke = 0.5 * mass * speed**2
        
        # Potential energy (if gravity present)
        pe = np.zeros_like(y)
        if abs(ay) > 0.01:
            pe = -mass * ay * (y - y[0])  # Relative to initial height
        
        total_energy = ke + pe
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Energy Components Over Time', 'Energy Conservation Check'),
            vertical_spacing=0.15
        )
        
        # Energy components
        fig.add_trace(
            go.Scatter(x=time_points, y=ke, name='Kinetic Energy',
                      line=dict(color='red', width=2), fill='tozeroy'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=time_points, y=pe, name='Potential Energy',
                      line=dict(color='blue', width=2), fill='tozeroy'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=time_points, y=total_energy, name='Total Energy',
                      line=dict(color='green', width=3, dash='dash')),
            row=1, col=1
        )
        
        # Energy conservation check
        energy_variation = (total_energy - total_energy[0]) / (total_energy[0] + 1e-10) * 100
        
        fig.add_trace(
            go.Scatter(x=time_points, y=energy_variation,
                      line=dict(color='purple', width=2),
                      name='Energy Variation %'),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Time (s)", row=2, col=1)
        fig.update_yaxes(title_text="Energy (J)", row=1, col=1)
        fig.update_yaxes(title_text="Variation (%)", row=2, col=1)
        
        fig.update_layout(
            height=700,
            showlegend=True,
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_hodograph(vx, vy, time_points):
        """
        Create velocity hodograph (velocity space diagram)
        """
        fig = go.Figure()
        
        # Velocity trajectory in velocity space
        fig.add_trace(go.Scatter(
            x=vx, y=vy,
            mode='lines+markers',
            marker=dict(
                size=8,
                color=time_points,
                colorscale='Turbo',
                showscale=True,
                colorbar=dict(title="Time (s)")
            ),
            line=dict(color='rgba(100, 200, 255, 0.6)', width=3),
            name='Velocity Path'
        ))
        
        # Start point
        fig.add_trace(go.Scatter(
            x=[vx[0]], y=[vy[0]],
            mode='markers',
            marker=dict(size=15, color='green', symbol='star'),
            name='Initial Velocity'
        ))
        
        # End point
        fig.add_trace(go.Scatter(
            x=[vx[-1]], y=[vy[-1]],
            mode='markers',
            marker=dict(size=15, color='red', symbol='x'),
            name='Final Velocity'
        ))
        
        # Origin
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers',
            marker=dict(size=10, color='black', symbol='circle'),
            name='Origin'
        ))
        
        fig.update_layout(
            title="Hodograph (Velocity Space)",
            xaxis_title="Vx (m/s)",
            yaxis_title="Vy (m/s)",
            xaxis=dict(scaleanchor="y", scaleratio=1, zeroline=True, zerolinewidth=2),
            yaxis=dict(zeroline=True, zerolinewidth=2),
            hovermode='closest'
        )
        
        return fig
    
    @staticmethod
    def create_comparison_plot(scenarios_data, mode='2d'):
        """
        Create comparison plot for multiple scenarios
        scenarios_data: list of dicts with keys: 'name', 'x', 'y', 'time_points'
        """
        fig = go.Figure()
        
        colors = ['cyan', 'magenta', 'yellow', 'lime', 'orange', 'pink']
        
        for idx, scenario in enumerate(scenarios_data):
            color = colors[idx % len(colors)]
            
            if mode == '2d':
                fig.add_trace(go.Scatter(
                    x=scenario['x'],
                    y=scenario['y'],
                    mode='lines+markers',
                    name=scenario['name'],
                    line=dict(color=color, width=3),
                    marker=dict(size=4)
                ))
                
                # Mark start and end
                fig.add_trace(go.Scatter(
                    x=[scenario['x'][0]],
                    y=[scenario['y'][0]],
                    mode='markers',
                    marker=dict(size=10, color=color, symbol='circle'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                fig.add_trace(go.Scatter(
                    x=[scenario['x'][-1]],
                    y=[scenario['y'][-1]],
                    mode='markers',
                    marker=dict(size=10, color=color, symbol='x'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        fig.update_layout(
            title="Scenario Comparison",
            xaxis_title="X Position (m)",
            yaxis_title="Y Position (m)",
            xaxis=dict(scaleanchor="y", scaleratio=1),
            hovermode='closest',
            legend=dict(x=1.05, y=1)
        )
        
        return fig
    
    @staticmethod
    def create_motion_heatmap(x, y, vx, vy, time_points, grid_size=50):
        """
        Create heatmap showing time spent in different regions
        """
        # Create grid
        x_bins = np.linspace(x.min(), x.max(), grid_size)
        y_bins = np.linspace(y.min(), y.max(), grid_size)
        
        # Bin the trajectory
        heatmap, xedges, yedges = np.histogram2d(x, y, bins=[x_bins, y_bins])
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap.T,
            x=xedges,
            y=yedges,
            colorscale='Hot',
            colorbar=dict(title="Frequency")
        ))
        
        # Overlay trajectory
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode='lines',
            line=dict(color='cyan', width=2),
            name='Trajectory',
            showlegend=True
        ))
        
        fig.update_layout(
            title="Motion Density Heatmap",
            xaxis_title="X Position (m)",
            yaxis_title="Y Position (m)",
            xaxis=dict(scaleanchor="y", scaleratio=1)
        )
        
        return fig
    
    @staticmethod
    def create_acceleration_analysis(time_points, vx, vy):
        """
        Create detailed acceleration analysis plot
        """
        # Calculate accelerations numerically
        ax = np.gradient(vx, time_points)
        ay = np.gradient(vy, time_points)
        a_mag = np.sqrt(ax**2 + ay**2)
        a_angle = np.arctan2(ay, ax) * 180 / np.pi
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Acceleration Components', 'Acceleration Magnitude',
                          'Acceleration Direction', 'Acceleration vs Velocity'),
            specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
                   [{'type': 'scatter'}, {'type': 'scatter'}]]
        )
        
        # Acceleration components
        fig.add_trace(
            go.Scatter(x=time_points, y=ax, name='ax', line=dict(color='red')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=time_points, y=ay, name='ay', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Magnitude
        fig.add_trace(
            go.Scatter(x=time_points, y=a_mag, name='|a|',
                      line=dict(color='purple', width=3)),
            row=1, col=2
        )
        
        # Direction
        fig.add_trace(
            go.Scatter(x=time_points, y=a_angle, name='angle',
                      line=dict(color='green', width=2)),
            row=2, col=1
        )
        
        # Acceleration vs velocity (hodograph derivative)
        speed = np.sqrt(vx**2 + vy**2)
        fig.add_trace(
            go.Scatter(x=speed, y=a_mag, mode='markers',
                      marker=dict(color=time_points, colorscale='Viridis', showscale=True),
                      name='a vs v'),
            row=2, col=2
        )
        
        fig.update_xaxes(title_text="Time (s)", row=1, col=1)
        fig.update_xaxes(title_text="Time (s)", row=1, col=2)
        fig.update_xaxes(title_text="Time (s)", row=2, col=1)
        fig.update_xaxes(title_text="Speed (m/s)", row=2, col=2)
        
        fig.update_yaxes(title_text="a (m/s²)", row=1, col=1)
        fig.update_yaxes(title_text="|a| (m/s²)", row=1, col=2)
        fig.update_yaxes(title_text="Angle (°)", row=2, col=1)
        fig.update_yaxes(title_text="|a| (m/s²)", row=2, col=2)
        
        fig.update_layout(height=800, showlegend=True)
        
        return fig
    
    @staticmethod
    def create_tangent_normal_analysis(x, y, time_points):
        """
        Analyze tangential and normal components of motion
        """
        # Calculate derivatives
        vx = np.gradient(x, time_points)
        vy = np.gradient(y, time_points)
        ax = np.gradient(vx, time_points)
        ay = np.gradient(vy, time_points)
        
        speed = np.sqrt(vx**2 + vy**2)
        
        # Tangential acceleration (along velocity)
        a_tangent = (vx * ax + vy * ay) / (speed + 1e-10)
        
        # Normal acceleration (perpendicular to velocity)
        a_total = np.sqrt(ax**2 + ay**2)
        a_normal = np.sqrt(np.maximum(0, a_total**2 - a_tangent**2))
        
        # Curvature
        curvature = a_normal / (speed**2 + 1e-10)
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Tangential vs Normal Acceleration', 'Path Curvature')
        )
        
        fig.add_trace(
            go.Scatter(x=time_points, y=a_tangent, name='Tangential',
                      line=dict(color='red', width=2)),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=time_points, y=a_normal, name='Normal',
                      line=dict(color='blue', width=2)),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=time_points, y=curvature, name='Curvature',
                      line=dict(color='green', width=2)),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Time (s)", row=2, col=1)
        fig.update_yaxes(title_text="Acceleration (m/s²)", row=1, col=1)
        fig.update_yaxes(title_text="Curvature (m⁻¹)", row=2, col=1)
        
        fig.update_layout(height=600)
        
        return fig