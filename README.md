## Installation
Requires Python 3.4 or higher. Install dependencies with:

```python
pip install -r requirements.txt
```

## Usage

Run `pull_data.py` to retrieve TI6 match data from the OpenDota API (stored in the `data` folder, which will be created 
if necessary). `parse.py` then extracts potentially-interesting features from the data and spits out
 `ti6.csv`.