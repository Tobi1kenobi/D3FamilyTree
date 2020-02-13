import pandas as pd
import numpy as np
from datetime import date
from jinja2 import Environment, FileSystemLoader
import os


# Global variable, should change later
# Dictionary that sets different strengths for different types of link
link_vars = {'partner':{'strength':2,'distance':60,'type':'partner'},
            'child':{'strength':2,'distance':40,'type':'child'},
            'invisible':{'strength':20,'distance':[300, 180, 70, 50],'type':'invisible'}}


#######################################################################
############ FUNCTIONS
#######################################################################



def GetAge(birth_year):
    '''
    Given a year returns the two possible ages.
    '''

    if isinstance(birth_year, int):
        return str(date.today().year - birth_year - 1) + '/' + str(date.today().year - birth_year)
    else:
        return '?'

def MakePeopleNodes(family_df):
    '''
    Makes nodes for the people in the family dataframe
    '''

    people_node_list = []
    for i, row in family_df.iterrows():
        person_node = {}
        person_node['id'] = row['First Name'] + row['Last Name']
        person_node['label'] = row['First Name'] + ' ' + row['Last Name']
        person_node['level'] = np.nanmin([row['Generation'],10]) # Takes the level or assigns a 'partner level' of 10
        person_node['born'] = row['Born']
        person_node['age'] = GetAge(row['Born'])
        person_node['group'] = 'Person'
        person_node['gender'] = row['Gender']
        person_node['dad'] = row['Father']
        person_node['mum'] = row['Mother']
        
        people_node_list.append(person_node)
    return people_node_list

def MarriedOrSeparated(partners_string):
    '''
    Breaks a partners string into a dictionary of partners and either 'm' for married or 's' for separated.
    '''
    
    partners_list = partners_string.split(';')
    if len(partners_list) == 1:
        return {partners_string:'m'}
    else:
        dict_of_partners = {} # Initiliase empty dictionary to be returned
            
        for partner in partners_list:
            if partner == partners_list[-1]: # Exception for last partner in list
                if partner.replace(' ', '') == '':
                    break
                else:
                    dict_of_partners[partner] = 'm'
            else:
                dict_of_partners[partner] = 's'
    
    return dict_of_partners
                    
        

def MakePartnershipNodes(family_df):
    '''
    Makes nodes for relationships that children were born from.
    '''

    partner_node_list = []
    for i, row in family_df.iterrows():
        if pd.isna(row['Partners']) == False:
            partners_dict = MarriedOrSeparated(row['Partners'])
            for partner, status in partners_dict.items():
                partner_node = {}
                partner_node['id'] = row['First Name'] + row['Last Name'] + ';' + partner.replace(' ', '')
                partner_node['label'] = status
                partner_node['level'] = 2
                partner_node['born'] = 0
                partner_node['group'] = 'Partnership'
                
                partner_node_list.append(partner_node)
    return partner_node_list

def MakePartnerLinks(partner_nodes):
    '''
    Makes links between partners.
    '''
    
    links_list = []
    
    for node in partner_nodes:
        sources = node['id'].split(';')
        for src in sources:
            link = {}
            link['source'] = src
            link['target'] = node['id']
            link['distance'] = link_vars['partner']['distance']
            link['strength'] = link_vars['partner']['strength']
            link['type'] = link_vars['partner']['type']
            
            links_list.append(link)
    
    return links_list


def GetPartnerNodeOrder(partner_nodes, string):
    '''
    If necessary, reverses the order of the input string e.g. Gary;Jane to Jane;Gary, to match
    how the partner node is listed. If the string already matches, does nothing.
    '''

    list_of_partner_node_ids = [node['id'] for node in partner_nodes]
    if string in list_of_partner_node_ids:
        return string
    else:
        split_string = string.split(';')
        new_string = split_string[1] + ';' + split_string[0]
        return new_string

def MakeChildLinks(family_nodes, partner_nodes):
    '''
    Makes links between children and the relationship node that they arose from.
    '''
    
    links_list = []
    
    for node in family_nodes:
        if node['mum'] == 'na':
            continue
        else:
            partner_target = GetPartnerNodeOrder(partner_nodes,
                                                 node['dad'].replace(' ', '') + ';' + node['mum'].replace(' ', ''))
            link = {}
            link['source'] = node['id']
            link['target'] = partner_target
            link['distance'] = link_vars['child']['distance']
            link['strength'] = link_vars['child']['strength']
            link['type'] = link_vars['child']['type']
            
            links_list.append(link)
            
    return links_list

def MakeInvisibleLinks(family_nodes, partner_nodes):
    '''
    Makes links between partners so they are more drawn to each other than they
    are to their children. These links are transparent in the tree.
    '''              
    
    fam_node_dict = {}
    
    for node in family_nodes:
        fam_node_dict[node['id']] = node
      
    links_list = []
    for node in partner_nodes:
        src, trgt = node['id'].split(';')
        
        src_fam_node = family_nodes
        
        link = {}
        link['source'] = src
        link['target'] = trgt
        link['distance'] = link_vars['invisible']['distance'][fam_node_dict[src]['level']-1] # Use node level to reference a distance custom for each generation
        link['strength'] = link_vars['invisible']['strength'] 
        link['type'] = link_vars['invisible']['type'] 
        
        links_list.append(link)
    
    return links_list

env = Environment( loader = FileSystemLoader('.') )
template = env.get_template('Tree_template.html')
 

#######################################################################
############ MAIN
#######################################################################

# Load in data
family = pd.read_csv('family.csv')

# Make the nodes in the tree
family_nodes = MakePeopleNodes(family)
family_partner_nodes = MakePartnershipNodes(family)

# Make the links in the tree
family_partner_links = MakePartnerLinks(family_partner_nodes)
family_child_links  = MakeChildLinks(family_nodes, family_partner_nodes)
family_invisible_links = MakeInvisibleLinks(family_nodes, family_partner_nodes)

# Fill the HTML template with the information here
filename = 'FamilyTree.html'
with open(filename, 'w') as fh:
    fh.write(template.render(
        fam_nodes = family_nodes + family_partner_nodes,
        fam_links = family_partner_links + family_child_links + family_invisible_links,
    ))

# Open the tree    
os.startfile(filename)