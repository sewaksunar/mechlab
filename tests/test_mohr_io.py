import os
import numpy as np
from mechlab.mechanics.mos.stress import StressTensor


def test_save_mohr_circle(tmp_path):
    s = StressTensor(10, 30, 15, 7.5, 0, 0)
    out_file = tmp_path / "mohr_test.png"
    s.save_mohr_circle(str(out_file), plane='xy', dpi=50)
    assert out_file.exists()
    # Check file is non-empty
    assert out_file.stat().st_size > 0
    # Clean up (tmp_path fixture handles cleanup)


def test_generate_principal_plot_creates_file():
    s = StressTensor(120, 55, -85, -55, -75, 33)
    out = "mohr_principal_example.png"
    # remove if exists
    try:
        import os
        if os.path.exists(out):
            os.remove(out)
    except Exception:
        pass
    s.plot_principal_mohr(show=False, filename=out)
    assert os.path.exists(out) and os.path.getsize(out) > 0
