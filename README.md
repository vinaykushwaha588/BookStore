## first you need to create install python3 on the system after that create venv 
1.1 - python3 -m venv myenv
1.2 for windows- myenv\Scripts\activate
1.2 for ubuntu- source myenv/bin/activate
## install requirements
2.1 - pip install -r requirements.txt
2.2 -> run- python manage.py runserver
# Django Project Name
BooksStore

## POST_MAN Payload Collections
link - https://api.postman.com/collections/36505766-18fbafbe-5995-41a5-83db-3fe79ade02b5?access_key=PMAT-01J4HVZWYYRQHHGV7KX1RTSX5E

## Contributing API END POINT
● POST: http://localhost:8000}/api/user/signup/: Create a new User.
● POST: http://localhost:8000/api/user/login: Login User.
● POST: http://localhost:8000/api/book/fetch_and_save_books/: Fetch a Book From Google API and store on the db.
● GET: http://localhost:8000//api/book/book_list/: Book List.
● POST: http://localhost:8000/api/recommend/comment/: Comment on the Book.
● PUT : http://localhost:8000/api/recommend/1/like/: Like Book.
● GET http://localhost:8000/api/recommend/book_recommendations/?book_id=12: Book Recomendations.
