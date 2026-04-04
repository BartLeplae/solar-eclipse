"""
Solar Eclipse Kinematics Simulation: Earth Rest Frame
=====================================================
This script simulates the relative motion of the Earth, Moon, and a photon 
stream (sunlight/shadow) during a solar eclipse, specifically from the 
Earth's rest frame. 

It calculates and visualizes stellar aberration angles using high-precision 
decimal arithmetic to account for relativistic light-travel effects.

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
output_path = os.path.join(output_dir, 'solar_eclipse_earth_frame.mp4')

# --- Precision Physics Constants ---
# Using Python's decimal module to handle highly precise calculations needed for aberration
decimal.getcontext().prec = 50
G = decimal.Decimal('6.67430e-11')
M_sun = decimal.Decimal('1.989e30')
c_dec = decimal.Decimal('299792458')

# Earth orbital parameters
r_earth_dec = decimal.Decimal('149.6e9')
v_earth_dec = (G * M_sun / r_earth_dec).sqrt()

# Convert down to standard floats for matplotlib performance
c = float(c_dec)
v_earth = float(v_earth_dec)
r_earth = float(r_earth_dec)

# --- Moon Physics Logic ---
v_moon_rel = 1022.0          # Moon's orbital speed relative to Earth (m/s)
v_moon = v_earth - v_moon_rel # Absolute velocity of the Moon
t_intercept = -1.3           # Time offset when Moon intercepts the photon stream (seconds)

# --- Aberration Angle Calculations ---
# Calculate the perceived angle of incoming light due to observer velocity
theta_earth_dec = v_earth_dec / c_dec
theta_moon_dec = decimal.Decimal(v_moon) / c_dec
diff_theta_dec = abs(theta_earth_dec - theta_moon_dec)

# Convert radians to arcseconds for standard astronomical notation
rad_to_arcsec = (180.0 / math.pi) * 3600.0
theta_earth_arcsec = float(theta_earth_dec) * rad_to_arcsec
theta_moon_arcsec = float(theta_moon_dec) * rad_to_arcsec
diff_theta_arcsec = float(diff_theta_dec) * rad_to_arcsec

# Formatting the UI text block for the plot
angle_str = (f"Stellar Aberration Angles:\n"
             f"Earth ($θ_E$): {theta_earth_arcsec:.3f}''\n"
             f"Moon ($θ_M$): {theta_moon_arcsec:.3f}''\n"
             f"Difference ($Δθ$): {diff_theta_arcsec:.3f}''")

# --- Plotting Conversions ---
# Scale distances and velocities for visualization
c_mkm = c / 1e9               # Light speed in Million km/s
r_earth_mkm = r_earth / 1e9   # Earth distance in Million km
v_kmps = v_earth / 1000       # Earth velocity in km/s
v_moon_kmps = v_moon / 1000   # Moon velocity in km/s
v_moon_rel_kmps = v_moon_rel / 1000 

# X-position where the Moon intercepts the light path
m_x = r_earth_mkm + c_mkm * t_intercept
vm_label = f"$v_{{rel}} = {v_moon_rel_kmps:.1f}$ km/s"

# --- Alignment Logic ---
# Calculates the exact geometric alignment timestamp (Sun, Moon, and Earth forming a line)
t_align = (-r_earth_mkm * v_moon_kmps * t_intercept) / (v_kmps * m_x - r_earth_mkm * v_moon_kmps)

# --- Plotting Setup ---
fig, ax = plt.subplots(figsize=(14, 8))
x_margin = 0.2 * c_mkm
ax.set_xlim(149.0, r_earth_mkm + x_margin)
ax.set_ylim(-20.0, 100.0) 

# Static background reference lines
ax.axvline(r_earth_mkm, color='blue', linestyle=':', linewidth=1, zorder=0, alpha=0.3)
ax.axvline(m_x, color='grey', linestyle=':', linewidth=1, zorder=0, alpha=0.3)

# Solar direction reference line
ax.axhline(0, color='gold', linestyle='-', linewidth=1.5, zorder=1, alpha=0.8)
ax.text(149.05, 2, "Direction Sun at moment of Solar Eclipse", color='darkgoldenrod', fontsize=10, fontweight='bold', va='bottom')

# Relativistic Line of Sight (Diagonal due to transverse velocity)
x_vals = np.array([148.0, 150.3])
y_vals = -(v_kmps / c_mkm) * (x_vals - r_earth_mkm)
ax.plot(x_vals, y_vals, color='red', linestyle='--', alpha=0.5, linewidth=1.5, zorder=1)

# Vector indicating the speed of light 'c'
vec_x_start = 149.4
vec_y_start = 25.0
vec_dx = 0.04
vec_dy = -(v_kmps / c_mkm) * vec_dx
ax.annotate('', xy=(vec_x_start + vec_dx, vec_y_start + vec_dy), xytext=(vec_x_start, vec_y_start),
            arrowprops=dict(arrowstyle="->", color='red', lw=2, mutation_scale=20), zorder=10)
ax.text(vec_x_start + vec_dx/2, vec_y_start + vec_dy/2 + 3, '$c$', color='red', fontsize=14, fontweight='bold', ha='center')

# Axis labels and titles
ax.set_xlabel('Distance from Sun (Million km)')
ax.set_ylabel('Vertical Displacement (km) - Earth Rest Frame') 
ax.set_title("Kinematics of a Solar Eclipse: Earth Rest Frame")
ax.grid(True, linestyle='--', alpha=0.4)

# Render aberration info box
ax.text(0.02, 0.95, angle_str, transform=ax.transAxes, 
        fontsize=11, color='darkred', fontweight='bold', ha='left', va='top', 
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="darkred", alpha=0.9))

# Legend setup with custom graphical markers
from matplotlib.lines import Line2D
custom_lines = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', markersize=8),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='orange', markersize=12),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='lightgrey', markersize=12),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='brown', markersize=12, alpha=0.4),
    Line2D([0], [0], color='red', lw=1.5, alpha=0.5, linestyle='--'), 
    Line2D([0], [0], color='grey', lw=8, linestyle='-'),
    Line2D([0], [0], color='gold', lw=1.5, linestyle='-'),
    Line2D([0], [0], color='red', lw=2, marker='>', markersize=5),
]
ax.legend(custom_lines, [
    'Earth', 'Moon', 'Photon (Active)', 'Photon (Shadow)', 'Moonlight',
    'Line of Sight / Trajectory', 'Moon Shadow', 'Direction Sun at moment Solar Eclipse', 'Velocity Light/Shadow $c$'
], loc='upper right', bbox_to_anchor=(0.99, 0.88), frameon=True, framealpha=0.9)

bbox_props = dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.9)

# --- Animation Logic ---
dynamic_artists = []
times = np.linspace(-4, 0.2, 120)

def update(frame_idx):
    """Updates the celestial body positions and vectors for each animation frame."""
    for artist in dynamic_artists:
        artist.remove()
    dynamic_artists.clear()
    
    t = times[frame_idx]
    
    # Calculate positions based on the Earth Rest Frame
    ex, ey = r_earth_mkm, 0.0
    mx, my = m_x, v_moon_kmps * (t - t_intercept) - v_kmps * t
    px, py = r_earth_mkm + c_mkm * t, -v_kmps * t
    
    earth_dot = ax.scatter(ex, ey, color='blue', s=120, zorder=5)
    moon_dot = ax.scatter(mx, my, color='grey', s=60, zorder=5)
    
    # Photon behavior shifts from active light to shadow upon intercepting the Moon
    if t >= t_intercept:
        p_color = 'lightgrey'
        p_edge = 'dimgrey'
        moonlight_halo = ax.scatter(px, py, color='brown', s=500, alpha=0.4, zorder=4)
        dynamic_artists.append(moonlight_halo)
    else:
        p_color = 'orange'
        p_edge = 'red'
        
    photon_dot = ax.scatter(px, py, color=p_color, s=150, marker='*', zorder=6, edgecolor=p_edge)
    
    # Text updates for timing and Moon's Y-position
    t_rel_align = t - t_align
    time_text = ax.text(0.99, 0.95, f"t = {t_rel_align:.1f} s relative to moment Geometric Alignment", transform=ax.transAxes,
                        va='top', ha='right', fontsize=14, color='black', 
                        fontweight='bold', bbox=bbox_props)
    
    moon_y_text = ax.text(mx + 0.01, my + 5, f"$y = {my:.1f}$ km", 
                          va='bottom', ha='left', fontsize=11, color='dimgrey', 
                          fontweight='bold', bbox=bbox_props)
                        
    dynamic_artists.extend([earth_dot, moon_dot, photon_dot, time_text, moon_y_text])

    # Draw the relative velocity arrow for the Moon
    if t < 0.1:
        v_len = 15.0 
        moon_arrow = ax.annotate('', xy=(mx, my - v_len), xytext=(mx, my), 
                                 arrowprops=dict(arrowstyle="-|>", lw=2, color="purple", shrinkA=0, shrinkB=0, mutation_scale=12))
        moon_text = ax.text(mx - 0.005, my - v_len - 2, vm_label, 
                            ha='right', va='top', fontsize=11, color='purple', bbox=bbox_props)
        dynamic_artists.extend([moon_arrow, moon_text])

    # Render the shadow cast by the Moon hitting Earth
    if t >= t_intercept:
        shadow_y = py - (v_kmps / c_mkm) * (mx - px)
        shadow_line, = ax.plot([px, mx], [py, shadow_y], color='grey', linestyle='-', linewidth=8, alpha=0.6, zorder=2)
        dynamic_artists.append(shadow_line)

ani = animation.FuncAnimation(fig, update, frames=len(times), interval=50, blit=False)

# Save the animation output to the graphs directory
print(f"Saving animation to: {output_path}")
ani.save(output_path, writer='ffmpeg', fps=30)
print("Finished saving successfully.")