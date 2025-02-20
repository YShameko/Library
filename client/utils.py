from book.models import Books, Borrowed

def available_books(list_of_books):
    available_books_list = []
    for book in list_of_books:
        borrowed_qty = Borrowed.objects.filter(book_id=book, closed=False).count()
        if book.quantity - borrowed_qty > 0:
            available_books_list.append(book)

    return available_books_list