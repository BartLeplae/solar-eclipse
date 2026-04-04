"""
Solar Eclipse Kinematics Simulation: Solar System Frame
=======================================================
This script visualizes a solar eclipse occurring 39 seconds before the 
perfect geometric alignment of the Sun, Moon, and Earth. It is mapped from 
the Solar System barycentric reference frame.

It demonstrates the velocity vectors, line of sight, and the discrepancy 
between absolute geometric position and apparent optical position.

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
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'solar_eclipse_solar_system_frame.mp4')

# --- Precision Physics Constants ---
decimal.getcontext().prec = 50
G = decimal.Decimal('6.67430e-11')
M_sun = decimal.Decimal('1.989e30')
c_dec = decimal.Decimal('299792458')

r_earth_dec = decimal.Decimal('149.6e9')
v_earth_dec = (G * M_sun / r_earth_dec).sqrt()

# --- Triangle Velocity Difference Calculation ---
second_largest_side = (c_dec**2 - v_earth_dec**2).sqrt()
diff_v_dec = c_dec - second_largest_side
diff_v_val = float(diff_v_dec) # Approx 1.48 m/s

# Standard floats for base plotting performance
c = float(c_dec)
v_earth = float(v_earth_dec)
r_earth = float(r_earth_dec)

# --- Moon Physics Logic ---
v_moon_rel = 1022.0  # Moon's orbital speed relative to Earth in m/s
v_moon = v_earth - v_moon_rel 
t_intercept = -1.3   # Time offset when Moon cuts the photon ray

# --- Aberration Angle Calculations ---
theta_earth_dec = v_earth_dec / c_dec
theta_moon_dec = decimal.Decimal(v_moon) / c_dec
diff_theta_dec = abs(theta_earth_dec - theta_moon_dec)

rad_to_arcsec = (180.0 / math.pi) * 3600.0
theta_earth_arcsec = float(theta_earth_dec) * rad_to_arcsec
theta_moon_arcsec = float(theta_moon_dec) * rad_to_arcsec
diff_theta_arcsec = float(diff_theta_dec) * rad_to_arcsec

angle_str = (f"Stellar Aberration Angles:\n"
             f"Earth ($θ_E$): {theta_earth_arcsec:.3f}''\n"
             f"Moon ($θ_M$): {theta_moon_arcsec:.3f}''\n"
             f"Difference ($Δθ$): {diff_theta_arcsec:.3f}''")

# --- Plotting Conversions ---
c_mkm = c / 1e9             # X-axis speed (Million km/s)
r_earth_mkm = r_earth / 1e9 # X-axis position (Million km)

v_kmps = v_earth / 1000       
v_moon_kmps = v_moon / 1000   

# Calculate Moon's constant X position based on intercept time
m_x = r_earth_mkm + c_mkm * t_intercept

# --- Alignment Logic ---
# Calculates geometric alignment (when Sun, Moon, and Earth share equal slopes)
t_align = (-r_earth_mkm * v_moon_kmps * t_intercept) / (v_kmps * m_x - r_earth_mkm * v_moon_kmps)

# UI Labels
v_label = f"$v_{{Earth}} = {v_kmps:.1f}$ km/s"
vm_label = f"$v_{{Moon}} = {v_moon_kmps:.1f}$ km/s"
c_vector_label = f"$c - {diff_v_val:.2f}$ m/s"

# --- Plotting Setup ---
fig, ax = plt.subplots(figsize=(14, 8))

# Expand approach distance along the X-axis
x_margin = 0.2 * c_mkm
ax.set_xlim(149.0, r_earth_mkm + x_margin)

# Clamp the Y-axis tightly in km to emphasize transverse displacement
ax.set_ylim(-4.5 * v_kmps, 60.0)
fig.canvas.draw() 

# Static background references
ax.axhline(0, color='gold', linewidth=2, zorder=0, alpha=0.5, label="Photon Path")
ax.axvline(r_earth_mkm, color='blue', linestyle=':', linewidth=1, zorder=0, alpha=0.3)
ax.axvline(m_x, color='grey', linestyle=':', linewidth=1, zorder=0, alpha=0.3)

ax.set_xlabel('Distance from Sun (Million km)')
ax.set_ylabel('Vertical Displacement (km)') 
ax.set_title("Photon Direction & Trajectory (39s prior to geometric alignment)")
ax.grid(True, linestyle='--', alpha=0.4)

# Static Aberration Angle Box
ax.text(0.02, 0.95, angle_str, transform=ax.transAxes, 
        fontsize=11, color='darkred', fontweight='bold', ha='left', va='top', 
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="darkred", alpha=0.9))

# --- Fixed Vector Setup ---
c_color = '#d9b300' # Dark yellow for visibility
c_y_offset = 10.0  
c_vector_len = 0.16 * c_mkm 
fixed_c_x = 149.4

ax.annotate('', xy=(fixed_c_x + c_vector_len, c_y_offset), xytext=(fixed_c_x, c_y_offset), 
            arrowprops=dict(arrowstyle="-|>", lw=2, color=c_color, shrinkA=0, shrinkB=0, mutation_scale=15))
ax.text(fixed_c_x + c_vector_len / 2, c_y_offset + 2, c_vector_label, 
         ha='center', va='bottom', fontsize=11, color=c_color, fontweight='bold')

# Legend Setup
from matplotlib.lines import Line2D
moon_lw = math.sqrt(60) # Dynamically match linewidth to scatter marker diameter

custom_lines = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='grey', markersize=8),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='orange', markersize=12),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='lightgrey', markersize=12),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='brown', markersize=12, alpha=0.4),
    Line2D([0], [0], color='red', lw=1.5, alpha=0.3, linestyle='--'), 
    Line2D([0], [0], color='red', lw=2), 
    Line2D([0], [0], color='black', lw=moon_lw, linestyle='-'), 
    Line2D([0], [0], color=c_color, lw=2) 
]
ax.legend(custom_lines, [
    'Earth', 'Moon', 'Photon (Active)', 'Photon (Shadow)', 'Moonlight',
    'Line of Sight', 'Direction light+shadow (velocity = $c$)', 
    'Line of Sight (Moon Shadow)', 'Direction Sun at moment of Eclipse'
], loc='lower left')

arrow_props = dict(arrowstyle="-|>", lw=1.5, shrinkA=0, shrinkB=0, mutation_scale=12)
bbox_props = dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.9)

# --- Animation Logic ---
dynamic_artists = []
times = np.linspace(-4, 0.2, 240)
dt_vector = 0.5 # 0.5s look-ahead for velocity vectors

fixed_red_x = 149.3
red_dy = -(v_kmps / c_mkm) * c_vector_len # Matches line of sight slope

def update(frame_idx):
    """Updates rendering arrays per animation frame."""
    for artist in dynamic_artists:
        artist.remove()
    dynamic_artists.clear()
    
    t = times[frame_idx]
    
    # Body Coordinates
    ex, ey = r_earth_mkm, v_kmps * t
    mx, my = m_x, v_moon_kmps * (t - t_intercept) 
    px, py = r_earth_mkm + c_mkm * t, 0
    
    # Lookahead coordinates for vector drawing
    ex_next, ey_next = r_earth_mkm, v_kmps * (t + dt_vector)
    mx_next, my_next = m_x, v_moon_kmps * (t + dt_vector - t_intercept)
    
    # Plot celestial bodies
    earth_dot = ax.scatter(ex, ey, color='blue', s=120, zorder=5)
    moon_dot = ax.scatter(mx, my, color='grey', s=60, zorder=5)
    
    # Handle intercept/shadow logic
    if t >= t_intercept:
        p_color = 'lightgrey'
        p_edge = 'dimgrey'
        moonlight_halo = ax.scatter(px, py, color='brown', s=500, alpha=0.4, zorder=4)
        dynamic_artists.append(moonlight_halo)
    else:
        p_color = 'orange'
        p_edge = 'red'
        
    photon_dot = ax.scatter(px, py, color=p_color, s=150, marker='*', zorder=6, edgecolor=p_edge)
    
    # Timing and UI Tracking text
    t_rel_align = t - t_align
    time_str = f"t = {t_rel_align:.1f} s relative to moment of Geometric Alignment"
                
    time_text = ax.text(0.98, 0.95, time_str, transform=ax.transAxes,
                        va='top', ha='right', fontsize=14, color='black', fontweight='bold', bbox=bbox_props, zorder=10)
                        
    earth_y_text = ax.text(ex - 0.02 * c_mkm, ey - 3.0, f"$y = {ey:.1f}$ km", 
                           va='top', ha='right', fontsize=11, color='blue', fontweight='bold', bbox=bbox_props)
                           
    moon_y_text = ax.text(mx + 0.02 * c_mkm, my + 3.0, f"$y = {my:.1f}$ km", 
                          va='bottom', ha='left', fontsize=11, color='grey', fontweight='bold', bbox=bbox_props)
    
    dynamic_artists.extend([earth_dot, moon_dot, photon_dot, time_text, earth_y_text, moon_y_text])

    # Dynamic Vectors & Lines of sight (Drawn while approaching)
    if t < 0.1:
        # Earth Velocity Vector (Green) 
        earth_arrow = ax.annotate('', xy=(ex_next, ey_next), xytext=(ex, ey), 
                                  arrowprops=dict(**arrow_props, color="green"))
        earth_text = ax.text(ex - 0.02 * c_mkm, ey_next, v_label, 
                             ha='right', va='bottom', fontsize=11, color='green', bbox=bbox_props)
        
        # Moon Velocity Vector (Purple) 
        moon_arrow = ax.annotate('', xy=(mx_next, my_next), xytext=(mx, my), 
                                 arrowprops=dict(**arrow_props, color="purple"))
        moon_text = ax.text(mx - 0.02 * c_mkm, my_next, vm_label, 
                            ha='right', va='bottom', fontsize=11, color='purple', bbox=bbox_props)
        
        dynamic_artists.extend([earth_arrow, earth_text, moon_arrow, moon_text])

        # Red Line of Sight Tracker
        if t < -0.05: 
            red_dashed_arrow = ax.annotate('', xy=(ex, ey), xytext=(px, py), 
                                    arrowprops=dict(**arrow_props, color="red", alpha=0.3, linestyle="--"))
            
            y_on_line = -(v_kmps / c_mkm) * (fixed_red_x - px)
            arrow_y = y_on_line - 5.0
            
            solid_red_arrow = ax.annotate('', xy=(fixed_red_x + c_vector_len, arrow_y + red_dy), 
                                          xytext=(fixed_red_x, arrow_y), 
                                          arrowprops=dict(arrowstyle="-|>", lw=2, color="red", shrinkA=0, shrinkB=0, mutation_scale=15))
            
            mid_y = arrow_y + red_dy / 2
            red_text = ax.text(fixed_red_x + c_vector_len / 2, mid_y + 2.0, "$c$", 
                               ha='center', va='bottom', fontsize=11, color="red", fontweight='bold')
            
            dynamic_artists.extend([red_dashed_arrow, solid_red_arrow, red_text])
            
    # Moon Shadow Extension Line
    ext_y = -(v_kmps / c_mkm) * (m_x - px)
    if ext_y > 0:
        black_line, = ax.plot([px, m_x], [py, ext_y], color='black', linestyle='-', linewidth=moon_lw, alpha=0.7)
        dynamic_artists.append(black_line)

ani = animation.FuncAnimation(fig, update, frames=len(times), interval=33, blit=False)

print(f"Rendering animation to: {output_path} (This may take a moment)")
ani.save(output_path, writer='ffmpeg', fps=30)
print("Finished saving successfully.")