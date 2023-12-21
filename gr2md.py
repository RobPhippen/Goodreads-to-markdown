#!/usr/bin/env python
import csv  # CSV processing
import re   # Regular expressions
import os
import sys

def wikiLink(s):
    return f'[[{s}]]'

def urlLink(description, url):
    return f'[{description}]({url})'

def mdTag(tag):
    return f'#{tag.capitalize()}' # Always capitalise tag strings

def mdH(title, level):
    return f'{"#"*level} {title}\n'

def mdLinkList(stringList, level):
    md = ""
    indent = "    " * level
    for item in stringList:
        md += f'{indent}- [[{item}]]\n'
    return md

class Author:
    def __init__(self, name):
        self.name = name
        self.books = []

    def addBook(self, title):
        self.books.append(title)

    def markdown(self):
        md  = mdH(self.name,1)
        md += f'{mdTag("author")} {mdTag("Goodreads")}\n'
        md += mdH("Books in my collection:",3)
        md += mdLinkList(self.books,0)

        return md

class Book:
    def __init__(self, book):
        self.book = book
        ## CSV columns:
        # Book Id
        # Title
        # Author
        # Author l-f
        # Additional Authors
        # ISBN
        # ISBN13
        # My Rating
        # Average Rating
        # Publisher
        # Binding
        # Number of Pages
        # Year Published
        # Original Publication Year
        # Date Read
        # Date Added
        # Bookshelves
        # Bookshelves with positions
        # Exclusive Shelf
        # My Review
        # Spoiler
        # Private Notes
        # Read Count
        # Owned Copies


        # Removed from book title
        #   # don't want new tags!
        #   /  "     "   new directory! (we use title as a filename)
        self.title = self.book["Title"].replace("#","").replace("/"," ")

        # replace square brackets in the title with round ones - avoid phantom wikilinks
        self.title = self.title.replace("[","(").replace("]",")")
        self.publisher = self.book['Publisher']
        self.id = self.book["Book Id"]
        self.rating = self.book["My Rating"]
        self.shelves = self.book["Bookshelves"]
        self.review = self.book["My Review"]
        self.authorName = self.book['Author'].strip()

        # turn otherauthors into an array
        if self.book['Additional Authors'] == "":
            self.otherAuthors = []
        else:
            self.otherAuthors = self.book['Additional Authors'].split(',')

        #print(f'authorName: {self.authorName} otherAuthors:{self.otherAuthors}')
        self.authorNames =  [self.authorName]
        self.authorNames.extend(self.otherAuthors)
        #print(f'authorNames: {self.authorNames}')

        # Construct the goodreads URL
        self.url = f'https://www.goodreads.com/book/show/{self.id}'

    def authorMarkdown(self):
        # Render each author as a wikilink
        md = f'[[{self.authorName}]]'
        if self.otherAuthors != []:
            md += " with "
            first = True
            for oa in self.otherAuthors:
                if first != True:
                    md += ', '
                md += f'[[{oa}]]'
                first = False
        return md


    def markdown(self):
        authorMarkdown = self.authorMarkdown()
        #print(f'authorMarkdown: {authorMarkdown}')
        doc = (
          f'# {self.title}\n'
          f'#Book #Goodreads\n'
          f'- Written by {self.authorMarkdown()}\n'
          f'- Publisher: {self.publisher}\n'
          f'- [Details on Goodreads]({self.url})\n'
          )
        if self.rating != "0":
          doc += f'- My rating: {self.rating} Stars\n'

        if self.shelves != "":
          # Convert each shelf name into a tag
          shelves = "#" + self.shelves.replace(', ',', #')
          #print(f'Shelves: {self.shelves}  Tagged:{shelves}')
          doc += f'- Shelves: {shelves}\n'

        if self.review != "":
            # A little HTML translation
            rev = re.sub("<br/>","\n", self.review)
            rev = re.sub("<strong>","**", rev) # Render 'strong' as bold
            rev = re.sub("</strong>","**", rev)

            doc += f'### My Review\n{rev}\n'
        return doc

class Library:
    def __init__(self, filename):
        # opening the file using "with"
        # statement
        self.authors = {} # Define authors as a dictionary so that we can retrieve them by name
        self.books = []   # Simple list of books
        self.ids = []

        #with open('examples/history.txt', r) as oldIds:
            # get the old IDs

        with open(filename, 'r') as data:
          # for each line in the CSV
          for bookItem in csv.DictReader(data):
              #print('Creating a book')
              book = Book(bookItem)          # create a new book
              self.ids.append(book.id)
              self.books.append(book)             # Add this book to the list
              for name in book.authorNames:  # for each author of the book
                  # if the author has not yet been recorded, do it now
                  if not name in self.authors:
                      self.authors[name] = Author(name) # add the author if they aren't already known

                  # add this book title to the author's works
                  self.authors[name].addBook(book.title)

    def printBooks(self):
        for book in self.books:
            print(book.markdown())
            print("-----------------------------")

    def printAuthors(self):
        for authorName in list(self.authors.keys()):
            print(self.authors[authorName].markdown())

    def saveIds(self, fileName):
        with open(fileName, 'w') as idfile:
            for id in self.ids:
                idfile.write(f'{id}\n')

    def saveMarkdown(self, directory):
        for authorName in self.authors.keys():
            author = self.authors[authorName]
            file = open(f'./{directory}/{authorName}.md','w')
            file.write(author.markdown())
            file.close()

        for book in self.books:
            file = open(f'{directory}/{book.title}.md', 'w')
            file.write(book.markdown())
            file.close


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
csvFileName = "goodreads_library_export.csv"
mdDirectory = "Goodreads Library"
bookIdFileName = "libraryIds.txt"


# Initilise the library object
if not os.path.exists(csvFileName):
    print(f'Could not find {csvFileName}')
    sys.exit(1)
else:
    library = Library(csvFileName)

# Create the 'Goodreads Library' directory and save the markdown files
if os.path.exists(mdDirectory):
    if not os.path.isdir(mdDirectory):
        print('There is a file called Goodreads Library - fix this - should be a directory!')
        sys.exit(1)
    else:                                           # Directory already exists
        library.saveMarkdown(mdDirectory)
        library.saveIds(bookIdFileName)
        sys.exit(0)
else: # Directory does not yet exist
    os.mkdir(mdDirectory)
    library.saveMarkdown(mdDirectory)
    library.saveIds(bookIdFileName)
    sys.exit(0)
