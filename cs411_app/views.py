from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core import serializers

from django.db import connection

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')
    #return HttpResponse("CS 411 Project: Development Environment Setup")


@csrf_exempt
def insert_record(request):
    print(request.POST)

    user_name = str(request.POST["name"])
    user_id = str(request.POST["user_name"])
    age = int(request.POST["age"])
    gender = str(request.POST["gender"])
    state = str(request.POST["state"])




@csrf_exempt
def query_databases(request):
    print(request.POST)

    state_filter = str(request.POST["state"])

    query1 = "SELECT State, Y1999 from pop where STATE = %s"

    query2 = "SELECT causes1.CAUSE_NAME, causes1.STATE, causes1.deaths " + \
            "FROM causes as causes1, (SELECT STATE, max(Deaths) as max_deaths " + \
            "FROM causes  WHERE STATE = %s " + \
            "and C113_CAUSE_NAME!='All Causes' GROUP BY STATE) causes2 " + \
            "WHERE causes1.STATE = causes2.STATE and causes2.max_deaths = causes1.DEATHS;"

    cursor = connection.cursor()
    cursor.execute(query2, [state_filter])
    result = cursor.fetchall()

    columns = cursor.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in result]

    print(cursor._last_executed)
    print(result)

    return render(request, 'result.html', {'result': result})
