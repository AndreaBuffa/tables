'''
 implement a system that manages seating for a Restaurant.
'''
import re

MAX_TABLE_SIZE = 6
MIN_TABLE_SIZE = 2
MAX_GROUP_SIZE = 6

class Table:
	size = 0
	emptySeats = 0

	def __init__(self, _size):
		self.size = _size
		self.emptySize = MAX_TABLE_SIZE - _size

class CustomerGroup:
	size = 0
	served = False
	managed = False
	table = None

	def __init__(self, _size):
		self.size = _size

''' 
Our restaurant has round tables. Tables come in different sizes that can
accommodate 2, 3, 4, 5 or 6 people. People arrive at our restaurant in
groups of 6 or less. People in the same group want to be seated at the same
table. You can seat a group at any table that has enough empty seats for
them. If it's not possible to accommodate them, they're willing to wait.

Once they're seated, they can stay as long as they want and you cannot ask
them to move to another table (i.e. you cannot move them to make space for 
another group). In terms of fairness of seating order: seat groups in the
order they arrive, but seat opportunistically. For example: a group of 6 is
waiting for a table and there are 4 empty seats at a table for 6; if a group
of 2 arrives you may put them at the table for 6 but only if you have
nowhere else to put them. This may mean that the group of 6 waits a long
time, possibly until they become frustrated and leave.
'''
class SeatingManager:
	# a nested list where '''
	tables = []
	waitingGroups = []

	def __init__(self, _tables):
		for x in range(0, MAX_TABLE_SIZE + 1):
			self.tables.append([])
		for table in _tables:
			table.emptySeats = table.size
			self.tables[table.size].append(table)

	# Group arrives and wants to be seated. '''
	def arrives(self, group):
		if group.managed: 
			return
		if group.served:
			return
		if not self.allocateTable(group):
			waitingGroups.append(group)

	''' Whether seated or not, the group leaves the restaurant. '''
	def leaves(self, group):
		if group.managed:
			if group.served:
				group.served = group.managed = False
				self.deallocateTable(group)
			else:
				waitingGroups.find(
				filter(lambda station: station['delay_m'] > 0,
				stationsByDelay)

	''' Return the table at which the group is seated, or null if they 
	are not seated (whether they're waiting or already left). '''
	def locate(self, group):
		return self.table

	def allocateTable(self, group):
		tableSize = 0
		tableSize = group.size
		while tableSize < MAX_TABLE_SIZE:
			table = self.tables[tableSize].pop()
			if table:
				group.table = table
				group.served = True
				table.emptySeats = table.size - group.size
				self.tables[table.emptySeats].append(table)
				return True
			else:
				tableSize += 1
		return False

	def deallocateTable(self, group):
		tableSize = group.size
		while tableSize < MAX_TABLE_SIZE:
			table = self.tables[tableSize].pop()
			if table:
				group.table = None
				group.served = False
				table.emptySeats += group.size
				self.tables[table.emptySeats].append(table)
				return True
			else:
				tableSize += 1 
		return False

tables = []
groups = []
settings = open('settings', 'r')
for line in settings:
	tableSize = re.compile('table (\d)+').search(line)
	if tableSize:
		tables.append(Table(int(tableSize.group(1))))
		print "Table with %s seats added" % tableSize.group(1)

manager = SeatingManager(tables)

f = open('inputSimulation', 'r')
# Each file line is a message to the SeatingManager
for line in f:
	groupSize = re.compile('arrive group (\d)+').search(line)
	if groupSize:
		theGroup = CustomerGroup(groupSize)
		# rememeber for later
		groups.append(theGroup)
		# ARRIVE MESSAGE
		manager.arrives(theGroup)
	else:
		listIndex = re.compile('leave group [(\d)+]').search(line)
		if listIndex:
			group = groups[listIndex]
			if group:
				# LEAVE MESSAGE
				manager.arrives(group)
		else:
			listIndex = re.compile('locate group [(\d)+]').search(line)
			if listIndex:
				group = groups[listIndex]
				if group:
					# LOCATE MESSAGE
					manager.locate(group)
	# dump tables and groups for each message
	raw_input("Enter to continue")
