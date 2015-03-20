# tables

1) Time complexity 

The basic idea is to have a nested list for referencing the tables, where
tables[i] is the list of tables with i empty seats.

When a group with i persons comes, a table with i seats can accessed with 
O(1).
The munber of empty seats for that table (the last of the list) is decreased 
of CustomerGroup.size and the table is inserted in the new corresponding 
list, with O(1) as well.

Example: 

aTable.size = 4

tables[2] = [ .. ]
tables[4] = [ .. , aTable] 

-> CustomerGroup.size = 2 arrived!

aTable.size = 2 # new size

tables[2] = [ .., aTable ]
tables[4] = [ .. ]

Hence arrives() has a complexity of O(1)

When the groups left, time complexity should be O(i) where i is the number 
of the tables with i empty seats. The smaller is the group, the more tables must be 
scanned.
The worst case would be when every table has a one person group and every
group inline is a 6 person one.

Furthermore, every time a group leaves, the inline queue is scanned. 
Hence the total complexity of leave() is O(n+m) where n is the
number of the tables and m the number of the groups inline.


A possible improvement would be to substitute the list basic type with an
implementation of a double linked list, where each CustomerGroup has a 
reference to the next and previous. In this way, pop operation would be 
O(1). The same code would work.

2) Space occupation
The space occupation is roughly

72 * #Table + 96 * #CustomerGroup bytes.

The datastructures footprint is the size of 
6 * (sizeof(list)) +
1 * sizeof(list)

corresponding to SeatingManager.tables SeatingManager.waitingGroups lists.

It tooks about 5 hours to tackle this job, about two-three to design it, 
and two-three to test/implement it. Actually, there must be more time to 
implement some automatic test.




