# Script to track Wikimedia Commons page views

This directory contains a Python script, [vandercommonsdatabot.ipynb](https://github.com/HeardLibrary/dashboard/blob/master/gallery/vandercommonsdatabot.ipynb), whose purpose is to use the Wikimedia API to download page view data for Vanderbilt Fine Arts Gallery works whose images are uploaded to Wikimedia Commons, then to upload those data to GitHub. For information about using the script and its license, see the comments in the script.

The data uploaded by the script is in [this CSV file on GitHub](https://github.com/HeardLibrary/dashboard/blob/master/gallery/commons_pageview_data.csv). The column headers are the M IDs of the Commons pages (ID used by the Structured data on Commons Wikibase instance to identify pages).

The metadata about the Commons page (M ID, label, accession number, Q ID, etc.) is in [this CSV file on GitHub](https://github.com/HeardLibrary/dashboard/blob/master/gallery/commons_images.csv)

----
Revised 2021-12-14
