from django.shortcuts import render
from django.db import connection
from .models import *
from django.core.cache import cache
from django.shortcuts import HttpResponseRedirect


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

def Rankings(request,X=9999,genre = 'defValue'):
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT genre FROM GenresWithMoreThanFiveP
        """)
        sql_res1 = dictfetchall(cursor)

        cursor.execute("""
                            select hid from Households
                        """)
        sql_res_hid = dictfetchall(cursor)

        cursor.execute("""
                                    select title from Programs
                                """)
        sql_res_programs_names = dictfetchall(cursor)



        cursor.execute("""select distinct genre, count(distinct title) as CountPrograms
                            from Programs
                            where genre is not null
                            group by genre
                            HAVING count(distinct title)>=5
                                               """)
        at_least_five = dictfetchall(cursor)

        cursor.execute("""
        select title,count(title) countRanks
                            from ProgramRanks
                            group by title
                            having count(title) >= %s;
                                                       """, [X])
        spoken_program = dictfetchall(cursor)

        cursor.execute("""
        select top 5 genre,pr.title,round(avg(cast(pr.rank as float)),2) as Average_Rank
        from ProgramRanks pr, (select pp.title,count(pp.title) countRanks ,min(p.genre)  as genre
                                    from ProgramRanks pp,Programs p
                                    where pp.title = p.title and genre = %s -- put here the parameter
                                    group by pp.title
                                    having count(pp.title) >= %s) as Spoken
        where Spoken.title = pr.title and genre is not null
        group by genre,pr.title
        order by round(avg(cast(pr.rank as float)),2) desc""", [genre, X])

        top_five_spoken_genre = dictfetchall(cursor)


        cursor.execute("""select title, 0 as Average_Rank
            from  Programs p1
                            where title not in (select pr.title
                                    from ProgramRanks pr, (select pp.title,count(pp.title) countRanks ,min(p.genre)  as genre
                                                                from ProgramRanks pp,Programs p
                                                                where pp.title = p.title and p.genre = %s-- put here the parameter
                                                                and p1.genre = p.genre
                                                                group by pp.title
                                                                having count(pp.title) >= %s) as Spoken
                                    where Spoken.title = pr.title) and genre = %s """, [genre, X, genre])
        not_spoken_titles = dictfetchall(cursor)

        how_many_add = 5 - len(top_five_spoken_genre)
        if how_many_add > 0 and genre != 'defValue':
            for i in range(how_many_add):
                top_five_spoken_genre.append(not_spoken_titles[i])

#רשימה של מילונים

    return render(request, 'Rankings.html', {'sql_res1': sql_res1, 'sql_res_hid': sql_res_hid,
                                             'sql_res_programs_names': sql_res_programs_names,
                                             'at_least_five': at_least_five,'spoken_program': spoken_program,
                                             'top_five_spoken_genre': top_five_spoken_genre})

def addNewRank(request):
    if request.method == 'POST' and request.POST:
        title = request.POST["title"]
        hid = request.POST["hID"]
        rank = request.POST["rank"]


        with connection.cursor() as cursor:
            cursor.execute(""" select %s,%s from ProgramRanks""", [title, hid])
            all_title_hid = dictfetchall(cursor)
            if len(all_title_hid) > 0:
                cursor.execute("""DELETE FROM ProgramRanks WHERE title = %s and hid = %s""", [title, hid])

            cursor.execute("""INSERT INTO ProgramRanks (title, hID,rank) VALUES (%s, %s,%s)""", [title, hid, rank])
        connection.close()

    return Rankings(request)



def submitNumber(request):
    if request.method == 'POST' and request.POST:
        X = request.POST["minNumber"]
        genre = request.POST["genre"]
        return Rankings(request, X, genre)






















































































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
                    return Records(request, True, "The program is ordered by this family already!",False,"")
        for row in recordReturns:
            if row['title'] == input_title and int(row['hID']) == int(input_hid):
                return Records(request, True, "The movie was already ordered by this family before!",False,"")
        for row in famsWithChildren:
            if int(row['hID']) == int(input_hid):
                for row in allTitles:
                    if row['title'] == input_title:
                        if str(row['genre'])==str("Reality") or str(row['genre'])==str("Adults Only"):
                            return Records(request, True, "The program genre is restricted to families with children!",False,"")

        return Records(request,False,"",False,"")



def returnRecord(request):
    if request.method == 'POST' and request.POST:
        with connection.cursor() as cursor:
            cursor.execute("""
                               SELECT * FROM RecordOrders
               """)
            alreadyOrdered = dictfetchall(cursor)
        connection.close()
        input_hid = request.POST["hid_2"]
        input_title = request.POST["title_2"]
        if (programExist(input_title) == False):
            return Records(request, False, "", True, "Title does not exist!")
        titleOrdered=False
        for row in alreadyOrdered:
            if row['title'] == input_title:
                titleOrdered=True
                if int(row['hID']) != int(input_hid):
                    return Records(request, False, "", True, "The family does not hold this title")
        if titleOrdered!=True:
            return Records(request, False, "", True, "Title is not exist in the order list")
        try:
            record_order = Recordorders.objects.get(pk=input_title)
            record_order.delete()
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO RecordReturns (title, hID) VALUES (%s, %s)""",[input_title,input_hid])
            connection.close()
        except Recordorders.DoesNotExist:
            # Handle the exception
            return Records(request, False, "",True,"exception")
        cause="Return the program " + input_title + " for family number " + input_hid + " was successfully done"


        return Records(request,False,"",True,cause)

