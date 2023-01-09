from django.shortcuts import render
from django.db import connection
from .models import *

def dictfetchall(cursor):
    # Returns all rows from a cursor as a dict '''
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def index(request):
    return render(request,'index.html')

def Query(request):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT DISTINCT TitlesReturnsByZeroFam.genre,AGenresMaxDuration.title,MaxDuration
FROM
    AGenresMaxDuration JOIN TitlesReturnsByZeroFam
ON
    AGenresMaxDuration.title=TitlesReturnsByZeroFam.title
ORDER BY genre
                            """)

        sql_res = dictfetchall(cursor)

        cursor.execute("""
        SELECT LR.title AS Title,rank AS Average_Rank FROM More_Than_3_Legal_Rates LR JOIN Programs_AVG_Rank PR ON LR.title=PR.title
ORDER BY rank DESC ,LR.title
                                       
                                            """)
        sql_res2 = dictfetchall(cursor)

        cursor.execute("""
        SELECT title FROM HIGH_LEVEL_PROGRAM WHERE title NOT IN (SELECT title FROM ProgramRanks WHERE rank<2) ORDER BY title ASC
                           
                            """)
        sql_res3 = dictfetchall(cursor)

        return render(request, 'Query.html', {'sql_res': sql_res, 'sql_res2': sql_res2, 'sql_res3': sql_res3})

def Rankings(request):
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT genre FROM GenresWithMoreThanFiveP
    """)
        sql_res1 = dictfetchall(cursor)
    return render(request, 'Rankings.html', {'sql_res1': sql_res1})

def Records(request,OrderNotApproved=False,cause="",ReturnNotApproved=False,cause_1=""):
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT TOP 3 hID,COUNT(title) AS Total_Orders FROM Ever_Ordered GROUP BY hID ORDER BY Total_Orders DESC,hID
    """)
        sql_res1 = dictfetchall(cursor)

    return render(request, 'Records.html', {'sql_res1': sql_res1,'OrderNotApproved':OrderNotApproved,'cause':cause,
                                            'ReturnNotApproved':ReturnNotApproved,'cause_1':cause_1})
# Create your views here.
def programExist(input_title):
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT title,genre FROM Programs
    """)
        allTitles = dictfetchall(cursor)
    for row in allTitles:
        if row['title'] == input_title:
            return True
    return False


def orderNewRecord(request):
    if request.method == 'POST' and request.POST:
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT title,genre FROM Programs
        """)
            allTitles = dictfetchall(cursor)
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT hID FROM FamilyNumOfOrders WHERE NumberOfOrders=3
        """)
            famWithThree = dictfetchall(cursor)
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT * FROM RecordOrders
        """)
            alreadyOrdered = dictfetchall(cursor)
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT * FROM RecordReturns
        """)
            recordReturns = dictfetchall(cursor)
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT hID
                        FROM Households
                        WHERE hID
                        NOT IN
                         (SELECT hID FROM HouseHoldsZeroChildren)
                                                                 """)
            famsWithChildren = dictfetchall(cursor)
        input_hid = request.POST["hid"]
        input_title = request.POST["title"]
        if programExist(input_title) == False:
            return Records(request, True, "Title does not exist!",False,"")
        for row in famWithThree:
            if int(row['hID']) == int(input_hid):
                return Records(request, True, "Family is Already holds 3 titles!",False,"")
        for row in alreadyOrdered:
            if row['title']==input_title:
                if int(row['hID']) != int(input_hid):
                    return Records(request, True, "The movie is ordered by another family and yet to be returned!",False,"")
                if int(row['hID']) == int(input_hid):
                    return Records(request, True, "The movie is ordered by this family!",False,"")
        for row in recordReturns:
            if row['title'] == input_title and int(row['hID']) == int(input_hid):
                return Records(request, True, "The movie was already ordered by this family before!",False,"")
        for row in famsWithChildren:
            if int(row['hID']) == int(input_hid):
                for row in allTitles:
                    if row['title'] == input_title:
                        if str(row['genre'])==str("Reality") or str(row['genre'])==str("Adults Only"):
                            return Records(request, True, "The program genre is restricted to families with children!",False,"")


        new_content = Programs(title=input_title)
        new_content.save()
        new_content = Households(hid=input_hid)
        new_content.save()
        new_content = Recordorders(title=Programs(input_title),hid=Households(input_hid))
        new_content.save()
        return Records(request,False,"",False,"")



def returnRecord(request):
    if request.method == 'POST' and request.POST:
        with connection.cursor() as cursor:
            cursor.execute("""
                        SELECT * FROM RecordOrders
        """)
            alreadyOrdered = dictfetchall(cursor)
        input_hid = request.POST["hid_2"]
        input_title = request.POST["title_2"]
        if (programExist(input_title) == False):
            return Records(request, False, "",True,"Title does not exist!")
        for row in alreadyOrdered:
            if row['title']==input_title:
                if int(row['hID']) != int(input_hid):
                    return Records(request,False,"", True, "The family does not hold this title")


        Recordorders.objects.filter(pk=input_title).delete()
        # Recordorders.refresh_from_db(self=Recordorders,using=None,fields=None)
        new_content = Programs(title=input_title)
        new_content.save()
        new_content = Households(hid=input_hid)
        new_content.save()
        new_content = Recordreturns(title=Programs(input_title), hid=Households(input_hid))
        new_content.save()
        return Records(request, False, "", False, "")

