# local 에 MCP 서버 구축
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, root_mean_squared_error
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor 

# Create a MCP server
mcp = FastMCP("DataAnalysis")  #mcp server name

# mcp 서버에 들어갈 tool 추가
@mcp.tool()
def describe_column(csv_path: str, column: str)-> dict:
    with open(csv_path, 'r') as f:
        df = pd.read_csv(f)
        
    if column not in df.columns:
        raise ValueError(f"Column {column} not found in csv")
    return df[column].describe()

@mcp.tool()
def plot_histogram(csv_path: str, column: str, bins: int = 10)-> str:
    df = pd.read_csv(csv_path)
    if column not in df.columns:
        raise ValueError(f"Column {column} not found in csv")
    
    plt.figure(figsize=(8, 6))
    sns.histplot(
        df[column].dropna(),
        bins=bins,
        kde=True,
        stat="density",
        edgecolor="black",
        alpha=0.7,
    )
    plt.xlabel(column)
    plt.ylabel("Density")
    plt.title(f"Histogram of {column}")
    
    output_path = f"histogram_{column}.png"
    plt.savefig(output_path)
    plt.close()
    
    return output_path

@mcp.tool()
def model_train(csv_path: str, x_columns: list, y_column: str)-> dict:
    df = pd.read_csv(csv_path)
    
    for col in x_columns + [y_column]:
        if col not in df.columns:
            raise ValueError(f"Column {col} not found in csv")
        
    X = df[x_columns]
    y = df[y_column]
    
    for col in X.select_dtypes(include=["object"]).columns:
        X[col] = LabelEncoder().fit_transform(X[col])
        
    is_classification = y.dtype == "object" or len(y.unique()) <= 10
    
    if is_classification:
        y = LabelEncoder().fit_transform(y)
        model = RandomForestClassifier()
        metric_name = "accuracy"
    else:
        model = RandomForestRegressor()
        metric_name = "rmse"
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    if is_classification:
        score = accuracy_score(y_test, y_pred)
        model_type = "RandomForestClassifier"
    else:
        score = root_mean_squared_error(y_test, y_pred, squared=False)
        model_type = "RandomForestRegressor"
        
    result = {
        "model_type": model_type,
        "metric": metric_name,
        "score": score,
    }
    return result

@mcp.prompt()
def default_prompt(user_input: str)-> list[base.Message]:
    return [
        base.AIMessage(
            "You are a helpful assistant that can analyze data and train models."
            "Please clearly organize and return the tool calling and the data analysis results."
        ),
        base.UserMessage(user_input),
    ]
        
if __name__ == "__main__":
    print("MCP server is running...")
    mcp.run(transport="stdio")