import csv
import json

# names.csv comes from this dataset: https://healthdata.gov/dataset/baby-names-beginning-2007
# Imports names from names.csv and selects only names that have more than a certain limit to put into a JSON list dumped into processed_names
if __name__ == '__main__':
    males = {}
    females = {}
    limit = 100  # So if there are more than 100 alans in new york state, then alan will be added to our list

    with open('names.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        first_row = True  # is it currently going through the first row

        for row in csv_reader:
            if first_row:
                first_row = False  # now it is not going through the first row
            else:
                if row[3] == 'M':
                    try:  # If name is already in list
                        males[row[1]] += int(row[4])
                    except KeyError:  # If name is not in list
                        males[row[1]] = int(row[4])
                if row[3] == 'F':
                    try:
                        females[row[1]] += int(row[4])
                    except KeyError:
                        females[row[1]] = int(row[4])

    males_list = []
    females_list = []

    for name in males: # Iterates through dictionary of males
        if males[name] > limit:  # Checks if name has more than the limit we've set, then that's appended to a new list of males
            males_list.append(name)

    for name in females:  # Same as males
        if females[name] > limit:
            females_list.append(name)

    file = open("processed_names.json", "w")
    file.write(json.dumps({'male': males_list,'female': females_list}))
    file.close()
