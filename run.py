#user/bin/python

''' run.py: checks the Wikipedia page of each state and finds the state's official language '''

__author__ = "Lewis Millholland"
__copyright__ = "Lewis Millholland, 2017"

import requests
import lxml.html as lh
import csv

base_url = 'https://en.wikipedia.org/wiki/'


# Find the official language of a particular state
def language_of_state(state):

	# Plug the state into the Wikipedia url and extract the desired <td> text
	try:
		data 	  = requests.get(base_url + state).content
		root 	  = lh.fromstring(data)
		parent_tr = root.xpath('.//a[text()="Official language"]')[0]
		node 	  = parent_tr.getparent().getparent()[1]
		language  = remove_container_chars( lh.tostring(node) )
		language  = language.replace('\n', ' ').strip()
		return language

	# In cases such as New York, the term must be disambiguized (is that a word?)
	except Exception:
		if '(state)' in state:  # for infinite loops
			return 'No official language detected.'
		else:
			language = language_of_state(state + ' (state)')

	return language


# Remove all container characters
def remove_container_chars(html):
	html = remove_tags(html, '<', '>')
	html = remove_tags(html, '[', ']')
	return html


# Remove all container elements in HTML string, denoted by the input container chars
def remove_tags(html, l_container, r_container):

	# Remove one HTML tag and try again
	try:
		l_idx = html.index( l_container )
		r_idx = html.index( r_container )
		html = html[0:max(l_idx, 0)] + html[r_idx + 1:]
		return remove_tags(html, l_container, r_container)

	# No more bracket tags left
	except Exception:
		return html


# Gather list of state names
def list_of_states():
	with open('states.txt', 'r') as states_file:
		states = [s.replace('\n', '') for s in states_file.readlines()]
	return states


# Given a dictionary of states and languages, write to csv
def write_to_csv(states):

	# Put states in column one and languages in 2
	with open('statelanguages.csv', 'wb') as o_file:
		w = csv.writer(o_file)
		for row in states.iteritems():
			w.writerow(row)


# Find all official states
def main():

	# Organize list of states
	state_names = list_of_states()
	states = dict()

	# Find language of each state
	for state in state_names:
		language = language_of_state(state)
		states[state] = language

	# Output data to csv
	write_to_csv(states)


main()