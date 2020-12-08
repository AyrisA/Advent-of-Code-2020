"""
--- Day 7: Handy Haversacks ---
You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)
"""

def process_contents(inside_stuff):
    bags = []
    if inside_stuff != 'no other bags.':
        braw = [x.strip() for x in inside_stuff.split(',')]
        for b in braw:
            bags.append(' '.join(b.split()[1:-1]))

    return bags


def find_containers(bmap, bname):
    my_containers = [x for x in bmap if bname in bmap[x]]
    containers = set(my_containers)

    if len(my_containers) > 0:
        for c in my_containers:
            containers.update(find_containers(bmap, c))

    return containers


with open('./input07.txt', 'r') as f:
    input = [x.strip().split(' bags contain ') for x in f.readlines()]

bagmap = {}

for rule in input:
    outside = rule[0]
    inside = process_contents(rule[1])
    for bag in [outside] + inside:
        if bag not in bagmap:
            bagmap[bag] = set()

    bagmap[outside].update(set(inside))

sg_containers = find_containers(bagmap, 'shiny gold')
print("{} bag colors can eventually hold a shiny gold bag".format(len(sg_containers)))
