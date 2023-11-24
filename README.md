# Multi-Threaded-Network-Server
Multi-Threaded Network Server for Pattern Analysis

python3 MultiThreadedServer.py -l 0.0.0.0 -p 12345 -p "little"

The code/implementation fulfills these requirements: 
Pattern analysis frequency  
Results printed at intervals
Book titles sorted by the most frequent occurrences of the selected pattern


For example, when you run the command: python3 MultiThreadedServer.py -l localhost -p "world", for two books each on different connection, then the outcome would look something like this:

(Note: results are printed at intervals; while also printing the data that's being added to the shared data structure)

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