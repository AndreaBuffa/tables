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

	''' Group arrives and wants to be seated. '''
	def arrives(self, group):
		if group.managed: 
			return
		if group.served:
			return
		if not self.allocateTable(group):
			self.waitingGroups.append(group)

	''' Whether seated or not, the group leaves the restaurant. '''
	def leaves(self, group):
		if group.managed:
			if group.served:
				group.served = group.managed = False
				self.deallocateTable(group)
			else:
				self.waitingGroups = filter(
					lambda aGroup: aGgroup is group,
					self.waitingGroups)
			return True
		return False

	''' Return the table at which the group is seated, or null if
	they  are not seated (whether they're waiting or already left). '''
	def locate(self, group):
		if group:
			return group.table
		return None

	def allocateTable(self, group):
		tableSize = group.size
		while tableSize <= MAX_TABLE_SIZE:
			if len(self.tables[tableSize]):
				table = self.tables[tableSize].pop()
				group.table = table
				group.served = group.managed = True
				table.emptySeats = table.size - group.size
				self.tables[table.emptySeats].append(table)
				return True
			else:
				tableSize += 1
		return False

	def deallocateTable(self, group):
		tableSize = group.table.emptySeats
		table = group.table
		self.tables[tableSize] = filter(lambda theTable: theTable is not table, self.tables[tableSize])
		group.table = None
		group.served = group.managed = False
		table.emptySeats += group.size
		self.tables[table.emptySeats].append(table)
		return True

	def dump(self):
		queueString = b"Groups waiting inline: "
		if len(self.waitingGroups):
			for group in self.waitingGroups:
				queueString += " %d" % group.size
		else:
			queueString += "%d" % 0
		print "-------------------------"
		print queueString
		print "-------------------------"
		print "Occupied tables"
		tableString = b""
		for tableRow in self.tables:
			for table in tableRow:
				tableString += "\n %d seats table, %d seated" % (table.size, table.size - table.emptySeats)
			print tableString
			tableString = b""

tables = []
groups = []
settings = open('settings', 'r')
for line in settings:
	tableSize = re.compile('table (\d)+').search(line)
	if tableSize:
		tables.append(Table(int(tableSize.group(1))))
		#print "Table with %s seats added" % tableSize.group(1)

manager = SeatingManager(tables)

f = open('inputSimulation', 'r')
# Each file line is a message to the SeatingManager
for line in f:
	groupSize = re.compile('arrive group (\d)+').search(line)
	if groupSize:
		theGroup = CustomerGroup(int(groupSize.group(1)))
		# rememeber for later
		groups.append(theGroup)
		# ARRIVE MESSAGE
		print "*** Group made of %d arrived! ***" % theGroup.size
		manager.arrives(theGroup)
	else:
		listIndex = re.compile('leave group \[(\d)+\]').search(line)
		if listIndex:
			group = groups[int(listIndex.group(1))]
			if group:
				# LEAVE MESSAGE
				print "*** Group made of %d left! ***" % group.size
				found = manager.leaves(group)
				if not found: print "Already left <--------"
		else:
			match = re.compile('locate group \[(\d)+\]').search(line)
			if match:
				listIndex = int(match.group(1))
				group = groups[listIndex]
				if group:
					# LOCATE MESSAGE
					print "Locate group index [%d]:" % listIndex
					table = manager.locate(group)
					print table
	# dump tables and groups for each message
	manager.dump()
	raw_input("[Enter to continue]")
