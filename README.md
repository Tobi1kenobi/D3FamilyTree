# D3FamilyTree
A means of dynamically creating D3.js force-directed family trees using python

![Example_tree](https://user-images.githubusercontent.com/25749859/74199799-1f5bc980-4c5d-11ea-8c0f-73d6bd511d9e.png)

The relations are defined using a CSV file (for which I've provided an example, `family.csv`), a python script creates nodes and links which are then used to fill in a template HTML file to make an interactive D3.js force-directed graph.


## How to create the example tree

1. Install python 3 - ensure you have the pandas, numpy, os, datetime, and jinja2 libraries
1. Run the script `create-tree.py`  
2. Open `FamilyTree.html` in a web browser

## How to make your own family CSV

The the script `create-tree.py` refers to the example CSV, so after making a new CSV, `create-tree.py` must be modified to read in the new CSV.

### The columns First Name, Last Name, Father, Mother, Generation, Gender, Born, and Partners are required.

First Name and Last contain the first and last name of the individual. 

Father contains the first and last name of the individual's father **only if** they exist elsewhere in the CSV file. Spelling **must** match. Use 'na' if the invididual's father is not in the CSV file.

Mother is the same as Father but with the individual's mother.

Generation refers to which ancestral level the individual belongs to where 1 is the root ancestor, 2 is the children of the root, 3 is the grandchildren of the root and so on. Individuals unrelated to the root are assigned generation 10.

Gender currently must be either M or F.

Born is the year of birth of the individual.

Partners contains, in order, the partners that the individual has had either married or had children with. These partners **must be individuals** in the CSV file additionally but with the caveat that the partner individual **does not** have any entries in their Partners column. If an individual has multiple partners these are separated by a semicolon ';', the final partner is assumed to be married to the individual if this is not the case a semicolon should be added after the final partner.

### Important

The easiest way to produce a non-functional tree is to have names that do not correspond between First Name + Last Name, Father, Mother or Partners. The tree is built on the assumption that the names will match i.e. that corresponding individuals are named consistently throughout - if this is not the case the tree will fail to load properly.

An example CSV file and the corresponding tree can be found in this repository.

## References
D3 code was heavily adapted from: https://medium.com/ninjaconcept/interactive-dynamic-force-directed-graphs-with-d3-da720c6d7811
