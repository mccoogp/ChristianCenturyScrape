# ChristianCenturyScrape
Instructions:

Run CreateCenturyDf.py to create an empty csv to work with.

After this run ScrapeCenturyArts.py. This will open a new chrome window and you will have 30 seconds to sign into Christian Century on this new tab. After that, the code should go through every link in CenturyArts.csv which is every link from May 1998 to late february 2026. If you want to get more recent results, rerun GetArts.py. A likely bug you will run into is chrome version. I have it set to main version 149 on line 20, but you are able to edit this. Aditionally you will need to run "pip3 install selenium pandas undetected-chromedriver webdriver-manager" in the terminal or some version of this to install these python libraries.
