"""
--- Day 4: Passport Processing ---
You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport. While these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore aren't actually valid documentation for travel in most of the world.

It seems like you're not the only one having problems, though; a very long line has formed for the automatic passport scanners, and the delay could upset your travel itinerary.

Due to some questionable network security, you realize you might be able to solve both of these problems at the same time.

The automatic passport scanners are slow because they're having trouble detecting which passports have all required fields. The expected fields are as follows:

byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID)
Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

Here is an example batch file containing four passports:

ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt (the Height field).

The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials, not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields. Treat this "passport" as valid.

The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not, so this passport is invalid.

According to the above rules, your improved system would report 2 valid passports.

Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?
"""

import re

def read_input(input):
    raw_records = []
    record = []
    for line in input:
        if line == '':
            raw_records.append(record)
            record = []
        else:
            record.append(line)
    raw_records.append(record)

    records = [proc_record_text(r) for r in raw_records]
    return records

def proc_record_text(rtext):
    elements = []
    for line in rtext:
        elements += [tuple(el.split(':')) for el in line.split()]
    
    record = dict(elements)
    for key in record:
        if key in ['byr','iyr','eyr']:
            try:
                record[key] = int(record[key])
            except:
                pass
    return record


def is_valid(rec, ignore_cid = False, check_values=True, verbose=False):
    fields = [
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    ]
    if not ignore_cid:
        fields += "cid"

    # Check keys
    keys = rec.keys()
    for f in fields:
        if f not in keys:
            return False

    # Check values
    if check_values:
        # Check years
        if (rec['byr'] < 1920) or (rec['byr'] > 2002):
            if verbose:
                print("fail BYR")
            return False
        if (rec['iyr'] < 2010) or (rec['iyr'] > 2020):
            if verbose:
                print("fail IYR")
            return False
        if (rec['eyr'] < 2020) or (rec['eyr'] > 2030):
            if verbose:
                print("fail EYR")
            return False
        
        # Check height
        unit = rec['hgt'][-2:]
        if unit not in ['in','cm']:
            if verbose:
                print("fail HGT -- unit")
            return False

        bounds = [150, 193] if unit == 'cm' else [59, 76]
        try:
            h = int(rec['hgt'][:-2])
            if (h < bounds[0]) or (h > bounds[1]):
                if verbose:
                    print("fail HGT -- bounds")
                return False
        except:
            if verbose:
                print("fail HGT -- integer")
            return False

        # Check hair color
        regex = r"^#[0-9,a-f]{6}"
        matched = re.fullmatch(regex, rec['hcl'])
        if not matched:
            if verbose: 
                print("fail HCL")
            return False

        # Check eye color
        colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        if rec['ecl'] not in colors:
            if verbose:
                print("fail ECL")
            return False

        # Check PID
        if not(len(rec['pid']) == 9 and rec['pid'].isnumeric()):
            if verbose:
                print("fail PID")
            return False
    return True
        


with open('./input04.txt', 'r') as f:
    input = [x.strip() for x in f.readlines()]

valid_count = 0
valid2_count = 0
records = read_input(input)
for rec in records:
    if is_valid(rec, ignore_cid=True, check_values=False):
        valid_count += 1
    if is_valid(rec, ignore_cid=True):
        valid2_count += 1

print("Part 1: {} valid records".format(valid_count))
print("Part 2: {} valid records".format(valid2_count))
