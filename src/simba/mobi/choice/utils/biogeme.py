import os
from pathlib import Path

import biogeme.biogeme as bio


def estimate_in_directory(
    biogeme_instance: bio.BIOGEME, directory: Path
) -> bio.res.bioResults:
    """Estimate with biogeme and save results in a directory."""
    cwd = os.getcwd()
    os.chdir(directory)
    # Estimate the parameters
    results = biogeme_instance.estimate()
    os.chdir(cwd)
    return results
