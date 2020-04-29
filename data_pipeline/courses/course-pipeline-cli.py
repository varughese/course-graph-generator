import sys
from scraper import scrape_term
import os
import argparse

parser = argparse.ArgumentParser(description='Scrape course data, parse prereqs, and convert it to a graph.')
parser.add_argument('--term', type=int, help='The Pitt term code to scrape', default=-1)
parser.add_argument('--reset_scrape', help='Ignore previous cache for scrapinng', default=False, action="store_true")
parser.add_argument('--reset_parser', help='Recompiler the PegJS parser and then reparse the json', default=False, action="store_true")

args = parser.parse_args()
term = args.term

if term == -1:
	term = int(input("Enter in the term code \n> "))

print("Starting to scrape ...")
scrape_term(term, USE_CHECKPOINTS=(not args.reset_scrape))

term_dir = os.path.join(".", "scraped", str(term))
course_data_path = os.path.join(term_dir, "course_data.json")
course_parsed_raw_path = os.path.join(term_dir, "course_data-parsed-raw.json")
course_parsed_fixing_path = os.path.join(term_dir, "course_data-parsed-fixing.json")

if args.reset_parser or not os.path.isfile("./parser/parser.js"):
	print("Running PegJS Parser")
	os.system("yarn run pegjsparse")

if args.reset_parser or not os.path.isfile(course_parsed_raw_path):
	print("Parsing prerequisites")
	os.system("parser/prereq-cli {} -o {}".format(course_data_path, course_parsed_raw_path))

fixpreqs = input("Do you want to fix the prequisities that did not parse? (empty line for no)")

# I was getting annoyed by how many inconsistencies and edge cases there were with these prereqs, so
# I just stopped

if fixpreqs.strip() != ' ':
	print("Fixing preqrequisites")
	if not args.reset_parser and os.path.isfile(course_parsed_fixing_path):
		os.system("parser/prereq-cli {} -u -f -s2".format(course_parsed_fixing_path))
	else:
		os.system("parser/prereq-cli {} -o {} -f -s2".format(course_parsed_raw_path, course_parsed_fixing_path))