# -*- coding: utf-8 -*-

class Person:
	def __init__(self, name, preferNames, id):
		self.name = name
		self.preferNames = preferNames
		self.preferIndexes = []
		self.id = id
		self.partnerIndex = -1

	def prefersMoreThanCurrent(self, person):
		if self.partnerIndex == -1:
			return True
		indexOfCurrent = self.preferIndexes.index(self.partnerIndex)
		indexOfCandidate = self.preferIndexes.index(person.id)
		return indexOfCandidate < indexOfCurrent

	def fillPreferIndexes(self, partners):
		self.preferIndexes = []
		for name in self.preferNames:
			for partner in partners:
				if partner.name == name:
					self.preferIndexes.append(partner.id)
					break

def readFile(filename, encoding):
	return open(filename, encoding=encoding).readlines()

def getPersons(lines):
	persons = []
	index = 0
	for line in lines:
		name, prefers = line.split(':')
		name = name.split(' ')[0]
		prefers = prefers.split('\n')[0].split(' ')[1:]
		persons.append(Person(name, prefers, index))
		index += 1
	return persons	

def main():
	# read names and prefers of persons
	Men = getPersons(readFile('men.in', 'utf-8'))
	Women = getPersons(readFile('women.in', 'utf-8'))

	# fill preferIndexes - bind names and persons
	for man in Men:
		man.fillPreferIndexes(Women)

	for woman in Women:
		woman.fillPreferIndexes(Men)

	k = 0
	n = len(Men)

	while k < n:

		man = Men[k]

		indexOfLastPartner = None
		while man is not None:
			
			womanIndex = man.preferIndexes[0]
			woman = Women[womanIndex]
			
			if woman.prefersMoreThanCurrent(man):
				man.partnerIndex = womanIndex
				indexOfLastPartner = woman.partnerIndex
				woman.partnerIndex = man.id
				if indexOfLastPartner != -1:
					man = Men[indexOfLastPartner]
				else:
					man = None	
			
			if man is not None:
				man.preferIndexes.pop(0)
		
		k = k + 1

	
	# refill preferIndexes for testing
	for man in Men:
		man.fillPreferIndexes(Women)

	for woman in Women:
		woman.fillPreferIndexes(Men)

	# test
	for man in Men:
		for woman in Women:
			condition1 = man.prefersMoreThanCurrent(woman)
			condition2 = woman.prefersMoreThanCurrent(man)
			if condition1 and condition2:
				print("there is an error:")
				print("Man %s prefers woman %s more than his wife" % (man.name, woman.name))
				print("Woman %s prefers man %s more than her husband" % (woman.name, man.name))

	# print pairs
	for man in Men:
		print("%s + %s" % (man.name, Women[man.partnerIndex].name))

if __name__ == '__main__':
	main()