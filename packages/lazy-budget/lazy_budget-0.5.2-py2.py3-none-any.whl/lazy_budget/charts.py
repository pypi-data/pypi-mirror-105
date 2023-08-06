from itertools import takewhile
from typing import Iterable

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from lazy_budget.budget import Budget, FinancialOperation


def burndown_chart(budget: Budget, operations: Iterable[FinancialOperation]):
    max_date = budget.today
    operations = budget.filter(operations)
    spent_per_day = budget.get_spent_by_day(operations)
    for_df = []
    total_spent = budget.total.amount
    for day in takewhile(lambda x: x <= max_date, iter(budget)):
        budget.today = day
        ops = budget.filter(operations)
        total_spent += spent_per_day[day].amount
        should_be_available = (
            budget.days_left * budget.available_per_day.amount + budget.keep.amount
        )
        for_df.append(
            (
                day.strftime("%d"),
                total_spent,
                should_be_available,
                0,
                budget.available_per_day.amount,
                budget.get_currently_keeping(ops).amount,
                budget.keep.amount,
            )
        )
    df = pd.DataFrame(
        for_df,
        columns=[
            "day",
            "money",
            "should_be_available",
            "zero",
            "available_per_day",
            "currently_keeping",
            "keep",
        ],
    )
    sns.set_theme()
    sns.set_style("darkgrid")

    plt.plot("day", "money", data=df, color="red", label="real burndown")
    plt.plot(
        "day",
        "should_be_available",
        data=df,
        linestyle="dashed",
        color="red",
        label="planned burndown",
    )
    plt.plot("day", "zero", data=df, linestyle="dashed")
    plt.plot("day", "currently_keeping", data=df, color="green", label="real savings")
    plt.plot(
        "day", "keep", data=df, color="green", linestyle=":", label="planned savings"
    )
    plt.legend()
    plt.show()
