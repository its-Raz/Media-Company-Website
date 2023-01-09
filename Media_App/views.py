from django.shortcuts import render
from django.db import connection

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

def Records(request):
    return render(request,'Records.html')
# Create your views here.


