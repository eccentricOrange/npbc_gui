from django.shortcuts import render
from calculator import helpers
from pathlib import Path
from json import load

papers = load((Path(__file__).parent.parent / "exp.json").open('r'))


def home(request):
    
    papers = helpers.get_all_papers()

    context = {
        "papers": papers,
        "total_cost": 200
    }

    return render(request, "calculator/home.html", context)