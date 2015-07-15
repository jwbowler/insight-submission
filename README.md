Insight Data Engineering Coding Challenge - John Bowler's Submission
===========================================================

Feature 1 uses `mincemeat.py`, provided in `src` - a simple one-file MapReduce implementation. `run.sh` runs a server process (`words_tweeted.py`) and a single client process (`mincemeat.py`), but it is possible to run multiple clients.

Feature 2 depends on `joblib`, available through `[sudo] pip install joblib`. The `median_unique.py` Python script is multithreaded per file: if you split the input file and pass the paths as separate command line arguments, the Python script will process the files in parallel and produce a correctly merged output. (`run.sh` runs it only on a single file.)
