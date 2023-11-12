# Multi-Threaded-Network-Server
Multi-Threaded Network Server for Pattern Analysis

NOTE: We have put in a lot of time and effort and so please make sure to run PART_B.py or assignment3-PART_B.py ---> this is what contains our PART B code. 

PART A: 

server_side command: python3 assignment3.py -l 12345 -p "little"
client-side commands look like: 
nc localhost 12345 -i 1 <bookA.txt
nc localhost 12345 -i 1 <bookB.txt


PART B: 

server_side command: python3 assignment3-PART_B.py -l localhost -p "little"
client-side commands look like:
nc localhost 12345 -i 1 <bookA.txt
nc localhost 12345 -i 1 <bookB.txt


Our code/implementation fulfills all three requirements of the assignment: 
Pattern analysis frequency is correct   (10%)
Results printed at intervals  (5%)
Book titles sorted by the most frequent occurrences of the selected pattern  (5%)


For example, when you run the command: python3 assign3.py -l localhost -p "world", for two books each on different connection, then the outcome would look something like this:

(Note: results are printed at intervals; while also printing the data that's being added to the shared data structure for PART A)

Books titles sorted by frequency of search pattern 'world':
book_02: 1 occurrences
book_01: 1 occurrences

Books titles sorted by frequency of search pattern 'world':
book_01: 2 occurrences
book_02: 1 occurrences

Books titles sorted by frequency of search pattern 'world':
book_01: 4 occurrences
book_02: 1 occurrences

Books titles sorted by frequency of search pattern 'world':
book_01: 5 occurrences
book_02: 1 occurrences


Note: Till there is an occurrence of the search term in any of the books, the print statement would look empty; something like - "Books titles sorted by frequency of search pattern 'little':"

Our confidence in our solution comes from testing different search terms and counting the no. of occurences of these terms in the books using 'ctrl + f' command.