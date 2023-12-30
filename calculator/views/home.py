from datetime import date, timedelta, timezone
from http import HTTPStatus
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from calculator import helpers, models
from pathlib import Path
from json import load
from django.utils import timezone


def home(request: HttpRequest) -> HttpResponse:

    papers = helpers.get_all_papers()

    month = int(request.GET.get("month", 0))
    year = int(request.GET.get("year", 0))
    paper_id = int(request.GET.get("paper", 1))

    if not (month and year and 1 <= month <= 12):
        month = timezone.now().month
        year = timezone.now().year

    if not (paper_id and paper_id in (paper["id"] for paper in papers)):
        paper_id = models.Paper.objects.first().id

    calculated_costs = helpers.get_calculated_cost(month, year)

    time_change_data = {
        'next_month': (date(year, month, 28) + timedelta(days=4)).month,
        'next_year': (date(year, month, 28) + timedelta(days=4)).year,
        'previous_month': (date(year, month, 1) - timedelta(days=4)).month,
        'previous_year': (date(year, month, 1) - timedelta(days=4)).year,
        'current_month': month,
        'current_year': year
    }

    for paper in papers:
        paper["total_cost"] = calculated_costs[paper["id"]]

    context = {
        "papers": papers,
        "calendar": helpers.get_delivery_data(month, year, paper_id)[0],
        "weekdays": helpers.get_delivery_data(month, year, paper_id)[1],
        "currentMonth": {
            "month": month,
            "year": year
        },
        "currentPaper": paper_id,
        "total_cost": sum(calculated_costs.values()),
        "tcd": time_change_data
    }

    return render(request, "calculator/home.html", context)


def get_calendar(request: HttpRequest) -> HttpResponse:

    paper_id = int(request.GET.get("paper", 0))
    month = int(request.GET.get("month", 0))
    year = int(request.GET.get("year", 0))

    if not (month and year and 1 <= month <= 12):
        return HttpResponse("Invalid month or year", status=HTTPStatus.BAD_REQUEST)

    if not (paper_id and paper_id in (paper["id"] for paper in helpers.get_all_papers())):
        return HttpResponse("Invalid paper id", status=HTTPStatus.BAD_REQUEST)

    calendar = helpers.get_delivery_data(month, year, paper_id)[0]

    return HttpResponse(calendar, status=HTTPStatus.OK)


def register_undelivered_date(request: HttpRequest) -> HttpResponse:

    response: dict = json.loads(request.body)

    paper_id = int(response.get("paper", 0))
    month = int(response.get("month", 0))
    year = int(response.get("year", 0))
    day = int(response.get("day", 0))

    print(paper_id, month, year, day)


    if not (month and year and 1 <= month <= 12):
        return HttpResponse("Invalid month or year", status=HTTPStatus.BAD_REQUEST)

    if not (paper_id and paper_id in (paper["id"] for paper in helpers.get_all_papers())):
        return HttpResponse("Invalid paper id", status=HTTPStatus.BAD_REQUEST)

    if not (day and 1 <= day <= 31):
        return HttpResponse("Invalid day", status=HTTPStatus.BAD_REQUEST)

    if models.UndeliveredDates.objects.filter(
        paper=models.Paper.objects.get(id=paper_id),
        date__month=month,
        date__year=year,
        date__day=day
    ).exists():
        print("Date already exists")
        return HttpResponse("Date already exists", status=HTTPStatus.CONFLICT)

    models.UndeliveredDates.objects.create(
        paper=models.Paper.objects.get(id=paper_id),
        date=timezone.datetime(year, month, day)
    ).save()

    return HttpResponse("Success", status=HTTPStatus.OK)


def unregister_undelivered_date(request: HttpRequest) -> HttpResponse:

    response: dict = json.loads(request.body)

    paper_id = int(response.get("paper", 0))
    month = int(response.get("month", 0))
    year = int(response.get("year", 0))
    day = int(response.get("day", 0))

    if not (month and year and 1 <= month <= 12):
        return HttpResponse("Invalid month or year", status=HTTPStatus.BAD_REQUEST)

    if not (paper_id and paper_id in (paper["id"] for paper in helpers.get_all_papers())):
        return HttpResponse("Invalid paper id", status=HTTPStatus.BAD_REQUEST)

    if not (day and 1 <= day <= 31):
        return HttpResponse("Invalid day", status=HTTPStatus.BAD_REQUEST)
    
    required_date = models.UndeliveredDates.objects.filter(
        paper=models.Paper.objects.get(id=paper_id),
        date__month=month,
        date__year=year,
        date__day=day
    )

    if not required_date.exists():
        return HttpResponse("Date does not exist", status=HTTPStatus.BAD_REQUEST)

    required_date.delete()

    return HttpResponse("Success", status=HTTPStatus.OK)


def get_calculated_costs(request: HttpRequest) -> HttpResponse:
    print(request)
    
    month = int(request.GET.get("month", 0))
    year = int(request.GET.get("year", 0))

    print(month, year)

    if not (month and year and 1 <= month <= 12):
        return HttpResponse("Invalid month or year", status=HTTPStatus.BAD_REQUEST)

    calculated_costs = helpers.get_calculated_cost(month, year)

    content = {
        "total_cost": sum(calculated_costs.values()),
        "costs": calculated_costs
    }

    return JsonResponse(content, status=HTTPStatus.OK)