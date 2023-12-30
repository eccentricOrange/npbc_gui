from calendar import monthcalendar, day_name as weekday_names_iterable
from typing import Generator
from calculator import models
from datetime import date
import numpy
import numpy.typing

WEEKDAY_NAMES = tuple(weekday_names_iterable)

def get_all_papers() -> list[dict]:
    """
    Required structure is a list of this dictionary:
    ```py
    {
        "id": int,
        "title": str,
        "days": [
            {
                "id": int,
                "delivery": bool,
                "cost": float
            }
        ]
    }
    ```
    """

    papers = models.Paper.objects.all()

    papers_list = []

    for paper in papers:
        paper_dict = {
            "id": paper.id,
            "title": paper.title,
            "days": []
        }

        costs = models.Cost.objects.filter(paper=paper)

        for cost in costs:
            paper_dict["days"].append({
                "id": cost.id,
                "delivery": cost.delivery,
                "cost": cost.cost
            })

        papers_list.append(paper_dict)

    return papers_list


def get_number_of_each_weekday(month: int, year: int) -> Generator[int, None, None]:
    """generate a list of number of times each weekday occurs in a given month (return a generator)
    - the list will be in the same order as WEEKDAY_NAMES (so the first day should be Monday)"""

    # get the calendar for the month
    main_calendar = monthcalendar(year, month)

    # get the number of weeks in that month from the calendar
    number_of_weeks = len(main_calendar)

    # iterate over each possible weekday
    for weekday_index in range(len(WEEKDAY_NAMES)):

        # assume that the weekday occurs once per week in the month
        number_of_weekday: int = number_of_weeks

        # if the first week doesn't have the weekday, decrement its count
        if main_calendar[0][weekday_index] == 0:
            number_of_weekday -= 1
        
        # if the last week doesn't have the weekday, decrement its count
        if main_calendar[-1][weekday_index] == 0:
            number_of_weekday -= 1

        yield number_of_weekday


def calculate_cost_of_one_paper(
        number_of_each_weekday: list[int],
        undelivered_dates: set[date],
        cost_data: numpy.typing.NDArray[numpy.floating],
        delivery_data: numpy.typing.NDArray[numpy.int8]
    ) -> float:
    """calculate the cost of one paper for the full month
    - any dates when it was not delivered will be removed"""
    
    # initialize counters corresponding to each weekday when the paper was not delivered
    number_of_days_per_weekday_not_received = numpy.zeros(len(number_of_each_weekday), dtype=numpy.int8)
    
    # for each date that the paper was not delivered, we increment the counter for the corresponding weekday
    for day in undelivered_dates:
        number_of_days_per_weekday_not_received[day.weekday()] += 1

    return float(numpy.sum(
        delivery_data * cost_data * (number_of_each_weekday - number_of_days_per_weekday_not_received)
    ))


def calculate_cost_of_all_papers(
        number_of_each_weekday: list[int],
    ) -> dict[int, float]:
    """calculate the cost of all papers for the full month"""

    # initialize the dictionary of costs
    total_costs = {}

    # iterate over each paper
    for paper in models.Paper.objects.all():

        # get the cost and delivery data for the paper
        cost_data = numpy.array([
            cost.cost for cost in models.Cost.objects.filter(paper=paper).order_by('day')
        ])
        delivery_data = numpy.array([
            cost.delivery for cost in models.Cost.objects.filter(paper=paper).order_by('day')
        ])

        # calculate the cost of the paper and store it in the dictionary
        total_costs[paper.id] = calculate_cost_of_one_paper(
            number_of_each_weekday,
            set(models.UndeliveredDates.objects.filter(paper=paper).values_list('date', flat=True)),
            cost_data,
            delivery_data
        )

    return total_costs


def get_delivery_data(
        month: int,
        year: int,
        paper_id: int
    ) -> tuple[list[list[dict]], tuple[str, ...]]:
    """
    get the transient delivery data for a given month and paper

    Required structure is a list of lists of tuples:
    ```py
    [   # weeks
        [   # days
            {
                "day": int,
                "undelivered": bool
            }
        ]
    ]
    ```
    """

    # get the paper
    paper = models.Paper.objects.get(id=paper_id)

    # get the delivery data for the paper
    delivery_data = models.UndeliveredDates.objects.filter(
        paper=paper,
        date__month=month,
        date__year=year
    ).values_list('date', flat=True)

    list_of_days = tuple(map(
        lambda underlivered_date: underlivered_date.day,
        delivery_data
    ))

    # get the calendar for the month
    main_calendar = monthcalendar(year, month)

    formatted_delivery_data = [
        [
            {
                "day": day,
                "undelivered": day in list_of_days
            } for day in week
        ] for week in main_calendar
    ]

    return formatted_delivery_data, WEEKDAY_NAMES


def get_calculated_cost(
        month: int,
        year: int,
    ) -> dict[int, float]:
    """get the calculated cost for a given month and paper"""

    # get the number of each weekday in the month
    number_of_each_weekday = tuple(get_number_of_each_weekday(month, year))

    # get the cost of each paper
    total_costs = calculate_cost_of_all_papers(number_of_each_weekday)

    # return the total cost
    return total_costs