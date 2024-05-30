import pandas as pd
import numpy as np
import logging


def get_historical_average_spending(df, year, month, week_of_month):
    previous_data = df[(df['year'] != year) | (df['month'] != month)]
    week_data = previous_data[previous_data['week_of_month'] == week_of_month]
    if not week_data.empty:
        return week_data[week_data['amount'] < 0]['amount'].mean()
    return 0

def get_current_week_spending(df, year, month, week_of_month):
    current_week_data = df[(df['year'] == year) & (df['month'] == month) & (df['week_of_month'] == week_of_month)]
    return current_week_data[current_week_data['amount'] < 0]['amount'].sum()

def get_historical_average_earnings(df, year, month, week_of_month):
    previous_data = df[(df['year'] != year) | (df['month'] != month)]
    week_data = previous_data[previous_data['week_of_month'] == week_of_month]
    if not week_data.empty:
        return week_data[week_data['amount'] > 0]['amount'].mean()
    return 0

def get_current_week_earnings(df, year, month, week_of_month):
    current_week_data = df[(df['year'] == year) & (df['month'] == month) & (df['week_of_month'] == week_of_month)]
    return current_week_data[current_week_data['amount'] > 0]['amount'].sum()

def get_monthly_totals(df, year, month):
    current_month_data = df[(df['year'] == year) & (df['month'] == month)]
    total_spent = current_month_data[current_month_data['amount'] < 0]['amount'].sum()
    total_earned = current_month_data[current_month_data['amount'] > 0]['amount'].sum()
    return total_spent, total_earned

def get_overall_totals(df):
    total_spent = df[df['amount'] < 0]['amount'].sum()
    total_earned = df[df['amount'] > 0]['amount'].sum()
    return total_spent, total_earned

def get_historical_monthly_totals(df, year, month):
    previous_data = df[(df['year'] != year) | (df['month'] != month)]
    total_spent = previous_data[previous_data['amount'] < 0]['amount'].sum()
    total_earned = previous_data[previous_data['amount'] > 0]['amount'].sum()
    return total_spent, total_earned



def compare_last_three_analyses(analyses):
    logger = logging.getLogger(__name__)
    logger.debug(f"Retrieved analyses: {analyses}")

    if len(analyses) < 3:
        raise ValueError("Not enough analyses to compare. At least 3 analyses are required.")

    comparison_results = []

    for i in range(len(analyses) - 2):
        analysis1 = analyses[i]
        analysis2 = analyses[i + 1]
        analysis3 = analyses[i + 2]

        comparison = {
            "analysis1": analysis1,
            "analysis2": analysis2,
            "analysis3": analysis3,
            "spending_comparison": {
                "analysis1_vs_analysis2": analysis2["current_week_spending"] - analysis1["current_week_spending"],
                "analysis2_vs_analysis3": analysis3["current_week_spending"] - analysis2["current_week_spending"]
            },
            "earnings_comparison": {
                "analysis1_vs_analysis2": analysis2["current_week_earnings"] - analysis1["current_week_earnings"],
                "analysis2_vs_analysis3": analysis3["current_week_earnings"] - analysis2["current_week_earnings"]
            },
            "monthly_spending_comparison": {
                "analysis1_vs_analysis2": analysis2["current_month_spending"] - analysis1["current_month_spending"],
                "analysis2_vs_analysis3": analysis3["current_month_spending"] - analysis2["current_month_spending"]
            },
            "monthly_earnings_comparison": {
                "analysis1_vs_analysis2": analysis2["current_month_earnings"] - analysis1["current_month_earnings"],
                "analysis2_vs_analysis3": analysis3["current_month_earnings"] - analysis2["current_month_earnings"]
            }
        }

        comparison_results.append(comparison)

    return comparison_results