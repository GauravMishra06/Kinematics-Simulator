import numpy as np

class MetricsCalculator:
    """Calculate advanced kinematics metrics and statistics"""
    
    @staticmethod
    def calculate_1d_metrics(time_points, positions, velocities, acceleration):
        """
        Calculate comprehensive metrics for 1D motion
        """
        metrics = {}
        
        # Basic metrics
        metrics['total_displacement'] = positions[-1] - positions[0]
        metrics['total_distance'] = np.sum(np.abs(np.diff(positions)))
        metrics['max_position'] = np.max(positions)
        metrics['min_position'] = np.min(positions)
        metrics['max_velocity'] = np.max(velocities)
        metrics['min_velocity'] = np.min(velocities)
        metrics['avg_velocity'] = metrics['total_displacement'] / time_points[-1]
        metrics['avg_speed'] = metrics['total_distance'] / time_points[-1]
        
        # Acceleration info
        metrics['acceleration'] = acceleration
        
        # Zero crossings
        position_crossings = np.where(np.diff(np.sign(positions)))[0]
        velocity_crossings = np.where(np.diff(np.sign(velocities)))[0]
        metrics['position_zero_crossings'] = len(position_crossings)
        metrics['velocity_zero_crossings'] = len(velocity_crossings)
        
        if len(velocity_crossings) > 0:
            metrics['turning_points'] = len(velocity_crossings)
            metrics['turning_times'] = time_points[velocity_crossings].tolist()
        else:
            metrics['turning_points'] = 0
            metrics['turning_times'] = []
        
        # Energy-like quantities (assuming unit mass)
        metrics['initial_kinetic_energy'] = 0.5 * velocities[0]**2
        metrics['final_kinetic_energy'] = 0.5 * velocities[-1]**2
        metrics['kinetic_energy_change'] = metrics['final_kinetic_energy'] - metrics['initial_kinetic_energy']
        
        return metrics
    
    @staticmethod
    def calculate_2d_metrics(time_points, x, y, vx, vy, ax, ay):
        """
        Calculate comprehensive metrics for 2D motion
        """
        metrics = {}
        
        # Displacement and distance
        displacement = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2)
        distances = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
        total_distance = np.sum(distances)
        
        metrics['total_displacement'] = displacement
        metrics['total_distance'] = total_distance
        metrics['displacement_angle'] = np.arctan2(y[-1] - y[0], x[-1] - x[0]) * 180 / np.pi
        
        # Speed calculations
        speed = np.sqrt(vx**2 + vy**2)
        metrics['max_speed'] = np.max(speed)
        metrics['min_speed'] = np.min(speed)
        metrics['avg_speed'] = total_distance / time_points[-1]
        metrics['final_speed'] = speed[-1]
        
        # Velocity angle
        velocity_angle = np.arctan2(vy, vx) * 180 / np.pi
        metrics['initial_velocity_angle'] = velocity_angle[0]
        metrics['final_velocity_angle'] = velocity_angle[-1]
        metrics['angle_change'] = velocity_angle[-1] - velocity_angle[0]
        
        # Position bounds
        metrics['max_x'] = np.max(x)
        metrics['min_x'] = np.min(x)
        metrics['max_y'] = np.max(y)
        metrics['min_y'] = np.min(y)
        metrics['max_height'] = np.max(y)
        
        # Range (horizontal distance)
        metrics['range'] = x[-1] - x[0]
        
        # Flight time and apex time (if projectile motion)
        if ay < 0 and vy[0] > 0:  # Projectile motion detected
            apex_idx = np.argmax(y)
            metrics['apex_time'] = time_points[apex_idx]
            metrics['apex_height'] = y[apex_idx]
            metrics['apex_x_position'] = x[apex_idx]
            
            # Theoretical flight time (if it hits ground)
            if y[-1] <= y[0]:
                ground_crossings = np.where((y[:-1] >= y[0]) & (y[1:] < y[0]))[0]
                if len(ground_crossings) > 0:
                    metrics['flight_time'] = time_points[ground_crossings[-1]]
        
        # Acceleration magnitude
        metrics['acceleration_magnitude'] = np.sqrt(ax**2 + ay**2)
        metrics['acceleration_angle'] = np.arctan2(ay, ax) * 180 / np.pi
        
        # Energy calculations (assuming unit mass)
        ke_initial = 0.5 * (vx[0]**2 + vy[0]**2)
        ke_final = 0.5 * (vx[-1]**2 + vy[-1]**2)
        metrics['initial_kinetic_energy'] = ke_initial
        metrics['final_kinetic_energy'] = ke_final
        
        # Potential energy change (assuming uniform gravity)
        if ay != 0:
            metrics['potential_energy_change'] = -ay * (y[-1] - y[0])
            metrics['total_mechanical_energy_change'] = (ke_final - ke_initial) + metrics['potential_energy_change']
        
        # Curvature analysis
        dx = np.gradient(x, time_points)
        dy = np.gradient(y, time_points)
        ddx = np.gradient(dx, time_points)
        ddy = np.gradient(dy, time_points)
        
        # Curvature = |x'y'' - y'x''| / (x'^2 + y'^2)^(3/2)
        curvature = np.abs(dx * ddy - dy * ddx) / (dx**2 + dy**2)**(3/2)
        curvature = curvature[~np.isnan(curvature)]
        if len(curvature) > 0:
            metrics['max_curvature'] = np.max(curvature)
            metrics['avg_curvature'] = np.mean(curvature)
        
        return metrics
    
    @staticmethod
    def format_metrics_display(metrics, mode='1d'):
        """
        Format metrics for display in Streamlit
        """
        if mode == '1d':
            return f"""
### 📊 Motion Statistics

**Displacement & Distance:**
- Total Displacement: {metrics['total_displacement']:.3f} m
- Total Distance Traveled: {metrics['total_distance']:.3f} m
- Maximum Position: {metrics['max_position']:.3f} m
- Minimum Position: {metrics['min_position']:.3f} m

**Velocity Analysis:**
- Maximum Velocity: {metrics['max_velocity']:.3f} m/s
- Minimum Velocity: {metrics['min_velocity']:.3f} m/s
- Average Velocity: {metrics['avg_velocity']:.3f} m/s
- Average Speed: {metrics['avg_speed']:.3f} m/s

**Motion Characteristics:**
- Acceleration: {metrics['acceleration']:.3f} m/s²
- Turning Points: {metrics['turning_points']}
- Position Zero Crossings: {metrics['position_zero_crossings']}

**Energy (unit mass):**
- Initial KE: {metrics['initial_kinetic_energy']:.3f} J
- Final KE: {metrics['final_kinetic_energy']:.3f} J
- ΔKE: {metrics['kinetic_energy_change']:.3f} J
"""
        else:  # 2D mode
            output = f"""
### 📊 Motion Statistics

**Displacement & Distance:**
- Total Displacement: {metrics['total_displacement']:.3f} m at {metrics['displacement_angle']:.1f}°
- Total Distance Traveled: {metrics['total_distance']:.3f} m
- Horizontal Range: {metrics['range']:.3f} m
- Maximum Height: {metrics['max_height']:.3f} m

**Speed Analysis:**
- Maximum Speed: {metrics['max_speed']:.3f} m/s
- Minimum Speed: {metrics['min_speed']:.3f} m/s
- Average Speed: {metrics['avg_speed']:.3f} m/s
- Final Speed: {metrics['final_speed']:.3f} m/s

**Velocity Direction:**
- Initial Angle: {metrics['initial_velocity_angle']:.1f}°
- Final Angle: {metrics['final_velocity_angle']:.1f}°
- Total Angle Change: {metrics['angle_change']:.1f}°

**Position Bounds:**
- X: [{metrics['min_x']:.2f}, {metrics['max_x']:.2f}] m
- Y: [{metrics['min_y']:.2f}, {metrics['max_y']:.2f}] m
"""
            
            # Add projectile-specific metrics if available
            if 'apex_time' in metrics:
                output += f"""
**Projectile Motion:**
- Apex Time: {metrics['apex_time']:.3f} s
- Apex Height: {metrics['apex_height']:.3f} m
- Apex X Position: {metrics['apex_x_position']:.3f} m
"""
                if 'flight_time' in metrics:
                    output += f"- Flight Time: {metrics['flight_time']:.3f} s\n"
            
            output += f"""
**Acceleration:**
- Magnitude: {metrics['acceleration_magnitude']:.3f} m/s²
- Direction: {metrics['acceleration_angle']:.1f}°

**Energy (unit mass):**
- Initial KE: {metrics['initial_kinetic_energy']:.3f} J
- Final KE: {metrics['final_kinetic_energy']:.3f} J
"""
            if 'potential_energy_change' in metrics:
                output += f"- ΔPE: {metrics['potential_energy_change']:.3f} J\n"
                output += f"- Total ΔME: {metrics['total_mechanical_energy_change']:.3f} J\n"
            
            if 'max_curvature' in metrics:
                output += f"""
**Path Curvature:**
- Maximum: {metrics['max_curvature']:.6f} m⁻¹
- Average: {metrics['avg_curvature']:.6f} m⁻¹
"""
            
            return output
    
    @staticmethod
    def predict_landing_point(x0, y0, vx0, vy0, ax, ay, ground_level=0):
        """
        Calculate landing point for projectile motion
        """
        if ay >= 0:
            return None  # Not falling
        
        # Solve y = y0 + vy0*t + 0.5*ay*t^2 = ground_level
        # 0.5*ay*t^2 + vy0*t + (y0 - ground_level) = 0
        
        a_coef = 0.5 * ay
        b_coef = vy0
        c_coef = y0 - ground_level
        
        discriminant = b_coef**2 - 4*a_coef*c_coef
        
        if discriminant < 0:
            return None  # Doesn't reach ground
        
        t1 = (-b_coef + np.sqrt(discriminant)) / (2*a_coef)
        t2 = (-b_coef - np.sqrt(discriminant)) / (2*a_coef)
        
        # Take the positive time that's not zero
        landing_time = max(t1, t2) if max(t1, t2) > 0.01 else None
        
        if landing_time:
            landing_x = x0 + vx0*landing_time + 0.5*ax*landing_time**2
            return {
                'time': landing_time,
                'x': landing_x,
                'y': ground_level,
                'vx': vx0 + ax*landing_time,
                'vy': vy0 + ay*landing_time
            }
        return None