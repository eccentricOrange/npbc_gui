from datetime import timezone
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from calculator import helpers, models
from pathlib import Path
from json import load
from django.utils import timezone



def home(request: HttpRequest) -> HttpResponse:
    
    # papers = helpers.get_all_papers()
    papers = load((Path(__file__).parent.parent / "exp.json").open('r'))

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
        "calendar": helpers.get_delivery_data(month, year, paper_id)[0]
    }

    return render(request, "calculator/home.html", context)