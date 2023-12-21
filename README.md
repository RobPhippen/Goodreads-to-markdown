# Goodreads CSV export to Markdown Converter
This utility takes the CSV export from goodreads:
`goodreads_library_export.csv` and converts each book and each author into a separate `.csv` file.

## Features
* It converts only a subset of the information into CSV, concentrating on information entered by the user, such as rating and comment (if any).
* 'Shelves' are rendered as hashtags
* A URL to the book description on Goodreads is inserted
* Author documents are cross-linked from books and vice versa

## Running it
* It expects to find the `goodreads_library_export.csv` file in the current directory
* It creates a subdirectory within the current directory called `Goodreads Library` and inserts all of the markdown documents there

### Execution on Linux/Mac:
```
gr2md.py
```

### Execution on other platforms
```
python3 gr2md.py
```

## Import to other systems
This has been tested with Upnote, using its built-in markdown import.


## Examples
### Author
``` md
# Leonard Susskind
#Author #Goodreads
### Books in my collection:
- [[Special Relativity and Classical Field Theory]]
- [[The Black Hole War: My Battle with Stephen Hawking to Make the World Safe for Quantum Mechanics]]
- [[Classical Mechanics: The Theoretical Minimum (Theoretical Minimum 1)]]
- [[Quantum Mechanics: The Theoretical Minimum (Theoretical Minimum 2)]]
```

### Book
``` md
# Classical Mechanics: The Theoretical Minimum (Theoretical Minimum 1)
#Book #Goodreads
- Written by [[Leonard Susskind]] with [[George Hrabovsky]]
- Publisher: Penguin
- [Details on Goodreads](https://www.goodreads.com/book/show/51221389)
- Shelves: #resting, #science
```
