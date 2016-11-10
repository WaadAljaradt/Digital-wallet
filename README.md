# Digital-wallet

This Project is part of the Insight Data fellowship coding challenge. 
In this porject I implemented a fraud detecting system for a digital money transaction between two users

The Project process the input data from the batch input and build an initial graph of users as nodes and transaction that have
been made as an edge relationship between the two users.

The Project then process a streaming data of transaction and outputs values for three features,
Feature_1
if users have done transactions with each other before, the feature_1 will be trust otherwise it would be unverified 

Feature_2:
if the two users had a mutual friend who have done transactions with both of them (ie: inputs are mutual_friends)  then Feature_2
will be trusted otherwise it would be unverified

Feature_3
for users who are within 4 degrees of transaction history with friends the feature_3 would be trusted other wise it would be 
unverified

In my algorithm I used Graph theory to build the intial graph and I processed each stream transaction to find the three features 

The first two levels I traverse using BSF for processing the first two levels. 
if the point is out of the 2nd level I used cached points of the second level and again process for another two levels.
the point is to break the levels of BSF into three parts till finding the path between the two users in the transaction if it 
is within 4 degrees. if not the algorithm will return FOUND = false and have the three features unverified.

After that values of Feature_1, Feature_2, Feature_3 are written to output files.


