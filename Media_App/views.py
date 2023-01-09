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

        cursor.execute("""select top 5 genre,pr.title,round(avg(cast(pr.rank as float)),2) as Average_Rank
        from ProgramRanks pr, (select pp.title,count(pp.title) countRanks ,min(p.genre)  as genre
                                    from ProgramRanks pp,Programs p
                                    where pp.title = p.title and genre = %s -- put here the parameter
                                    group by pp.title
                                    having count(pp.title) >= %s) as Spoken
        where Spoken.title = pr.title and genre is not null
        group by genre,pr.title
        order by round(avg(cast(pr.rank as float)),2) desc""", [genre, X])

        top_five_spoken_genre = dictfetchall(cursor)


        cursor.execute(""" select title, 0 as Average_Rank
                            from  Programs p1
                            where title not in (select pr.title
                                    from ProgramRanks pr, (select pp.title,count(pp.title) countRanks ,min(p.genre)  as genre
                                                                from ProgramRanks pp,Programs p
                                                                where pp.title = p.title and p.genre = %s -- put here the parameter
                                                                and p1.genre = p.genre
                                                                group by pp.title
                                                                having count(pp.title) >= %s) as Spoken
                                    where Spoken.title = pr.title) and genre is not null
                                    """, [genre, X])
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


def Records(request):
    return render(request,'Records.html')


def addNewRank(request):
    if request.method == 'POST' and request.POST:
        title = request.POST["title"]
        hid = request.POST["hID"]
        rank = request.POST["rank"]
        new_content = Programranks(title = Programs(title),
                              hid = Households(hid),
                              rank = int(rank))
        new_content.save()
    return Rankings(request)

#





def submitNumber(request):
    if request.method == 'POST' and request.POST:
        X = request.POST["minNumber"]
        genre = request.POST["genre"]
        return Rankings(request, X, genre)

# Create your views here.

# QUERY 5
# SELECT TOP 5 PRT.title,genre,Rank_Times,
#        CASE
#            WHEN Rank_Times<=6 THEN 0
#            WHEN Rank_Times IS NULL THEN 0
#            ELSE rank
#            END AS Updated_Rank
# FROM ProgramsRankTime PRT
#     LEFT JOIN Programs_AVG_Rank PAR
#         ON PAR.title=PRT.title
# WHERE genre ='Action'
# ORDER BY genre,Updated_Rank DESC,title ASC

