
import pandas as pd


# Grade Assignment Logic

def get_grade(avg):
    if avg >= 90:
        return 'A+'
    elif avg >= 80:
        return 'A'
    elif avg >= 70:
        return 'B'
    elif avg >= 60:
        return 'C'
    elif avg >= 50:
        return 'D'
    else:
        return 'F'


# Clean & Preprocess DataFrame

def preprocess_data(df):
    df.dropna(inplace=True)
    df[['Subject1', 'Subject2', 'Subject3']] = df[['Subject1', 'Subject2', 'Subject3']].astype(int)
    df['Total'] = df[['Subject1', 'Subject2', 'Subject3']].sum(axis=1)
    df['Average'] = df['Total'] / 3
    df['Grade'] = df['Average'].apply(get_grade)
    return df


# Summary: Class Average & Topper

def get_summary(df):
    class_avg = df['Average'].mean()
    topper = df[df['Average'] == df['Average'].max()]
    return class_avg, topper


# Manual Input -> Create DataFrame

def create_dataframe_from_input(names, marks1, marks2, marks3):
    data = {
        'Name': names,
        'Subject1': marks1,
        'Subject2': marks2,
        'Subject3': marks3
    }
    df = pd.DataFrame(data)
    return preprocess_data(df)
