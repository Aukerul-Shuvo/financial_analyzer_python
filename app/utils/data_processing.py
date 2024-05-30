import pandas as pd
import numpy as np

def process_dates(df, date_column='date'):
    df.columns = df.columns.str.strip().str.lower()
    if date_column not in df.columns:
        raise KeyError(f"'{date_column}' column is missing from the dataframe.")
    
    df[date_column] = pd.to_datetime(df[date_column], format='%Y-%m-%d', errors='coerce')
    df = df[df[date_column].notnull()]
    return df

def impute_amounts(df, amount_column='amount', category_column='category'):
    mean_income = df[df[amount_column] > 0][amount_column].mean()
    median_expense = df[df[amount_column] < 0][amount_column].median()
    
    df.loc[df[amount_column].isnull() & (df[category_column] == 'Income'), amount_column] = mean_income
    df.loc[df[amount_column].isnull() & (df[category_column] != 'Income'), amount_column] = median_expense
    return df

def fill_missing_categories(df, amount_column='amount', category_column='category'):
    most_common_category = df[category_column].mode()[0] if not df[category_column].mode().empty else 'Miscellaneous'

    df[category_column] = df.apply(
        lambda row: 'Income' if row[amount_column] > 0 else (most_common_category if pd.isnull(row[category_column]) else row[category_column]),
        axis=1
    )
    return df

def handle_outliers(df, amount_column='amount'):
    q1 = df[amount_column].quantile(0.25)
    q3 = df[amount_column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    df = df[(df[amount_column] >= lower_bound) & (df[amount_column] <= upper_bound)]
    return df

def correct_category_names(df, category_column='category'):
    category_mappings = {
        'Dining Out': 'Dining',
        'Grocery Store': 'Groceries',
        'Electric Bill': 'Utilities',
        'Online Sales': 'Sales',
        'Freelance Client': 'Freelance'
    }
    df[category_column] = df[category_column].map(category_mappings).fillna(df[category_column])
    return df

def validate_geographic_data(df, city_column='city', region_column='region'):
    valid_cities = {
        'Philadelphia': 'PA',
        'Chicago': 'IL',
        'New York': 'NY',
        'Los Angeles': 'CA',
        'San Jose': 'CA',
        'San Diego': 'CA',
        'San Antonio': 'TX',
        'Phoenix': 'AZ',
        'Dallas': 'TX',
        'Houston': 'TX'
    }
    df = df[df.apply(lambda row: valid_cities.get(row[city_column]) == row[region_column], axis=1)]
    return df

def create_derived_features(df, date_column='date'):
    if date_column not in df.columns:
        raise KeyError(f"'{date_column}' column is missing from the dataframe.")
    
    df['day_of_week'] = df[date_column].dt.dayofweek
    df['week_of_month'] = df[date_column].apply(lambda x: (x.day - 1) // 7 + 1)
    df['month'] = df[date_column].dt.month
    df['year'] = df[date_column].dt.year
    print(df)
    return df

def preprocess_data(df):
    df.columns = df.columns.str.strip().str.lower()
    df = process_dates(df)
    df = impute_amounts(df)
    df = fill_missing_categories(df)
    df = validate_geographic_data(df)
    df = create_derived_features(df)
    return df

def preprocess_single_transaction(df):
    df.columns = df.columns.str.strip().str.lower()
    df = process_dates(df)  # Convert date column to datetime
    df = impute_amounts(df)
    df = fill_missing_categories(df)
    df = validate_geographic_data(df)
    df = create_derived_features(df)
    return df
