import sys
import os

# Add the parent directory (project folder) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Scrape_brockercheck import main


print(main())
