import csv  # CSV processing
import re   # Regular expressions

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


        # Remove hash characters from title - we don't want new tags!
        self.title = self.book["Title"].replace("#","")
        self.publisher = self.book['Publisher']
        self.id = self.book["Book Id"]
        self.rating = self.book["My Rating"]
        self.shelves = self.book["Bookshelves"]
        self.review = self.book["My Review"]
        self.authorNames = [self.book['Author'].strip()]
        if (self.book['Additional Authors'] != ''):
          others = self.book['Additional Authors'].split(',')
          [self.authorNames.append(author.strip()) for author in others]
        self.url = f'https://www.goodreads.com/book/show/{self.id}'

    def authorMarkdown(self):
        # Render each author as a wikilink
        authorLinks = [wikiLink(authorName) for authorName in self.authorNames]

        # initialise with the first author in the list
        authorMD = authorLinks[0]

        if (len(authorLinks) > 1):
            authorMD += " with;\n"
            for author in authorLinks[1:-1]:
                authorMD = authorMD + f'    - {author}\n'

        return authorMD


    def markdown(self):
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
          doc += f'- Shelves: {self.shelves}\n'

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

        with open(filename, 'r') as data:
          # for each line in the CSV
          for bookItem in csv.DictReader(data):
              book = Book(bookItem)          # create a new book
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



library = Library("examples/goodreads_library_export.csv")
library.saveMarkdown('examples/library')
