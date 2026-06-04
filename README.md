# Task3-GSG-ChessGame


/////////////       Quality Data Report                  //////////////////////

#  ///// Origin Data Set Status ////

// in chess 
chess data shape is (20058, 17)

//in player
players data shape is (215, 9)

# ///////////// I take Decisions /////////////////////

// in chess
1- drop "opening_response" because most data to this col is null 
2- drop all duplicated rows in chess data
3- drop rows that contain null in these columns [rated - black_id - white_id]
4- I drevied two columns  ["time_base", "time_sec"] From Time-increment columns
5- I create [rated_diff] columns and it contains on white_rating col sub white_rating col

// in players
1- drop rows that contain null in these columns [username]
2- drop all duplicated rows in chess data
3- I create [country_columns] because merge the same country
4- 

#  ///// output Data Set cleaned ////

// in chess 
new shape is (20058, 22)

//in player
new shape is (215, 10)











