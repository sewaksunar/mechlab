"""Plane stress example using MechLab."""

from mechlab.mechanics import StressState


def main() -> None:
    stress = StressState(100, 50, 25, unit="MPa")
    results = stress.results()

    print("Plane Stress Results")
    for key, value in results.items():
        if key == "unit":
            continue
        print(f"{key:>10} = {value:.3f} {results['unit']}")


if __name__ == "__main__":
    main()
