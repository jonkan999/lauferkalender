### INPUT SCRIPTS ###

# program_configuration.py
import sys

from extraction import (
    extract_data_laufen,
    extract_data_runme
)
from scraper_package.race_classes import Race, RaceCollection
from transform_race import transform_and_store_race

def run_all_scraper_scripts():
    print("Running all scraper scripts")
    extract_data_laufen.main()
    extract_data_runme.main()
    #extract_data_jogg_road.main()
    #extract_data_jogg_trail.main()
    #extract_data_trailkalendern.main()

if __name__ == "__main__":
    try:
        run_all_scraper_scripts()
    except Exception as e:
        print(e)
        sys.exit()
