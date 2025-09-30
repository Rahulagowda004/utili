import pandas as pd

def drop_col(df):
    required_columns = [
        "Parent summary",
        "Summary",
        "Assignee",
        "Custom field (Start date)",
        "Due date",
        "Σ Original Estimate",
        "Time Spent",
        "Status"
    ]
    df = df[required_columns]
    return df

def rename_col(df):
    rename_dict = {
        "Parent summary": "Module / Category",
        "Summary": "Task Details",
        "Assignee": "Assigned To",
        "Custom field (Start date)": "Start Date",
        "Due date": "Due Date",
        "Σ Original Estimate": "Planned (Hrs)",
        "Time Spent": "Actual (Hrs)",
        "Status": "Status"
    }
    df = df.rename(columns=rename_dict)
    df["End Date"] = df["Due Date"]
    df["Risk / Comments / Comp Off"] = ""
    return df

def date_format(df):
    df["Start Date"] = pd.to_datetime(df["Start Date"], dayfirst=True, format="mixed").dt.strftime("%#d/%#m/%Y")
    df["Due Date"] = pd.to_datetime(df["Due Date"], dayfirst=True, format="mixed").dt.strftime("%#d/%#m/%Y")
    df["End Date"] = df["Due Date"]
    return df

def time_format(df):
    df["Planned (Hrs)"] = (df["Planned (Hrs)"] / 3600).round(2)
    df["Actual (Hrs)"] = (df["Actual (Hrs)"] / 3600).round(2)
    return df

def pipeline(df):
    df = drop_col(df)
    df = rename_col(df)
    df = date_format(df)
    df = time_format(df)
    return df

# LHS                  RHS

# Module / Category = Parent summary
# Task Details = Summary
# Assigned To = Assignee
# Start Date = Custom field (Start date)
# Due Date = Due date
# Planned (Hrs) = Σ Original Estimate
# Actual (Hrs) = Time Spent
# Status = Status
# End Date = Due date
# Risk / Comments / Comp Off = .