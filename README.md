# Secure-Scripting
Repository for the project from college class "Secure Scripting"

Python script developed in WSL.

Should work out of box.

# Uses
This script only works on data provided from: https://coinmetrics.io/community-network-data/

Sample data from October of 2021 is provided in this repository but new data should still be compatible.

1. From terminal:
    python3 AnalyzeCryptoPrice.py
* This method analyzes all data in provided file

2. From terminal:
    python3 AnalyzeCryptoPrice.py date date
* This method analyzes data only between provided dates

# Results
The script will provide a histogram in terminal and save the data in relevant ranges to a csv file for later use, if needed.
