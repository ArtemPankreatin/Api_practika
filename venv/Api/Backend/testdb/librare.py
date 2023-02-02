from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
from .forms import *
from .models import User, Book
from array import *
from datetime import date
from .auth import get_cookie, return_response



# Create your views here.
@csrf_exempt
def Librare(request):
        parsed_data = JSONParser().parse(request)

        if request.method == 'BOOKS_LIST':                  #done
            response = ""
            data = Book.objects.values()
            if data.__len__() == 0:
                return HttpResponse("Empty table.")
            else:
                for record in data:
                    response+=str({"Название":record["name"]})+"\n"
                return HttpResponse(response)
        if request.method == 'BOOK_INFO':                #done
            book = Book.objects.get(name=parsed_data["name"])
            if book:
                book_data = {}
                book_data["Название"]=book.name
                book_data["Автор"] = ", ".join([Author.objects.get(id=int(i)).get_username() for i in book.id_author])
                book_data["Жанр"] = ", ".join([Genre.objects.get(id=int(i)).get_username() for i in book.id_genre])
                book_data["Дата написания"] = str(book.date_of_issue)
                return HttpResponse(str(book_data))
            else:
                return HttpResponse("Not valid data or this user already exists.")  
         
            
        user, cookie, user_name = get_cookie(request)

        if user:
            if request.method == 'NEW_BOOK' and user.role == "admin": #done
                date_book = [int(i) for i in parsed_data['date_of_issue'].split('.')] 
                parsed_data['date_of_issue'] = date(date_book[0],date_book[1],date_book[2])
                parsed_data["id_genre"] = [str(i) for i in parsed_data["id_genre"].split(",")]
                parsed_data["id_author"] = [str(i) for i in parsed_data["id_author"].split(",")]
                book_record = BookModel(data=parsed_data)
                if book_record.is_valid():
                    book_record.save()
                    return return_response("Record created.", cookie,user_name)
                else:
                    return return_response("Not valid data or this book already exists.", cookie,user_name)
                  
            elif request.method == 'ERASE_BOOK' and user.role == "admin": #done
                response = []
                book_record = Book.objects.get(name=parsed_data["name"])
                if book_record:
                    book_record.delete()
                    return return_response("Record deleted.", cookie, user_name)
                else:
                    return return_response("No such record", cookie, user_name)
            elif request.method == 'EDIT_LIST_OF_FAVORITE':
                user.list_of_favorite_books = [str(i) for i in parsed_data["list_of_favorite_books"].split(",")]
                user.save()
                return HttpResponse("Succesfully edited!")
            else:
                return return_response("This methon is not allowed for you.", cookie, user_name) 
            

                       
        else:
            return HttpResponse("You have to log in first.") 
            

            