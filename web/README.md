# Documentation

Created: December 6, 2022 1:46 PM
Last Edited Time: December 7, 2022 11:14 AM

## Motivation

To understand this project, you will need to some domain knowledge of the game Go. Go requires two players, one player playing black and the other white. They take turns playing and the game ends when two players come into agreement that there is nowhere to put the stones. Winner is determined by the number of territory the player has, and whoever has more territories win.

This project is an analysis of sequences played in Go games. In the Go industry, there are various established openings which are mentioned “ideal”. This makes the variety of opening sequences that appears in many Go games very limited to few numbers while the space of the game is “unlimited”. 

When professional Go players play amongst each other, we can observe that they play opening sequences that is known to have highest win-rate respective to their situation on the board. Another observation that we can make is that their choices are prune to change if they discover new and better sequences. For example, after the advent of artifical intelligence, the change was significant because players started following how artificial intelligence plays. This project is created to show this phenomenon of players’ choices of opening sequeneces changing throughout different eras.

## Overview of Design

From a higher level perspective, this project leverages the startegy of lambda architecture. This architecture is very helpful when working with Big Data projects, where we have to deal with large datasets and constantly incoming data. Due to using lambda architecture, the project can be described in 5 different parts: Data Lake, Batch Layer, Serving Layer, Speed Layer, and the Frontend.

### Data Lake

Currently the data lake is located in S3 bucket. All data is originally incoming in zip files, and each zip files contain number of [sgf](https://en.wikipedia.org/wiki/Smart_Game_Format) files. Initial dataset around 80 zip files and new zip files are added to this data lake every week. 

To initially start the project, I simply moved all the zip files into the S3 bucket, but for updates, there is a pipeline (name?) where I give the path to the zip file, it will be uploaded to S3 bucket.

### Batch Layer

This layer is responsible for many jobs in this project. First, it is responsible for converting raw data into a desired sql database format. To make this work, I have created a local library which parses SGF file into data object format. This object will be stored into SQL eventually where each row represents a node (move) of a game. Each node has a parent node and a list of child nodes, which basically makes my entire dataset mimic a behavior of a tree. 

After creating this tree, my sql file is stored as `<year>.sql` in batch layer of sql. Because I have sharded the entire dataset by years, we have multiple sql files. The sql databses created with computations in this layer will be used in serving layer. 

To create a batch view that we want to send to serving layer, we now merge all shareded sql files and compute win and pick rates for each sequences. A batch view will be created here where each row includes the node id with their pick and win rates every year. This view will be uploaded to the serving S3 bucket that is responsible for serving layer.

### Serving Layer

S3 bucket exists for serving layer and it contains the batch views. The serving layer is responsible for uploading the latest batch view to the client side API. Therefore, client side queries will use the latest database that is listed in the view. 

### Speed Layer

This project will most likely only update data every one week. (I am under a subscription of receiving data, and I receive them every week). Due to the natural behavior of this project of having infrequent updates to the database, it isn’t entirely necessary to have a realtime view at this moment. However, to enhance scalability of this project and possibility of having more frequent updates in datasets in the future, I have decided to use some strategies of speed layer. This speed layer is responsible for updating win and pick rates. 

One assumption that is taken when doing updates for realtime views are that incoming datasets are only games from current year. We do this to take advantage of how we display win and pick rates by year. 

To do this as I get a sequence, I can increment attributes of corresponding nodes. The tables store numerator and denominator values separately, and this allows me to only increment these values by 1 if we need to. So the update process is rather cost-friendly. 

However, there is a downside of this approach. When we increment the denominator and numerator value for a specific node, we ideally have to increment values for all nodes in the same level. However, this gets very expensive and there is no point of having a speed layer then. So I am sacrificing accuracy over pace of delivery. Although the accuracy won’t be perfect, I do see that since we are incrementing by 1 out of 10000+ games, the percentage won’t differ significantly.

This creates a new realtime view and we store it in the API. 

### Frontend

Here, we have an API that delivers data from API to React Frontend. The API is deployed on AWS Lambda. The frontend is deployed on Vercel. On the right, we see popular moves that is made as a next move from the left side board. The charts on the side represents the pick and win rates for that specific choice of move. When we click on one of the possible moves, it will re-fetch new data and display accordingly.

## Looking into the codebase

There are two main things to consider: `batch_view.sh` and `realtime_view.sh`. `batch_view.sh` is a pipeline that creates a new batch view with incoming data. This pipeline should be ran after uploading new dataset on AWS S3 bucket that deals with the batch layer. This first goes runs three scripts, `fan_out.py`, `mapper.py`, `precompute.py`, that deals with processing, sharding, and precomputing the data. After that we run `deploy.py` in serving layer which is responsible for uploading the view into the serving layer S3 Bucket and moving the view to API. Lastly it will deploy the API with the new view.

The `realtime_view.sh` is simpler. As we have a new dataset, we will run `realtime_update.py` with the new dataset zip folder. This will parse and update the realtime view that lives in the API. Also, it will upload the new realtime view to S3 Bucket for speed layer. Lastly, it will deploy the lambda function.

The frontend portion of the code lives in `/frontend` and it is a NextJS based web application. The deployed version can be found [here](http://www.trenduk-go.com). (if it doesn’t work try [this](https://trenduk.vercel.app))