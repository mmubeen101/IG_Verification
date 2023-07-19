import json,datetime
import re
import requests
from apify_client import ApifyClient




# with open("ig-scrapper/dataset_instagram-scraper_2023-07-11_06-57-38-578.json") as profile_info:
#     profile_data = json.load(profile_info)

# # Print the data
# print(len(profile_data))

# for i in profile_data['']:
#     print(i)
#     print('\n')


def is_legit(profile_data) -> bool:
    
    highestLikes = -100000000000000
    highestComments = -10000000000

    if profile_data["verified"]:

        return True
     
    if profile_data["isBusinessAccount"]:

        if profile_data["joinedRecently"] and not profile_data["profilePicUrl"]  and (profile_data["followersCount"] < 500 and profile_data["followersCount"] < profile_data["followsCount"]) and profile_data["biography"] == "":
            return False
        else:
            return True

    else:
        points = [0,2,4,6,8,10]
        pointsCount = 0


        # if profile_data["followersCount"] > 150:

        #     diff = profile_data["followersCount"] - 150
        #     if diff >= profile_data["followersCount"]:
        #         pointsCount+=points[5]
        #     elif diff > 0.75 * profile_data["followersCount"]:
        #         pointsCount+=points[4]
        #     elif diff > 0.50 * profile_data["followersCount"]:
        #         pointsCount+=points[3]
        #     elif diff > 0.25 * profile_data["followersCount"]:
        #         pointsCount+=points[2]
        #     elif diff >= 0.01 * profile_data["followersCount"]:
        #         pointsCount+= points[1]
        #     else:
        #         pointsCount+=points[0]


        
        if profile_data["followersCount"] > 150 :

            diff = profile_data["followersCount"] - 150
            if diff >= 150:
                pointsCount+=points[5]
            elif diff > 0.75 * 150:
                pointsCount+=points[4]
            elif diff > 0.50 * 150:
                pointsCount+=points[3]

            elif diff > 0.25 * 150:
                pointsCount+=points[2]
            elif diff >= 0.01 * 150:
                pointsCount+= points[1]
            else:
                pointsCount+=points[0]
            # print(pointsCount)
        else:
            if profile_data["postsCount"] > 100:
                # utc = pytz.utc

                # # Get the current datetime in UTC
                # now = datetime.datetime.now(tz=utc)
                

                # # Format the datetime as an ISO 8601 string in UTC timezone
                # iso_8601_string = now.isoformat(timespec='milliseconds') + 'Z'
                # print(type(iso_8601_string.split('T')[0]))
                for i in profile_data["latestPosts"]:

                    timestamp_obj = datetime.datetime.strptime(i["timestamp"], '%Y-%m-%dT%H:%M:%S.%f%z')
                    # print(type(timestamp_obj))
                    today = datetime.datetime.now(datetime.timezone.utc)
                    time_diff = (today - timestamp_obj).days
                    # print(time_diff)


                    if time_diff > 1095:
                        pointsCount+=points[0]
                    elif time_diff > 730:
                        pointsCount+=points[1]
                    elif time_diff > 545:
                        pointsCount += points[2]
                    elif time_diff > 365:
                        pointsCount += points[3]
                    elif time_diff > 60:
                        pointsCount += points[4]
                    elif time_diff > 30:
                        pointsCount += points[5]
            # print(pointsCount)

        for i in profile_data["latestPosts"]:

            if i["likesCount"] > highestLikes:
                highestLikes = i["likesCount"]
            
            if i["commentsCount"] > highestComments:
                highestComments = i["commentsCount"]

        if highestLikes > 0.5 * profile_data["followersCount"]:
            pointsCount+=points[5]
        elif highestLikes > 0.3 * profile_data["followersCount"]:
            pointsCount+=points[4]
        elif highestLikes > 0.25 * profile_data["followersCount"]:
            pointsCount+=points[3]
        elif highestLikes > 0.15 * profile_data["followersCount"]:
            pointsCount+=points[2]
        elif highestLikes > 0.05 * profile_data["followersCount"]:
            pointsCount+=points[1]
        else:
            pointsCount+=points[0]
        # print("After Likes" ,pointsCount)

        if highestComments > 0.1 * profile_data["followersCount"]:
            pointsCount+=points[5]
        elif highestComments > 0.08 * profile_data["followersCount"]:
            pointsCount+=points[4]
        elif highestComments > 0.06 * profile_data["followersCount"]:
            pointsCount+=points[3]
        elif highestComments > 0.04 * profile_data["followersCount"]:
            pointsCount+=points[2]
        elif highestComments > 0.02 * profile_data["followersCount"]:
            pointsCount+=points[1]
        else:
            highestComments+=points[0]
        
        # print("Points :::====>", pointsCount)

        if pointsCount >= 15 :
            return True
        else:
            return False
                    



if __name__ == "__main__":
    
    with open("/Users/mubeen/Documents/OneFi/Optimization_Code/ig-scrapper/dataset_instagram-scraper_2023-07-11_07-02-18-234.json") as profile_info:
        profile_data = json.load(profile_info)

    url = input("Enter the instagram URL ")

    # Define a regular expression to match a URL
    url_regex = re.compile(r"^https?://.*instagram\.com/.*$")

    print(url_regex.match(url))
    while not url_regex.match(url):
         print("Invalid URL format. Please enter a valid URL starting with 'http://' or 'https://'.")
         url = input("Enter the instagram URL ")

    print(url) 


    # auth = f"https://api.instagram.com/oauth/authorize?client_id=642334427495095&redirect_uri=onefiadrian.github.io&scope=user_profile,user_media&response_type=code"
    client = ApifyClient("apify_api_ckVoz1xe0eaZAjfwPGFZTxl3XsKAc83DgGbQ")


    # response = requests.get(auth)
    # print(response.content)


    # Prepare the Actor input
    run_input = {
        # ["https://www.instagram.com/manhohin0516"]
        "directUrls": [url] ,
        "resultsType": "details",
        "resultsLimit": 200,
        "searchType": "hashtag",
        "searchLimit": 1,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        },
        "maxRequestRetries": 11,
        "extendOutputFunction": """async ({ data, item, helpers, page, customData, label }) => {
    return item;
    }""",
        "extendScraperFunction": """async ({ page, request, label, response, helpers, requestQueue, logins, addProfile, addPost, addLocation, addHashtag, doRequest, customData, Apify }) => {
    
    }""",
        "customData": {},
    }

    # Run the Actor and wait for it to finish
    run = client.actor("apify/instagram-scraper").call(run_input=run_input)
    

    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        # print(item)
        data = item 

    # print(client.dataset(run["defaultDatasetId"]).iterate_items())



    # print(type(profile_data[0])) 
    profile_data = profile_data[0]
    # print(profile_data["verified"])

    print(is_legit(data))