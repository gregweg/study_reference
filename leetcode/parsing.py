# Parsing CSV line
line = "Alice,30,New York"
parts = line.split(",")
name, age, city = parts
print(name, age, city)  # Alice 30 New York

# PARSING Key-Value Pairs

text = "user=alice;id=42;active=true"
pairs = dict(item.split("=") for item in text.split(";"))
print(pairs)  # {'user': 'alice', 'id': '42', 'active': 'true'}

# REG EXPRESSIONS

import re

log = "2025-09-16 10:32:15 INFO User=Alice Action=Login"
pattern = r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) .*User=(?P<user>\w+) Action=(?P<action>\w+)"
match = re.match(pattern, log)

if match:
    print(match.groupdict())
    # {'date': '2025-09-16', 'time': '10:32:15', 'user': 'Alice', 'action': 'Login'}

# PARSING JSON

import json

data = '{"user": "alice", "id": 42, "active": true}'
parsed = json.loads(data)
print(parsed["user"], parsed["id"])  # alice 42

# COMMAND LINE ARGUMENTS

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name")
parser.add_argument("--age", type=int)
args = parser.parse_args(["--name", "Alice", "--age", "30"])
print(args.name, args.age)  # Alice 30

# Parsing HTML
from bs4 import BeautifulSoup

html = "<html><body><h1>Hello</h1><p>User: Alice</p></body></html>"
soup = BeautifulSoup(html, "html.parser")
print(soup.h1.text)   # Hello
print(soup.p.text)    # User: Alice


# PARSING ARITHMETIC EXPRESSIONS (using ast)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name")
parser.add_argument("--age", type=int)
args = parser.parse_args(["--name", "Alice", "--age", "30"])
print(args.name, args.age)  # Alice 30