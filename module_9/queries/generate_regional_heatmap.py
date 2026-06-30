"""
Module 9 — Regional Claim-Count Heatmap (India, city-anchored)
====================================================================
CGHS regions (the SS_REGION_ID space used throughout this report) are
city-anchored, not state polygons — e.g. region 9 = Jalandhar, region 4 =
Chandimandir, region 29 = "Delhi 2". A state choropleth would therefore
misrepresent the geography (several regions share one state, and a region's
catchment is centred on its named city, not spread evenly across a state).

Instead this renders each region as a bubble at its city's coordinates,
sized and coloured by that region's claim count (Pattern 1, last 5 FYs) —
the heavier the claim volume passing through a region, the hotter the
bubble. India's state outlines are drawn underneath for geographic context
only; they carry no data themselves.

Output: module_9/data/india_region_heatmap.png
"""

import csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import geopandas as gpd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, 'data')

# Approximate coordinates (lon, lat) for each CGHS region's named city
CITY_COORDS = {
    'Delhi':         (77.21, 28.65),
    'Delhi 2':       (77.05, 28.55),
    'Trivandrum':    (76.94, 8.52),
    'Pune':          (73.86, 18.52),
    'Chandimandir':  (76.85, 30.73),
    'Secunderabad':  (78.50, 17.45),
    'Lucknow':       (80.95, 26.85),
    'Kochi':         (76.27, 9.93),
    'Jaipur':        (75.79, 26.91),
    'Jalandhar':     (75.58, 31.33),
    'Kolkata':       (88.36, 22.57),
    'Ranchi':        (85.31, 23.34),
    'Jammu':         (74.87, 32.73),
    'Chennai':       (80.27, 13.08),
    'Visakhapatnam': (83.22, 17.69),
    'Dehradun':      (78.03, 30.32),
    'Nagpur':        (79.09, 21.15),
    'Bangalore':     (77.59, 12.97),
    'Jabalpur':      (79.95, 23.18),
    'Ahmedabad':     (72.57, 23.02),
    'Guwahati':      (91.74, 26.14),
    'Patna':         (85.14, 25.59),
    'Kanpur':        (80.33, 26.45),
    'Ambala':        (76.78, 30.38),
    'Coimbatore':    (76.96, 11.02),
    'Mumbai':        (72.87, 19.07),
    'Hisar':         (75.72, 29.15),
    'Allahabad':     (81.85, 25.43),
    'Bareilly':      (79.43, 28.35),
    'Bhubaneswar':   (85.84, 20.27),
    'Nepal':         (85.32, 27.70),
    'Yol':           (76.27, 32.10),
    'Meerut':        (77.71, 28.98),
}

def load_csv(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))

def latest(pattern):
    import glob
    files = glob.glob(os.path.join(DATA_DIR, pattern))
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def main():
    region_master = {r['region_id']: r['region_name'] for r in load_csv(os.path.join(DATA_DIR, 'CGHS_Region_Master.csv'))}
    regional = load_csv(latest('01a_Regional_Fraud_Hotspots*.csv'))

    points = []
    for r in regional:
        name = region_master.get(r['region_id'])
        coords = CITY_COORDS.get(name)
        if not coords:
            continue
        points.append({
            'region_id': r['region_id'],
            'name': name,
            'lon': coords[0],
            'lat': coords[1],
            'claims': int(r['claims']),
        })

    print(f"Plotting {len(points)} of {len(regional)} regions (matched to city coordinates)")

    # Full national boundary including claimed territory (J&K/Ladakh up to the
    # Line of Control and Aksai Chin) — NOT the simplified ADM1 states file,
    # which clips the map at the de-facto line and drops PoK/Aksai Chin.
    india = gpd.read_file(os.path.join(DATA_DIR, 'source', 'india_composite.geojson'))

    fig, ax = plt.subplots(figsize=(9, 10))
    india.plot(ax=ax, color='#f2f2f2', edgecolor='#999999', linewidth=0.5, zorder=0)

    claims = [p['claims'] for p in points]
    max_c, min_c = max(claims), min(claims)
    sizes = [200 + 2600 * ((c - min_c) / (max_c - min_c)) for c in claims]

    sc = ax.scatter(
        [p['lon'] for p in points], [p['lat'] for p in points],
        s=sizes, c=[c / 1e5 for c in claims], cmap='YlOrRd', edgecolors='#1a2744', linewidths=0.8,
        alpha=0.85, zorder=3,
    )

    for p in points:
        ax.annotate(f"R-{p['region_id']}", (p['lon'], p['lat']),
                    fontsize=6.5, ha='center', va='center', zorder=4,
                    color='#1a2744', fontweight='bold')

    cbar = fig.colorbar(sc, ax=ax, orientation='horizontal', fraction=0.04, pad=0.03)
    cbar.set_label('Claim Count, in Lakh (1 Lakh = 100,000 claims) — last 5 financial years, higher = hotter',
                    fontsize=8.5)

    ax.set_xlim(67, 98)
    ax.set_ylim(6, 38)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('ECHS Claim Volume by CGHS Region — All India', fontsize=13, fontweight='bold', color='#1a2744', pad=12)

    out_path = os.path.join(DATA_DIR, 'india_region_heatmap.png')
    plt.savefig(out_path, dpi=170, bbox_inches='tight', facecolor='white')
    print(f"Saved -> {out_path}")

if __name__ == '__main__':
    main()
