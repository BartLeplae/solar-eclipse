# Stellar Aberration & Solar Eclipse Kinematics Simulaton

This project contains a suite of Python simulations that visualize the kinematics of light travel and the relativistic effects of stellar aberration within the solar system. Using high-precision mathematical calculations (decimal library) and matplotlib animations, these scripts demonstrate how local orbital velocities affect the apparent speed and direction of incoming photons (light) during solar eclipses and deep-space travel.

The computational model treats every point in the solar system as a local inertial frame; essentially a "pocket" of space moving at a specific speed. Each pocket moves at the exact same Keplerian orbital velocity that a planetary mass would exhibit at that specific heliocentric distance. For our planet, this is formally designated as the Earth-Centered Inertial (ECI) frame.

Any kinematic motion relative to a local inertial frame induces time dilation, a relativistic effect that is directly measurable using atomic clocks. 

The relative motion between distinct local inertial frames manifests as an angular shift in the propagation direction of incident light. This angular deviation is strictly governed by the equations of relativistic aberration, which ensures that the invariant speed of light, c, is preserved within the moving local inertial frame.

To understand how light behaves when moving between these frames, imagine a boat crossing a flowing river:
* The Stationary Observer: If you are standing still on the riverbank (representing a static frame relative to the Sun), a boat trying to cross straight to the other side will appear to move slower. This is because a component of the boat's total velocity is expended fighting the current just to stay on track.
* The Solar System: In this simulation, light acts like that boat. When viewed from a "static" Solar System perspective, light moving sideways across the path of a moving planetary frame appears mathematically attenuated because it is traversing a moving frame.

Despite these complex shifts, the physics remains consistent for us on Earth:
* Lunar vs. Solar Light: Photons propagating from the Moon to the Earth travel at exactly c. Even though light from the Sun or distant stars has traveled much further, by the time it reaches Earth's "pocket" of space, it follows the same local rules, exhibiting identical velocity vectors and kinematic behavior upon reaching the observer.
* Personal Motion: Your own velocity (like the Earth spinning or a satellite orbiting) relative to the local inertial frame introduces an additional, complementary aberration component.
* If a space telescope traveling in the opposite orbital direction of the Earth observed the Sun and Moon at the exact moment of a solar eclipse, it would see both bodies shifted by roughly 20.5 arcseconds. The complementary aberration caused by the observer's velocity vector shift the apparent images of the Sun and Moon by the exact same angular amount and continue to perfectly overlap. The Sun would thereby appear in its actual direction, because the 20.5-arcsecond shift caused by stellar aberration and the 20.5-arcsecond shift caused by complementary aberration cancel each other out.

## Folder Structure
* `src/`: Contains the Python scripts used to calculate the physics and generate the animations.
* `graphs/`: The designated output directory where the resulting MP4 animations are saved.

## Included Scripts

1. **`stellar_aberration_earth_moon_solar_system_frame.py`**
   * **Purpose**: Maps a solar eclipse from the Solar System barycentric reference frame. It focuses on the timeframe roughly 39 seconds prior to perfect geometric alignment, highlighting the velocity vectors of the Earth and Moon, the line of sight, and the Moon's casted shadow.

2. **`stellar_aberration_earth_frame.py`**
   * **Purpose**: Simulates a solar eclipse specifically from the Earth's rest frame. It calculates and visualizes the exact stellar aberration angles for both the Earth and the Moon, demonstrating how light and shadows behave relative to a stationary Earth.

3. **`stellar_aberration_solar_system.py`**
   * **Purpose**: Visualizes a photon's continuous journey from the Sun outward past Jupiter. It dynamically calculates the subtle relativistic timing differences (in nanoseconds) and apparent speed discrepancies experienced across different local inertial frames as the photon travels deeper into the solar system.

## Environment Setup & Installation

This project uses Conda to manage both Python dependencies and system tools required for video generation (like `ffmpeg`). 

1. Ensure you have [Anaconda](https://www.anaconda.com/) or Miniconda installed.
2. Clone this repository and navigate to the project folder in your terminal.
3. Create the required environment by running:
   ```bash
   conda env create -f environment.yml
   ```
4. Activate the environment:
   ```bash
   conda activate stellar-aberration-env
   ```

## Execution

Run the scripts from within the src/ directory. They operate independently and can be run in the following order:
   ```bash
   python stellar_aberration_earth_moon_solar_system_frame.py
   python stellar_aberration_earth_frame.py
   python stellar_aberration_solar_system.py
   ```

## Results & Outputs

Executing the scripts will populate the `graphs/` directory with three high-definition MP4 animations, each illustrating different relativistic and kinematic concepts:

***`solar_eclipse.mp4`***(Generated by `stellar_aberration_earth_moon_solar_system_frame.py`)*
  Mapped from the Solar System barycentric reference frame, this animation focuses on the 39 seconds immediately prior to perfect geometric alignment. It graphically breaks down the discrepancy between the apparent optical position and the true geometric position of the Sun, Moon, and Earth, heavily utilizing dynamic tracking vectors for orbital velocities and the speed of light (c).

***`solar_eclipse_earth_frame.mp4`***(Generated by `stellar_aberration_earth_frame.py`)*
  This animation visualizes a solar eclipse from the Earth's rest frame. It demonstrates an active photon stream transitioning into a shadow upon intersecting the Moon. The visualization includes a real-time UI that tracks the exact stellar aberration angles for both the Earth and the Moon, as well as the relative geometric alignment timings.

***`photon_animation_jupiter.mp4`***(Generated by `stellar_aberration_solar_system.py`)*
  A logarithmic-scale animation tracking a photon's continuous journey from the Sun outward past Jupiter. The interface features a high-precision timer that dynamically tracks the accumulated relativistic delays (in nanoseconds) and apparent speed discrepancies experienced across different local inertial frames as the photon crosses planetary orbits.

