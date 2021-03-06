# D3FamilyTree
A means of dynamically creating D3.js force-directed family trees using python

[![Example_tree](https://user-images.githubusercontent.com/25749859/74477308-fe84b580-4ea2-11ea-88f3-e9ef5b575f35.png)](https://tobi1kenobi.github.io/D3FamilyTree/)
*Click [here](https://tobi1kenobi.github.io/D3FamilyTree/) to see the above tree in action!*

The relations are defined using a CSV file (for which I've provided an example, `family.csv`), a python script creates nodes and links which are then used to fill in a template HTML file to make an interactive D3.js force-directed graph.


## How to create the example tree

1. Install python 3 - ensure you have the pandas, numpy, os, datetime, and jinja2 libraries
1. Run the script `create-tree.py`  
2. Open `FamilyTree.html` in a web browser

## How to make your own family CSV

The the script `create-tree.py` refers to the file `family.csv`, so after making a new CSV the existing example `family.csv` file must be deleted and replaced your desired CSV.

### The columns `First Name`, `Last Name`, `Father`, `Mother`, `Generation`, `Gender`, `Born`, and `Partners` are required.

Each individual in the tree must have a row entry for all of the following:

`First Name` and `Last Name` contain the first and last name of the individual, respectively. 

`Father` contains the first and last name of the individual's father **only if** they exist elsewhere in the CSV file. Spelling **must** match. Use 'na' if the invididual's father is not in the CSV file.

`Mother` is the same as Father but with the individual's mother.

`Generation` refers to which ancestral level the individual belongs to where 1 is the root ancestor, 2 is the children of the root, 3 is the grandchildren of the root and so on. Individuals unrelated to the root are assigned generation 10.

`Gender` currently must be either M or F.

`Born` is the year of birth of the individual.

`Partners` contains, in chronological order, the partners that the individual has either married or had children with. These partners **must be individuals** in the CSV file additionally but with the caveat that the partner individual **does not** have any entries in their Partners column. Semicolons ';' following the partner's name indicate an ended relationship and a subsequent partner can be added after e.g. 'John Doe' indicates married to John Doe whilst 'John Doe; Allan Smith;' indicates separated from John Doe and then separated from Allan Smith.

### Important

The easiest way to produce a dysfunctional tree is to have names that do not correspond between First Name + Last Name, Father, Mother or Partners. The tree is built on the assumption that the names will match i.e. that corresponding individuals are named consistently throughout - if this is not the case the tree will **fail to load properly**.

An example CSV file and the corresponding tree can be found in this repository.

## TODOS

 - [ ] Add (optional) photos in the tooltip
 - [ ] Add support for more than 5 generations
 - [ ] Add tests in python that catch when there are non-matching names or other things that will break the HTML file
 - [ ] Make editing tree more user friendly
 - [ ] Allow for looking at tree in a given year (maybe with slider/animation)

## References
D3 code was adapted from: https://medium.com/ninjaconcept/interactive-dynamic-force-directed-graphs-with-d3-da720c6d7811
