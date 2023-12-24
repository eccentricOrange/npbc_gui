"""
Database models

- **Persistent models**: Paper, Cost. These models are stored in the database, and are used every time a calculation is made. They are not supposed to change often.
- **Transient models**: UndeliveredDates. These are used to aide calculations, and may change often. This data persists between sessions, until the user decides to log the calculation.
- **Log models**: Log, DeliveryLog, CostLog. These are not supposed to change once stored.
"""

from django.db import models
from django.utils import timezone


class Paper(models.Model):
    """
    Paper model
    - stores the title of a paper
    - stores discarded papers too, for logging purposes
    """

    title = models.CharField(
        max_length=500,
        unique=True
    )
    discarded = models.BooleanField(default=False)


class Cost(models.Model):
    """
    Cost and delivery model
    - stores the cost of a paper per weekday
    - stores whether the paper is supposed to be delivered per weekday
    """

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    day = models.IntegerField()  # 0-6, weekdays
    delivery = models.BooleanField()
    cost = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['paper', 'day'],
                name='unique_day'
            )
        ]


class UndeliveredDates(models.Model):
    """
    Undelivered dates model
    - stores the dates where a paper was not delivered
    - these are considered in the calculation
    - this data may change
    """

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['paper', 'date'],
                name='unique_undelivered_dates'
            )
        ]


class Log(models.Model):
    """
    Log model
    - stores the calculation date, the target date and the total cost
    - once stored, the data should not change
    """

    calculation_date = models.DateTimeField(default=timezone.now)
    target_date = models.DateField()  # month and year, day must be 1
    total_cost = models.FloatField()


class DeliveryLog(models.Model):
    """
    Delivery log model
    - stores the delivery dates for a paper
    - once stored, the data should not change
    - references the log and the paper
    """

    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['log', 'paper', 'date'],
                name='unique_delivery_log'
            )
        ]


class CostLog(models.Model):
    """
    Cost log model
    - stores the cost for a paper
    - once stored, the data should not change
    - references the log and the paper
    """

    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    cost = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['log', 'paper'],
                name='unique_cost_log'
            )
        ]
