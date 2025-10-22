import plotly.graph_objs as go
import numpy as np
from plotly.subplots import make_subplots

class AnimatedPlotter:
    """Advanced animated plotting for kinematics simulations"""
    
    def __init__(self, dark_mode=False):
        self.dark_mode = dark_mode
        self.template = "plotly_dark" if dark_mode else "plotly_white"
        
    def create_animated_1d_trajectory(self, time_points, positions, velocities, particle_size=15):
        """
        Create an animated 1D position plot with velocity color mapping
        """
        frames = []
        max_v = max(abs(velocities.max()), abs(velocities.min()))
        
        for i in range(1, len(time_points)):
            frame_data = go.Scatter(
                x=time_points[:i],
                y=positions[:i],
                mode='lines+markers',
                line=dict(color='cyan', width=3),
                marker=dict(
                    size=[8] * (i-1) + [particle_size],
                    color=velocities[:i],
                    colorscale='Viridis',
                    cmin=-max_v,
                    cmax=max_v,
                    showscale=True,
                    colorbar=dict(title="Velocity (m/s)")
                ),
                name='Position'
            )
            frames.append(go.Frame(data=[frame_data], name=str(i)))
        
        fig = go.Figure(
            data=[go.Scatter(x=[time_points[0]], y=[positions[0]], mode='markers',
                           marker=dict(size=particle_size, color='cyan'))],
            layout=go.Layout(
                title="Animated 1D Motion",
                xaxis=dict(title="Time (s)", range=[0, time_points[-1]]),
                yaxis=dict(title="Position (m)"),
                updatemenus=[{
                    'type': 'buttons',
                    'showactive': False,
                    'buttons': [
                        {'label': 'Play', 'method': 'animate', 
                         'args': [None, {'frame': {'duration': 50, 'redraw': True}, 
                                       'fromcurrent': True}]},
                        {'label': 'Pause', 'method': 'animate',
                         'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 
                                         'mode': 'immediate'}]}
                    ]
                }],
                template=self.template
            ),
            frames=frames
        )
        return fig
    
    def create_2d_trajectory_animation(self, x, y, vx, vy, time_points, show_velocity_vectors=True):
        """
        Create animated 2D trajectory with velocity vectors and trail effect
        """
        frames = []
        speed = np.sqrt(vx**2 + vy**2)
        max_speed = speed.max()
        
        for i in range(1, len(time_points)):
            # Trail with fading effect
            trail = go.Scatter(
                x=x[:i],
                y=y[:i],
                mode='lines',
                line=dict(color='cyan', width=2),
                showlegend=False
            )
            
            # Current position marker
            current = go.Scatter(
                x=[x[i-1]],
                y=[y[i-1]],
                mode='markers',
                marker=dict(
                    size=20,
                    color=speed[i-1],
                    colorscale='Plasma',
                    cmin=0,
                    cmax=max_speed,
                    showscale=True,
                    colorbar=dict(title="Speed (m/s)", x=1.15)
                ),
                showlegend=False
            )
            
            frame_data = [trail, current]
            
            # Velocity vector
            if show_velocity_vectors and i % 5 == 0:
                scale = 0.3
                arrow = go.Scatter(
                    x=[x[i-1], x[i-1] + vx[i-1] * scale],
                    y=[y[i-1], y[i-1] + vy[i-1] * scale],
                    mode='lines',
                    line=dict(color='red', width=3),
                    showlegend=False
                )
                frame_data.append(arrow)
            
            frames.append(go.Frame(data=frame_data, name=str(i)))
        
        # Initial frame
        initial_data = [
            go.Scatter(x=[x[0]], y=[y[0]], mode='markers',
                      marker=dict(size=20, color='cyan'))
        ]
        
        fig = go.Figure(
            data=initial_data,
            layout=go.Layout(
                title="Animated 2D Trajectory",
                xaxis=dict(title="X Position (m)", scaleanchor="y", scaleratio=1),
                yaxis=dict(title="Y Position (m)"),
                updatemenus=[{
                    'type': 'buttons',
                    'showactive': False,
                    'y': 1.15,
                    'x': 0.1,
                    'buttons': [
                        {'label': '▶ Play', 'method': 'animate',
                         'args': [None, {'frame': {'duration': 50, 'redraw': True},
                                       'fromcurrent': True, 'transition': {'duration': 0}}]},
                        {'label': '⏸ Pause', 'method': 'animate',
                         'args': [[None], {'frame': {'duration': 0, 'redraw': False},
                                         'mode': 'immediate'}]}
                    ]
                }],
                template=self.template
            ),
            frames=frames
        )
        return fig
    
    def create_phase_space_plot(self, positions, velocities, time_points):
        """
        Create phase space diagram (position vs velocity) with time color mapping
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=positions,
            y=velocities,
            mode='lines+markers',
            marker=dict(
                size=8,
                color=time_points,
                colorscale='Turbo',
                showscale=True,
                colorbar=dict(title="Time (s)")
            ),
            line=dict(color='rgba(100, 100, 255, 0.5)', width=2),
            name='Phase Space'
        ))
        
        # Start and end markers
        fig.add_trace(go.Scatter(
            x=[positions[0]],
            y=[velocities[0]],
            mode='markers',
            marker=dict(size=15, color='green', symbol='star'),
            name='Start'
        ))
        
        fig.add_trace(go.Scatter(
            x=[positions[-1]],
            y=[velocities[-1]],
            mode='markers',
            marker=dict(size=15, color='red', symbol='x'),
            name='End'
        ))
        
        fig.update_layout(
            title="Phase Space Diagram",
            xaxis_title="Position (m)",
            yaxis_title="Velocity (m/s)",
            template=self.template,
            hovermode='closest'
        )
        
        return fig
    
    def create_multi_panel_dashboard(self, time_points, x, y, vx, vy):
        """
        Create comprehensive 4-panel dashboard for 2D kinematics
        """
        speed = np.sqrt(vx**2 + vy**2)
        acceleration_x = np.gradient(vx, time_points)
        acceleration_y = np.gradient(vy, time_points)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Trajectory (X-Y)', 'Position vs Time',
                          'Velocity Components', 'Speed & Direction'),
            specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
                   [{'type': 'scatter'}, {'type': 'scatter'}]]
        )
        
        # Panel 1: Trajectory
        fig.add_trace(
            go.Scatter(x=x, y=y, mode='lines+markers',
                      marker=dict(size=4, color=time_points, colorscale='Viridis'),
                      line=dict(width=2), name='Trajectory'),
            row=1, col=1
        )
        
        # Panel 2: Position vs Time
        fig.add_trace(
            go.Scatter(x=time_points, y=x, name='X(t)',
                      line=dict(color='blue', width=2)),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=time_points, y=y, name='Y(t)',
                      line=dict(color='red', width=2)),
            row=1, col=2
        )
        
        # Panel 3: Velocity Components
        fig.add_trace(
            go.Scatter(x=time_points, y=vx, name='Vx',
                      line=dict(color='cyan', width=2)),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=time_points, y=vy, name='Vy',
                      line=dict(color='magenta', width=2)),
            row=2, col=1
        )
        
        # Panel 4: Speed and angle
        angle = np.arctan2(vy, vx) * 180 / np.pi
        fig.add_trace(
            go.Scatter(x=time_points, y=speed, name='Speed',
                      line=dict(color='orange', width=2)),
            row=2, col=2
        )
        
        fig.update_xaxes(title_text="X (m)", row=1, col=1)
        fig.update_yaxes(title_text="Y (m)", row=1, col=1)
        fig.update_xaxes(title_text="Time (s)", row=1, col=2)
        fig.update_yaxes(title_text="Position (m)", row=1, col=2)
        fig.update_xaxes(title_text="Time (s)", row=2, col=1)
        fig.update_yaxes(title_text="Velocity (m/s)", row=2, col=1)
        fig.update_xaxes(title_text="Time (s)", row=2, col=2)
        fig.update_yaxes(title_text="Speed (m/s)", row=2, col=2)
        
        fig.update_layout(
            height=800,
            showlegend=True,
            template=self.template,
            title_text="Comprehensive Kinematics Dashboard"
        )
        
        return fig
    
    def create_vector_field_plot(self, x_range, y_range, ax, ay, trajectory_x=None, trajectory_y=None):
        """
        Create acceleration vector field with optional trajectory overlay
        """
        x_grid = np.linspace(x_range[0], x_range[1], 15)
        y_grid = np.linspace(y_range[0], y_range[1], 15)
        X, Y = np.meshgrid(x_grid, y_grid)
        
        # Constant acceleration field
        U = np.ones_like(X) * ax
        V = np.ones_like(Y) * ay
        
        fig = go.Figure()
        
        # Quiver plot (vector field)
        for i in range(len(x_grid)):
            for j in range(len(y_grid)):
                fig.add_trace(go.Scatter(
                    x=[X[j, i], X[j, i] + U[j, i] * 0.5],
                    y=[Y[j, i], Y[j, i] + V[j, i] * 0.5],
                    mode='lines',
                    line=dict(color='rgba(150, 150, 150, 0.6)', width=2),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                # Arrowhead
                fig.add_trace(go.Scatter(
                    x=[X[j, i] + U[j, i] * 0.5],
                    y=[Y[j, i] + V[j, i] * 0.5],
                    mode='markers',
                    marker=dict(size=6, color='gray', symbol='arrow-up'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        # Overlay trajectory if provided
        if trajectory_x is not None and trajectory_y is not None:
            fig.add_trace(go.Scatter(
                x=trajectory_x,
                y=trajectory_y,
                mode='lines+markers',
                line=dict(color='cyan', width=3),
                marker=dict(size=6, color='yellow'),
                name='Trajectory'
            ))
        
        fig.update_layout(
            title=f"Acceleration Field (ax={ax:.1f}, ay={ay:.1f} m/s²)",
            xaxis=dict(title="X Position (m)", scaleanchor="y", scaleratio=1),
            yaxis=dict(title="Y Position (m)"),
            template=self.template
        )
        
        return fig