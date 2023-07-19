# IG_Verification

# Instagram Verification

This is a Python script to verify the legitimacy of an Instagram account. The script uses a set of rules to determine if a given Instagram account is legitimate or not. The rules include things like the number of followers, the number of likes and comments on the account's posts, and the age of the account.

## Installation

To run this code, you'll need to have Python 3 installed on your system. You'll also need to install the required packages using the following command:

```python
pip install -r requirements.txt
```

## Usage

To use this script, run the following command from the terminal or command prompt:

```python
python3 is_validated.py
```

The script will prompt you to enter the URL of the Instagram account you want to verify. Enter the URL and press Enter. The script will then use the Apify API to scrape data from the Instagram account and run it through a set of rules to determine if the account is legitimate or not. 

The output will be either "True" or "False", indicating if the account is legitimate or not.

Note: This script requires an Apify API key to access the Instagram scraper. You will need to replace the `apify_api_ckVoz1xe0eaZAjfwPGFZTxl3XsKAc83DgGbQ` with your own API key in the script.