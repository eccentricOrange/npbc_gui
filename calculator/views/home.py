from datetime import timezone
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from calculator import helpers, models
from pathlib import Path
from json import load
from django.utils import timezone



def home(request: HttpRequest) -> HttpResponse:
    
    papers = helpers.get_all_papers()
    # papers = load((Path(__file__).parent.parent / "exp.json").open('r'))

    month = int(request.GET.get("month", 0))
    year = int(request.GET.get("year", 0))
    paper_id = int(request.GET.get("paper", 0))

    if not (month and year and 1 <= month <= 12):
        month = timezone.now().month
        year = timezone.now().year

    if not (paper_id and paper_id in (paper["id"] for paper in papers)):
        paper_id = models.Paper.objects.first().id


    context = {
        "papers": papers,
        "total_cost": 200,
        "calendar": helpers.get_delivery_data(month, year, paper_id)[0],
        "weekdays": helpers.get_delivery_data(month, year, paper_id)[1]
    }

    return render(request, "calculator/home.html", context)


def get_calculated_cost(request: HttpRequest) -> HttpResponse:
    
    paper_id = int(request.GET.get("paper", 0))
    month = int(request.GET.get("month", 0))
    year = int(request.GET.get("year", 0))

    if not (month and year and 1 <= month <= 12):
        return HttpResponse("Invalid month or year")
    
    if not (paper_id and paper_id in (paper["id"] for paper in helpers.get_all_papers())): 
        return HttpResponse("Invalid paper id")
    
    cost = helpers.calculate_cost_of_one_paper(
        helpers.get_number_of_each_weekday(month, year),
        models.UndeliveredDates.objects.filter(
            paper=models.Paper.objects.get(id=paper_id),
            date__month=month,
            date__year=year
        ).values_list('date', flat=True),
        models.Cost.objects.filter(paper=models.Paper.objects.get(id=paper_id)).order_by('day').values_list('cost', flat=True),
        models.Cost.objects.filter(paper=models.Paper.objects.get(id=paper_id)).order_by('day').values_list('delivery', flat=True)
    )

    return HttpResponse(cost)


def get_calendar(request: HttpRequest) -> HttpResponse:
    
    paper_id = int(request.GET.get("paper", 0))
    month = int(request.GET.get("month", 0))
    year = int(request.GET.get("year", 0))

    if not (month and year and 1 <= month <= 12):
        return HttpResponse("Invalid month or year")
    
    if not (paper_id and paper_id in (paper["id"] for paper in helpers.get_all_papers())): 
        return HttpResponse("Invalid paper id")
    
    calendar = helpers.get_delivery_data(month, year, paper_id)[0]

    return HttpResponse(calendar)


def register_undelivered_date(request: HttpRequest) -> HttpResponse:
    
    paper_id = int(request.POST.get("paper", 0))
    month = int(request.POST.get("month", 0))
    year = int(request.POST.get("year", 0))
    day = int(request.POST.get("day", 0))

    if not (month and year and 1 <= month <= 12):
        return HttpResponse("Invalid month or year")
    
    if not (paper_id and paper_id in (paper["id"] for paper in helpers.get_all_papers())):
        return HttpResponse("Invalid paper id")
    
    if not (day and 1 <= day <= 31):
        return HttpResponse("Invalid day")
    
    if models.UndeliveredDates.objects.filter(
        paper=models.Paper.objects.get(id=paper_id),
        date__month=month,
        date__year=year,
        date__day=day
    ).exists():
        return HttpResponse("Date already exists")
    
    models.UndeliveredDates.objects.create(
        paper=models.Paper.objects.get(id=paper_id),
        date=timezone.datetime(year, month, day)
    )

    return HttpResponse("Success")