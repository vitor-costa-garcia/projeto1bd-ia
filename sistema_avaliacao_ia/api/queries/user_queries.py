from django.db import connection
from django.http import JsonResponse

def get_user(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuario WHERE id = %d", [id])
        result = cursor.fetchall()

    return JsonResponse({"users": result})
    
def get_all_user(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, email FROM usuario", [id])
        result =  cursor.fetchall()
    
    return JsonResponse({"users": result})
