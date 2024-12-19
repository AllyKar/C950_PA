#Alyssa Karlson, Student ID: 010965931

import csv
import datetime
from fileinput import filename
from os import remove


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
    def __init__(self, ID, address, city, state, zipcode, Deadline_time, weight,note, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.Deadline_time = Deadline_time
        self.weight = weight
        self.note = note
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.address, self.city, self.state, self.zipcode, self.Deadline_time, self.weight, self.note, self.delivery_time, self.status)

    def update_status(self, convertTime):
        if self.delivery_time == None:
            self.status = "At the hub"
        elif convertTime < self.departure_time:
            self.status = "At the hub"
        elif convertTime < self.delivery_time:
            self.status = "En route"
        else:
            self.status = "Delivered"
        if self.ID == 9:
            if convertTime > datetime.timedelta(hours=10, minutes=20):
                self.address = "410 S State St"
                self.zipcode = "84111"
            else:
                self.address = "300 State St"
                self.zipcode = "84103"


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
            pNote = package[7]
            pStatus = "At Hub"

            # Package object
            p = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline_time, pWeight, pNote, pStatus)

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


#nearest neighbor algorithm to determine order of delivery for packages on truck
def truckDeliverPackages(truck):
    notDelivered = []
    for packageID in truck.packages:
        package = packageHashTable.search(packageID)
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

#loads/delivers packages for each truck
truckDeliverPackages(truck1)
truckDeliverPackages(truck2)
truckDeliverPackages(truck3)

class Main:
    #User Interface
    #prints title and total mileage
    print("WGUPS")
    print("Truck 1 Mileage:", truck1.mileage)
    print("Truck 2 Mileage:", truck2.mileage)
    print("Truck 3 Mileage:", truck3.mileage)
    print("Total Mileage:", truck1.mileage + truck2.mileage + truck3.mileage)


    #tests if data was uploaded accurately from csv files
    #print(distanceBetween(1, 2))
    #print(loadAddressData(truck1.address))

    #algorithm functionality tests
    #print(truck3.depart_time)
    #print(truck1.time)
    #print(truck2.time)
    #print(truck2.mileage)
    
    #Provides three menu options
    text = input("Please select from the following options (type only the number to select option)\n"
                 "1. Print all package statuses with time and total mileage\n"
                 "2. Get a single package status with time\n"
                 "3. Exit the Program")
    #option 1: shows statuses of all packages at the time the user provided
    if text == "1":
            user_time = input("Please enter a time to check status of packages. Use the following format, HH:MM:SS")
            (h, m, s) = user_time.split(":")
            convertTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            for packageID in range(1, 41):
                package = packageHashTable.search(packageID)
                package.update_status(convertTime)
                print(str(package))

            print('Total Mileage:', truck1.mileage + truck3.mileage + truck2.mileage)
    #option 2: shows the status of a single package selected by user at the time provided
    elif text == "2":
            user_time = input("Please enter a time to check status of packages. Use the following format, HH:MM:SS")
            (h, m, s) = user_time.split(":")
            convertTime = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            solo_input = input("Enter the numeric package ID")
            package = packageHashTable.search(int(solo_input))
            package.update_status(convertTime)
            print(str(package))
    #option 3: exits the program
    elif text == "3":
        print("Exiting the Program")
        exit()





