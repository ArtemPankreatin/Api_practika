from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.http import HttpResponse
from .forms import *
from .models import User, Book
from array import *
from datetime import date



# Create your views here.
@csrf_exempt
def Parser(request):

        parsed_data = JSONParser().parse(request)
        

        if request.method == 'GET_USER':                  #done
            response = User.objects.values()
            if response.__len__() == 0:
                return HttpResponse("Empty table.")
            else:
                for record in response:
                    record.pop("id")
                    record.pop("last_login")
                    # record.pop("password")
                return HttpResponse(response)
            
        if request.method == 'CREATE_USER':                #done
            parsed_data["list_of_favorite_books"] = [str(i) for i in parsed_data["list_of_favorite_books"].split(",")]
            response = []
            user_record = UserModel(data=parsed_data)
            if user_record.is_valid():
                user_record.create(user_record.cleaned_data)
                return HttpResponse("Record created.")
            else:
                return HttpResponse("Not valid data or this user already exists.")
            
        if request.method == 'DELETE_USER':                 #done
            response = []
            user_record = User.objects.get(email=parsed_data["email"])
            if user_record:
                user_record.delete()
                return HttpResponse("Record deleted.")
            else:
                return HttpResponse("No such record")
            


        if request.method == 'GET_BOOKS': #done
            response = Book.objects.values()
            if response.__len__() == 0:
                return HttpResponse("Empty table.")
            else:
                for record in response:
                    record.pop("id")
                    record.pop("last_login")
                    record.pop("password")
                return HttpResponse(response)
        
        if request.method == 'CREATE_BOOKS': #done
            response = []
            date_book = [int(i) for i in parsed_data['date_of_issue'].split('.')] 
            date_book.reverse()
            parsed_data['date_of_issue'] = date(date_book[0],date_book[1],date_book[2])
            book_record = BookModel(data=parsed_data)
            if book_record.is_valid():
                book_record.save()
                return HttpResponse("Record created.")
            else:
                return HttpResponse("Not valid data or this book already exists.")
        if request.method == 'DELETE_BOOK': #done
            response = []
            book_record = Book.objects.get(name=parsed_data["name"])
            if book_record:
                book_record.delete()
                return HttpResponse("Record deleted.")
            else:
                return HttpResponse("No such record")
            
        if request.method == "GET_GENRES": #maybe done
            response=""
            data = Genre.objects.values()
            for record in data:
                record.pop("password")
                record.pop("last_login")
                response+=str(record)+"\n"
            return HttpResponse(response)

        if request.method == "CREATE_GENRE": #maybe done
            genre_record = GenreModel(data=parsed_data)
            if genre_record.is_valid():
                genre_record.save()
                return HttpResponse("Record complete.")
            else:
                return HttpResponse("No valid data") 

        if request.method == "DELETE_GENRE": #maybe done
            genre_record = Genre.objects.get(name=parsed_data["name"])
            if genre_record:
                genre_record.delete()
                return HttpResponse("Record deleted.")
            else:
                return HttpResponse("No such record")

        if request.method == "GET_AUTHORS":
            response=""
            data = Author.objects.values()
            for record in data:
                record.pop("password")
                record.pop("last_login")
                response+=str(record)+"\n"
            return HttpResponse(response)

        if request.method == "CREATE_AUTHOR": #maybe done
            author_record = AuthorModel(data=parsed_data)
            if author_record.is_valid():
                author_record.save()
                print(author_record)
                return HttpResponse("Record complete.")
            else:
                return HttpResponse("No valid data") 

        if request.method == "DELETE_AUTHOR": #maybe done
            response = []
            author_record = Author.objects.get(name=parsed_data["name"])
            if author_record:
                author_record.delete()
                return HttpResponse("Record deleted.")
            else:
                return HttpResponse("No such record")
            
            
            
            
        # if request.method == 'GET_OLT':
        #     response = get_db_handle().find({"_id": ObjectId(olt_data["_id"])}, {'_id': False})
        #     if user.can_edit:
        #         try:
        #             response.pop("access")
        #         except:
        #             pass
        #     return return_response(list(response), cookie, user_name)

    #     elif request.method == 'CREATE_OLT' and user.can_edit:
    #         if not list(get_db_handle().find({'ip': olt_data['ip']})):
    #             if olt_data['login'] and olt_data['password']:
    #                 status = get_db_handle().insert_one(olt_data)
    #                 return return_response(f"OLT added successfully.{status}", cookie, user_name)
    #         else:
    #             return return_response("Fail to add OLT. This ip already exists.", cookie, user_name)

    #     elif request.method == 'UPDATE_OLT' and user.can_edit:
    #         result = diff(get_db_handle().find_one({"_id": ObjectId(olt_data["_id"])}, {'_id': False}), olt_data)
    #         id = olt_data.pop("_id")
    #         get_db_handle().replace_one({"_id": ObjectId(id)}, olt_data)
    #         return return_response(list(result), cookie, user_name)

    #     elif request.method == 'DELETE_OLT' and user.can_edit:
    #         response = get_db_handle().delete_one({"_id": ObjectId(olt_data["Id"])}).deleted_count
    #         return return_response(f"Deleted {response} object.", cookie, user_name)

    #     else:
    #         return return_response("Method is not defined.", cookie, user_name)
    # except KeyError:
    #     return JsonResponse("Some data is wrong.", safe=False)
    # except (jwt.exceptions.DecodeError,jwt.exceptions.InvalidTokenError, AttributeError):
    #     return JsonResponse("Invalid token.", safe=False)
    # except Exception as err:
    #     print("shit happens")
    #     return HttpResponse(err)