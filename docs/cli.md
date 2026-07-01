# CLI Reference

## `mechlab beam`

Analyze a simply-supported beam under point and distributed loads.

```bash
python -m mechlab beam \
    --length 4.0 --E 200e9 --yield 250e6 \
    --I 9.19e-6 --area 2.3e-3 --c 0.076 \
    --support 0.0 --support 4.0 \
    --point-load 2.0 5000
```

| Flag | Required | Description |
|---|---|---|
| `--length` | yes | Beam length (m) |
| `--E` | yes | Young's modulus (Pa) |
| `--yield` | yes | Material yield strength (Pa) |
| `--I` | yes | Moment of inertia (m⁴) |
| `--area` | yes | Cross-sectional area (m²) |
| `--c` | yes | Extreme fiber distance (m) |
| `--support` | yes, ×2 | Support position (m). Pass twice for the two supports. |
| `--point-load` | no, repeatable | `POSITION MAGNITUDE` — pass multiple times for multiple loads |

### Example output

```
=== Beam Analysis Report ===

Reactions:
  x = 0.000 m  ->  R = 2500.00 N
  x = 4.000 m  ->  R = 2500.00 N

Max bending stress : 41.35 MPa at x = 2.00 m
Safety factor       : 6.05
```
