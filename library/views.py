from django.shortcuts import render, redirect, get_object_or_404
from .models import Author, Book
from .forms import AuthorForm, BookForm

def index(request):
    return render(request, 'library/index.html')

def author_list(request):
    authors = Author.objects.all()
    return render(request, 'library/author_list.html', {'authors': authors})

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            author = form.save()
            return redirect('author_detail', id=author.id)
    else:
        form = AuthorForm()
    return render(request, 'library/create_author.html', {'form': form})

def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            title = form.cleaned_data['title']
            authors = form.cleaned_data['authors']
            
            if Book.objects.filter(title=title, authors__in=authors.all()).exists():
                form.add_error('title', 'Книга с таким названием и авторами уже существует.')
            else:
                book.save()
                form.save_m2m()
                return redirect('book_detail', id=book.id)
    else:
        form = BookForm()
    return render(request, 'library/create_book.html', {'form': form})



def author_detail(request, id):
    author = get_object_or_404(Author, id=id)
    books = Book.objects.filter(authors__id=id)
    return render(request, 'library/author_detail.html', {'author': author, 'books': books})

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'library/book_detail.html', {'book': book})
