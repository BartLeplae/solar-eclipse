"""
Solar System Photon Travel & Aberration Simulation
==================================================
This script visualizes a photon's journey from the Sun outward past Jupiter, 
demonstrating the relationship between the speed of light, local orbital 
velocity, and stellar aberration. 

It uses high-precision decimal calculations to calculate subtle relativistic 
timing differences (in nanoseconds) and apparent speed discrepancies 
experienced by local inertial frames.

Expected Project Structure:
    ├── graphs/   # Output directory for the MP4 animations
    └── src/      # Directory containing this script

Dependencies: matplotlib, numpy, ffmpeg
"""

import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import decimal
import math

# --- Directory Management ---
# Automatically resolve paths to ensure the output goes to the '../graphs/' directory
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '..', 'graphs')
os.makedirs(output_dir, exist_ok=True) # Create the graphs folder if it doesn't exist
output_path = os.path.join(output_dir, 'photon_animation_jupiter.mp4')

# Set precision to 50 decimal places for exact relativistic calculations
decimal.getcontext().prec = 50

# --- Physics Constants (using Decimal for exactness) ---
G = decimal.Decimal('6.67430e-11')
M_sun = decimal.Decimal('1.989e30')
c = decimal.Decimal('299792458')

# Orbital distances from the Sun (in meters)
r_mercury = 57.9e9
r_venus = 108.2e9
r_earth = 149.6e9
r_mars = 227.9e9
r_jupiter = 778.5e9  

# Array of spatial points (includes spaces between planets for plot boundaries)
distances = [
    r_mercury,
    (r_mercury + r_venus) / 2,
    r_venus,
    (r_venus + r_earth) / 2,
    r_earth,
    (r_earth + r_mars) / 2,
    r_mars,
    (r_mars + r_jupiter) / 2,
    r_jupiter
]

# Only labeling the actual planets
names = ['Mercury', None, 'Venus', None, 'Earth', None, 'Mars', None, 'Jupiter']
x_positions = [float(d) / 1e9 for d in distances]

fig, ax = plt.subplots(figsize=(14, 7))

# Photon starts at the border of the Sun and travels past Jupiter
# Logspace ensures smooth visual movement across the logarithmic axis
x_frames = np.logspace(np.log10(0.7), np.log10(820), 250)

# Calculate transition distance where theoretical orbital velocity equals 80 km/s (80,000 m/s)
# Derived from r = GM / v^2
r_trans_m = float(G * M_sun) / (80000.0**2)
x_trans = r_trans_m / 1e9  # converted to Million km

# --- Precalculate Cumulative Extra Time & Distance ---
# Tracks the accumulated delay caused by relativistic aberration
extra_data = [(0.0, 0.0)]
current_extra_time = decimal.Decimal('0')

for i in range(1, len(x_frames)):
    dx_val = decimal.Decimal(str((x_frames[i] - x_frames[i-1]) * 1e9))
    
    # Calculate velocity at the midpoint of this frame's travel for better accuracy
    x_mid = (x_frames[i] + x_frames[i-1]) / 2.0
    r_mid = decimal.Decimal(str(x_mid * 1e9))
    
    v_true = (G * M_sun / r_mid).sqrt()
    
    # Ramp up from 0 to 80 km/s between Sun's border (0.7M km) and x_trans
    if x_mid < x_trans:
        v_ramp = 80000.0 * max(0.0, (x_mid - 0.7)) / (x_trans - 0.7)
        v_actual = decimal.Decimal(str(v_ramp))
    else:
        v_actual = v_true  # Past transition, follows standard Keplerian orbital velocity
    
    # Exact apparent speed of light c_x for this step
    c_x = (c**2 - v_actual**2).sqrt()
    
    # Time delta calculations (seconds)
    dt_true = dx_val / c
    dt_app = dx_val / c_x
    dt_extra = dt_app - dt_true
    
    current_extra_time += dt_extra
    
    # Convert extra time to nanoseconds (1e9) and equivalent spatial distance in meters
    extra_ns = float(current_extra_time * decimal.Decimal('1e9'))
    extra_dist_m = float(current_extra_time * c)
    
    extra_data.append((extra_ns, extra_dist_m))

def update(frame):
    """Update function for rendering individual animation frames."""
    ax.clear()
    
    # Plot the Sun at 0.4 (Log scale cannot plot exactly 0)
    ax.scatter([0.4], [0], color='orange', s=400, label='Sun', zorder=5)
    
    # Draw and label the Sun's border (0.7 Million km)
    ax.axvline(0.7, color='orange', linestyle=':', linewidth=1.5, zorder=0)
    ax.text(0.7, 30, 'Sun Border', ha='center', va='bottom', fontsize=11, color='orange', 
            fontweight='bold', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    x = float(x_frames[frame])
    r_val = decimal.Decimal(str(x * 1e9))
    
    # Draw the trailing yellow light path from the Sun up to the photon's current position
    ax.plot([0.7, x], [0, 0], color='yellow', linewidth=4, zorder=1)
    
    # Calculate standard theoretical velocity
    v_true = float((G * M_sun / r_val).sqrt())
    
    # Ramp up logic from 0 to 80 km/s near the Sun
    if x < x_trans:
        v_capped = 80000.0 * max(0.0, (x - 0.7)) / (x_trans - 0.7)
    else:
        v_capped = v_true
    
    # High-precision physics updates using the current velocity
    v_dec = decimal.Decimal(str(v_capped))
    x_comp = (c**2 - v_dec**2).sqrt()
    diff_meters_per_sec = float(c - x_comp)
    
    # Format apparent speed label depending on resolution
    if diff_meters_per_sec < 2.0:
        diff_str = f"c - {diff_meters_per_sec:.1f} m/s"
    else:
        diff_str = f"c - {diff_meters_per_sec:.0f} m/s"
    
    c_float = float(c)
    
    # Aberration Angle Calculation (Prevent math domain error when v_capped is exactly 0)
    ratio = v_capped / c_float
    theta_rad = math.asin(ratio) if ratio > 0 else 0.0
    theta_arcsec = theta_rad * (180.0 / math.pi) * 3600.0
    
    arcsec_str = f"{theta_arcsec:.0f}''"
    v_km_s = v_capped / 1000.0
    v_str = f"{v_km_s:.0f} km/s"
    
    # Timer logic (Base Time)
    t_seconds = (x * 1e9) / c_float
    t_minutes = t_seconds / 60.0
    
    # Retrieve the extra accumulated nanoseconds and distance
    extra_ns, extra_dist_m = extra_data[frame]
    
    dy = -v_km_s  
    # Make vector dx proportional to x so the triangle remains consistent visually on a log scale
    dx = x * 0.25     
    
    base_arrow_props = dict(arrowstyle="-|>", lw=1.5, shrinkA=0, shrinkB=0, mutation_scale=10)
    
    # Render moving Photon
    ax.scatter([x], [0], color='yellow', edgecolor='red', s=150, zorder=10, label='Photon')
    
    # Render Physics Vectors (Aberration, Light Direction, Local Frame Velocity)
    ax.annotate('', xy=(x + dx, dy), xytext=(x, 0), arrowprops=dict(**base_arrow_props, color="red"))
    ax.annotate('', xy=(x + dx, 0), xytext=(x + dx, dy), arrowprops=dict(**base_arrow_props, color="green"))
    ax.annotate('', xy=(x + dx, 0), xytext=(x, 0), arrowprops=dict(**base_arrow_props, color="black"))
    
    # Timer Label anchored to the top center of the axes
    timer_str = f"Photon Travel Time: {t_minutes:.0f} min  +  {extra_ns:.1f} ns ({extra_dist_m:.1f} m)"
    ax.text(0.5, 0.92, timer_str, ha='center', va='center', transform=ax.transAxes,
            fontsize=16, color='blue', fontweight='bold', 
            bbox=dict(facecolor='white', edgecolor='blue', alpha=0.9, boxstyle='round,pad=0.5'))
    
    # Labels and marker lines for fixed planetary orbits
    planet_count = 0
    for px, name in zip(x_positions, names):
        if name:
            y_pos = 12 if planet_count % 2 == 0 else 22
            ax.text(px, y_pos, name, ha='center', va='bottom', fontsize=13, fontweight='bold',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
            
            if y_pos == 22:
                ax.plot([px, px], [0, 22], color='gray', linestyle=':', linewidth=1, zorder=0)
                
            planet_count += 1
            
    # Moving Text Annotations tracking the vectors
    ax.text(x + dx/2, dy/2, ' c ', ha='right', va='center', fontsize=12, color='red', fontstyle='italic', fontweight='bold')
    ax.text(x + dx/2, 4, diff_str, ha='center', va='bottom', fontsize=10, color='black')
    ax.text(x + dx * 1.05, dy/2, v_str, ha='left', va='center', fontsize=10, color='green')
    ax.text(x + dx, dy - 2, arcsec_str, ha='center', va='top', fontsize=10, color='red', fontweight='bold')

    # Apply Logarithmic Scale mapping
    ax.set_xscale('log')
    ax.set_xlim(0.4, 1500)
    
    ax.set_ylim(-90, 60)
    ax.axhline(0, color='black', linewidth=0.8, zorder=0)
    
    ax.set_xlabel('Distance from Sun (Million km) [Logarithmic Scale]')
    ax.set_ylabel('Velocity Y-Component (km/s)')
    ax.set_title('Animated Velocity Vectors: Speed of Light (c) vs Orbital Velocity')
    ax.grid(True, linestyle='--', alpha=0.5)

    # Compile the Custom UI Legend
    from matplotlib.lines import Line2D
    custom_lines = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=15),
        Line2D([0], [0], color='yellow', lw=4),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markeredgecolor='red', markersize=10),
        Line2D([0], [0], color='red', lw=2),
        Line2D([0], [0], color='green', lw=2),
        Line2D([0], [0], color='black', lw=2)
    ]
    ax.legend(custom_lines, [
        'Sun', 'Light Path', 'Photon', 'Direction light (velocity c) upon aberration', 
        'Orbital Velocity of Local Inertial Frame', 'Apparent speed of light'
    ], loc='lower right')

# Generate the animation object
ani = animation.FuncAnimation(fig, update, frames=len(x_frames), interval=50)

# Save the animation formally as an .mp4 using ffmpeg writer
print(f"Saving animation to: {output_path}")
writer = animation.FFMpegWriter(fps=20, metadata=dict(artist='Matplotlib'), bitrate=1000)
ani.save(output_path, writer=writer)

print("Video generation perfectly completed.")