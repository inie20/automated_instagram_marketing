# automated_instagram_marketing

## Goal of Code:
I built a small homemade almond milk business and wanted to reach out to new potential customers. So I thought of reaching out to followers of similar brands to mine, basically my competitors. This was an extremely time consuming and repetitive process. Hence, I decided to automate this process via python. 

## Two Steps of the Project 
### Step 1: Get Follower List
We extract all the followers of our competitors page and store it in an excel file with the naming convention followers_{competitors_username}. All of the followers are assigned an index. 

### Step 2: Send DM
We decide how many users we want to send dms to and we set the variable number_of_dms to this. We will get out last index from our logging file from the previous run for this competitor. Then, once we run the script, the message we set will be sent to the followers of our competitior.
