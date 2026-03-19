import re
import json
import requests
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Body IDs — JPL Horizons identifiers for each body
# ---------------------------------------------------------------------------
BODY_IDS = {
    'mercury':  199,
    'venus':    299,
    'earth':    399,
    'mars':     499,
    'jupiter':  599,
    'saturn':   699,
    'uranus':   799,
    'neptune':  899,
    'pluto':    999,
    'ceres':    2000001,       # Dwarf planet
    'eris':     136199,
    'makemake': 136472,
    'haumea':   136108,
}

HORIZONS_URL = 'https://ssd.jpl.nasa.gov/api/horizons.api'
CACHE_FILE   = 'solar_system_cache.json'


# ---------------------------------------------------------------------------
# Core fetch function
# ---------------------------------------------------------------------------
def fetch_body_state(body_id, date=None):
    """
    Fetch position and velocity for a single body from JPL Horizons.

    Parameters
    ----------
    body_id : int
        JPL Horizons numeric ID for the body.
    date : str, optional
        Date string 'YYYY-MM-DD'. Defaults to today.

    Returns
    -------
    dict with keys x, y, z, vx, vy, vz  (all in meters / meters-per-second)
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    stop = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

    params = {
        'format':     'json',
        'COMMAND':    str(body_id),
        'CENTER':     '500@10',     # Heliocentric (Sun centre)
        'EPHEM_TYPE': 'VECTORS',
        'START_TIME': date,
        'STOP_TIME':  stop,
        'STEP_SIZE':  '1d',
        'VEC_TABLE':  '2',          # Position + velocity
        'REF_PLANE':  'ECLIPTIC',
        'OUT_UNITS':  'KM-S',       # km and km/s
    }

    response = requests.get(HORIZONS_URL, params=params, timeout=10)
    response.raise_for_status()
    data   = response.json()
    result = data['result']

    # Extract the data block between $$SOE and $$EOE markers
    soe   = result.index('$$SOE')
    eoe   = result.index('$$EOE')
    block = result[soe:eoe]

    # Parse X, Y, Z, VX, VY, VZ from the block
    values = {}
    for var in ['X', 'Y', 'Z', 'VX', 'VY', 'VZ']:
        if var.startswith('V'):
            # Velocity: straightforward match
            pattern = rf'{var}\s*=\s*([+-]?[\d.]+[Ee][+-]?\d+)'
        else:
            # Position: negative lookbehind prevents matching VX when seeking X
            pattern = rf'(?<![V]){var}\s*=\s*([+-]?[\d.]+[Ee][+-]?\d+)'

        match = re.search(pattern, block)
        if match:
            values[var] = float(match.group(1))
        else:
            raise ValueError(f'Could not parse {var} for body {body_id} on {date}')

    return {
        'x':  values['X']  * 1000,   # km  → m
        'y':  values['Y']  * 1000,
        'z':  values['Z']  * 1000,
        'vx': values['VX'] * 1000,   # km/s → m/s
        'vy': values['VY'] * 1000,
        'vz': values['VZ'] * 1000,
    }


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------
def load_cached():
    """
    Load today's cached body data from disk, if it exists and is fresh.

    Returns
    -------
    dict of body states, or None if cache is missing / stale.
    """
    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
        if cache.get('date') == datetime.now().strftime('%Y-%m-%d'):
            return cache['bodies']
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass
    return None


def save_cache(bodies_data):
    """
    Write today's body data to the cache file.

    Parameters
    ----------
    bodies_data : dict
        Mapping of body name → state dict {x, y, z, vx, vy, vz}.
    """
    cache = {
        'date':   datetime.now().strftime('%Y-%m-%d'),
        'bodies': bodies_data,
    }
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)
    print(f'  Cache saved to {CACHE_FILE}')


# ---------------------------------------------------------------------------
# Fetch all bodies
# ---------------------------------------------------------------------------
def fetch_all_positions():
    """
    Return real-time positional data for all bodies in BODY_IDS.

    Tries the on-disk cache first; falls back to live API calls.
    If all API calls fail, returns an empty dict (callers should use
    fallback positions).

    Returns
    -------
    dict  { 'mercury': {x, y, z, vx, vy, vz}, ... }
    """
    # --- Try cache first ---
    cached = load_cached()
    if cached is not None:
        print('Using cached positions (JPL Horizons)')
        return cached

    # --- Live fetch ---
    print('Fetching positions from JPL Horizons...')
    results = {}
    for name, body_id in BODY_IDS.items():
        try:
            print(f'  Fetching {name.capitalize()}...')
            results[name] = fetch_body_state(body_id)
        except Exception as e:
            print(f'  FAILED: {name.capitalize()} — {e}')

    if results:
        save_cache(results)
    else:
        print('  WARNING: No data retrieved. Fallback positions will be used.')

    return results


# ---------------------------------------------------------------------------
# Planet factory helper
# ---------------------------------------------------------------------------
def create_planet(Planet, name, fallback_x, fallback_y_vel,
                  radius, color, mass, real_data):
    """
    Construct a Planet using real JPL data when available, or hardcoded
    fallback values otherwise.

    Parameters
    ----------
    Planet        : class  — your Planet class
    name          : str    — body name, e.g. 'Mercury'
    fallback_x    : float  — fallback x position in metres (on x-axis)
    fallback_y_vel: float  — fallback circular orbital velocity in m/s
    radius        : int    — display radius in pixels
    color         : tuple  — RGB colour
    mass          : float  — mass in kg
    real_data     : dict   — output of fetch_all_positions()

    Returns
    -------
    Planet instance
    """
    key = name.lower()

    if key in real_data:
        d = real_data[key]
        planet        = Planet(name, color, mass, d['x'], d['y'], radius)
        planet.x_vel  = d['vx']
        planet.y_vel  = d['vy']
        print(f'  {name}: using real JPL position')
    else:
        planet = Planet(name, color, mass, fallback_x, 0, radius, fallback_y_vel)
        print(f'  {name}: using fallback position')

    return planet


# ---------------------------------------------------------------------------
# Example / quick test  (run this file directly to test the API)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print('Testing JPL Horizons fetch...\n')
    try:
        state = fetch_body_state(399)   # Earth
        print('Earth state vector (metres / m/s):')
        for k, v in state.items():
            print(f'  {k:3s} = {v:.6e}')
    except Exception as e:
        print(f'Fetch failed: {e}')

    print('\nFetching all bodies...')
    data = fetch_all_positions()
    print(f'\nRetrieved data for: {", ".join(data.keys())}')