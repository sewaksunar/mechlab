"""MechLab Demonstration Examples

Comprehensive examples showcasing MechLab capabilities:
  1. Projectile Motion with Animation
  2. Stress Analysis and Mohr's Circle
  3. Unit Conversions
  4. 3D Stress Transformations (Symbolic)

Run with: python -m examples.demo
"""

from __future__ import annotations

import numpy as np


def demo_projectile():
    """Example 1: Projectile motion with unified animator."""
    print("=" * 60)
    print("EXAMPLE 1: Projectile Motion")
    print("=" * 60)

    from mechlab.mechanics.dynamics import Projectile
    from mechlab.visual import animate

    # Create projectile: 20 m/s at 45°
    v0 = 20.0
    angle = np.radians(45)
    proj = Projectile(
        position=(0, 0, 0),
        velocity=(v0 * np.cos(angle), v0 * np.sin(angle), 0),
        mass=1.0,
    )

    # Query physics
    print(f"  Launch: {v0:.1f} m/s at 45°")
    print(f"  Range: {proj.range():.2f} m")
    print(f"  Max height: {proj.max_height():.2f} m")
    print(f"  Time of flight: {proj.time_of_flight():.2f} s")

    # Position at t=1s
    state = proj.state_at_time(1.0)
    print(f"  At t=1s: position={state.position}, velocity={state.velocity}")

    # Animate (uncomment to display or save)
    anim = animate(proj)
    print(f"  ✓ Created animator: {type(anim).__name__}")
    # anim.preview()
    # anim.save_gif("projectile.gif")
    print()


def demo_stress():
    """Example 2: Stress analysis and Mohr's circle."""
    print("=" * 60)
    print("EXAMPLE 2: Plane Stress Analysis")
    print("=" * 60)

    from mechlab.mechanics import StressState

    stress = StressState(100, 50, 25, unit="MPa")
    results = stress.results()

    print("  Input: σx=100, σy=50, τxy=25 MPa")
    print(f"  Principal: σ1={results['σ1']:.2f}, σ2={results['σ2']:.2f} MPa")
    print(f"  Max shear: τmax={results['τmax']:.2f} MPa")
    print(f"  Von Mises: σvm={results['von_mises']:.2f} MPa")
    print()


def demo_units():
    """Example 3: Unit conversions."""
    print("=" * 60)
    print("EXAMPLE 3: Unit Conversions")
    print("=" * 60)

    from mechlab.units import convert

    conversions = [
        (100, "MPa", "psi"),
        (1, "m", "ft"),
        (1, "m3", "L"),
    ]

    for value, from_unit, to_unit in conversions:
        result = convert(value, from_unit, to_unit)
        print(f"  {value} {from_unit} = {result:.4f} {to_unit}")
    print()


def demo_stress_transform():
    """Example 4: Symbolic 3D stress transformation."""
    print("=" * 60)
    print("EXAMPLE 4: Symbolic Stress Transformation")
    print("=" * 60)

    try:
        import sympy as sp
        from mechlab.mechanics.statics.stress import StressTransform

        st = StressTransform()

        # Identity rotation (no change)
        values = {
            st.sxx: 100, st.syy: 50, st.szz: 75,
            st.sxy: 20, st.syz: 15, st.sxz: 10,
            st.l1: 1, st.m1: 0, st.n1: 0,
            st.l2: 0, st.m2: 1, st.n2: 0,
            st.l3: 0, st.m3: 0, st.n3: 1,
        }

        sigma_transformed = sp.Matrix(st.transform()).subs(values)
        print("  Identity transform (σ' = σ):")
        print(f"    σxx'={float(sigma_transformed[0, 0]):.1f}")
        print(f"    σyy'={float(sigma_transformed[1, 1]):.1f}")
        print(f"    σzz'={float(sigma_transformed[2, 2]):.1f}")
    except ImportError:
        print("  ⚠ SymPy not installed. Skipping symbolic example.")
    print()


def demo_animation_export():
    """Example 5: Export animations (commented by default)."""
    print("=" * 60)
    print("EXAMPLE 5: Animation Export (demo code)")
    print("=" * 60)
    print("""
    # Projectile GIF:
    from mechlab.mechanics.dynamics import Projectile
    from mechlab.visual import animate
    proj = Projectile(velocity=(20, 20, 0))
    anim = animate(proj)
    anim.save_gif('projectile.gif', fps=20)

    # Stress animation:
    from mechlab.visual import StressAnimation
    stress_anim = StressAnimation(100, 50, 25)
    stress_anim.save_gif('stress.gif')

    # 3D cube projection:
    from mechlab.visual import animate_cube
    animate_cube(save='cube.gif')
    """)


def main():
    """Run all demos."""
    print("\n🔬 MECHLAB DEMONSTRATION\n")

    demo_projectile()
    demo_stress()
    demo_units()
    demo_stress_transform()
    demo_animation_export()

    print("=" * 60)
    print("✓ All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
