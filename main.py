#Alyssa Karlson, Student ID: 010965931

import csv
import datetime
from fileinput import filename


# HashTable class using chaining.
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=20):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                return kv[1]  # value
        return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])

# Create class for packages
class Package:
    def __init__(self, ID, address, city, state, zipcode, Deadline_time, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.Deadline_time = Deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zipcode, self.Deadline_time, self.weight, self.delivery_time, self.status)


# Create package objects from the CSV package file
# Load package objects into packageHashTable
def loadPackageData(filename, packageHashTable):
    with open(filename) as packageInfo:
        packageData = csv.reader(packageInfo, delimiter=',')
        for package in packageData:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline_time = package[5]
            pWeight = package[6]
            pStatus = "At Hub"

            # Package object
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pStatus)

            # Insert data into hash table
            packageHashTable.insert(pID, p)

# Create hash table
packageHashTable = ChainingHashTable()

# Load packages into hash table
loadPackageData("Package_File.csv", packageHashTable)

'''
test if package data was loaded correctly into packageHashTable
print(packageHashTable.search(1))
'''

#create truck class
class Truck:
    def __init__(self, capacity, speed, load, packages, mileage, address, depart_time):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.capacity, self.speed, self.load, self.packages, self.mileage,
                                               self.address, self.depart_time)

#create truck objects and manually load with packages
truck1 = Truck(16,18,None, [15, 13,19,1,2,4,14,16,17,20,21,24,33,34,7,40],0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck(16,18,None,[3,18,36,38,37,5,10.29], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
truck3 = Truck(16,18,None,[25,26,28,31,32,9,6,8,11,12,22,23,30,27,39,35],0.0,"4001 South 700 East", datetime.timedelta(hours=8))

with open("Distance_File.csv") as csvfile:
    Distance_File = csv.reader(csvfile)
    Distance_File = list(Distance_File)

def distanceBetween(x_value, y_value):
    distance = Distance_File[x_value][y_value]
    if distance == '':
        distance = Distance_File[y_value][x_value]

    return float(distance)


# Read the file of address information
with open("Address_File.csv") as csvfile1:
    Address_File = csv.reader(csvfile1)
    Address_File = list(Address_File)

# Method to get address number from string literal of address
def loadAddressData(address):
    for row in Address_File:
        if address in row[2]:
            return int(row[0])

def truckDeliverPackages(truck):
    notDelivered = []
    for ID in truck.packages:
        package = packageHashTable.search(ID)
        notDelivered.append(package)
    truck.packages.clear()

    while len(notDelivered) > 0:
        nextAddress = 2000
        nextPackage = None
        for package in notDelivered:
            if distanceBetween(loadAddressData(truck.address), loadAddressData(package.address)) <= nextAddress:
                nextAddress = distanceBetween(loadAddressData(truck.address), loadAddressData(package.address))
            nextPackage = package

    truck.packages.append(nextPackage.ID)
    notDelivered.remove(nextPackage)
    truck.mileage += nextAddress
    truck.address = nextPackage.address
    truck.time += datetime.timedelta(hours=nextAddress / 18)
    nextPackage.delivery_time = truck.time
    nextPackage.departure_time = truck.depart_time

    truckDeliverPackages(truck1)
    truckDeliverPackages(truck3)
    truck2.departure_time = min(truck1.time, truck3.time)
    truckDeliverPackages(truck2)

class Main:
    # User Interface
    # Upon running the program, the below message will appear.
    print("WGUPS")
    print("Total Mileage:")
    print(truck1.mileage + truck2.mileage + truck3.mileage)  # Print total mileage for all trucks

    print(distanceBetween(1, 2))


