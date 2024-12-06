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

    def update_status(self, convert_timedelta):
        if self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time > convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"

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
truck1 = Truck(16,18,16, [15, 13,19,1,2,4,14,16,17,20,21,24,33,34,7,40],0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck(16,18,8,[3,18,36,38,37,5,10,29], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
truck3 = Truck(16,18,16,[25,26,28,31,32,9,6,8,11,12,22,23,30,27,39,35],0.0,"4001 South 700 East", datetime.timedelta(hours=10))

with open("Distance_File.csv") as csvfile:
    distanceData = csv.reader(csvfile)
    distanceData = list(distanceData)

def distanceBetween(x_value, y_value):
    distance = distanceData[x_value][y_value]
    if distance == '':
        distance = distanceData[y_value][x_value]

    return float(distance)

# Read the file of address information
with open("Address_File.csv") as csvfile1:
    CSV_Address = csv.reader(csvfile1)
    CSV_Address = list(CSV_Address)

# Method to get address number from string literal of address
def loadAddressData(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])

# Method for ordering packages on a given truck using the nearest neighbor algo
# This method also calculates the distance a given truck drives once the packages are sorted
def delivering_packages(truck):
    # Place all packages into array of not delivered
    not_delivered = []
    for packageID in truck.packages:
        package = packageHashTable.search(packageID)
        not_delivered.append(package)
    # Clear the package list of a given truck so the packages can be placed back into the truck in the order
    # of the nearest neighbor
    truck.packages.clear()

    # Cycle through the list of not_delivered until none remain in the list
    # Adds the nearest package into the truck.packages list one by one
    while len(not_delivered) > 0:
        next_address = 2000
        next_package = None
        for package in not_delivered:
            if distanceBetween(loadAddressData(truck.address), loadAddressData(package.address)) <= next_address:
                next_address = distanceBetween(loadAddressData(truck.address), loadAddressData(package.address))
                next_package = package
        # Adds next closest package to the truck package list
        truck.packages.append(next_package.ID)
        # Removes the same package from the not_delivered list
        not_delivered.remove(next_package)
        # Takes the mileage driven to this packaged into the truck.mileage attribute
        truck.mileage += next_address
        # Updates truck's current address attribute to the package it drove to
        truck.address = next_package.address
        # Updates the time it took for the truck to drive to the nearest package
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time


# Put the trucks through the loading process
delivering_packages(truck1)
delivering_packages(truck2)
delivering_packages(truck3)

class Main:
    # User Interface
    # Upon running the program, the below message will appear.
    print("WGUPS")
    print("Total Mileage:", truck1.mileage + truck2.mileage + truck3.mileage)  # Print total mileage for all trucks
''' 
tests to determine if data uploaded from csv files correctly

    print(distanceBetween(1, 2))
    print(loadAddressData(truck1.address))
    print(truck3.depart_time)
    print(truck1.time)
    print(truck2.time)
    
'''

    text = input("Please select from the following options (type only the number to select option)\n"
                 "1. Print all package statuses with time and total mileage\n"
                 "2. Get a single package status with time\n"
                 "3. Exit the Program")
    if text == "1":
            user_time = input("Please enter a time to check status of packages. Use the following format, HH:MM:SS")
            (h, m, s) = user_time.split(":")
            convertTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            for packageID in range(1, 41):
                package = packageHashTable.search(packageID)
                package.update_status(convertTime)
                print(str(package))

            print('Total Mileage:', truck1.mileage + truck3.mileage + truck2.mileage)

    elif text == "2":
            user_time = input("Please enter a time to check status of packages. Use the following format, HH:MM:SS")
            (h, m, s) = user_time.split(":")
            convertTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            solo_input = input("Enter the numeric package ID")
            package = packageHashTable.search(int(solo_input))
            package.update_status(convertTime)
            print(str(package))

    elif text == "3":
        print("Exiting the Program")
        exit()





