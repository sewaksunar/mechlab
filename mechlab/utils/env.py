"""Environment detection utilities."""


def is_jupyter():
    """
    Check if code is running in a Jupyter notebook environment.
    
    Returns:
        True if running in Jupyter, False otherwise
    """
    try:
        from IPython import get_ipython
        return get_ipython() is not None
    except ImportError:
        return False
