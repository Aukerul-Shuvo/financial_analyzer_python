import json

def generate_financial_analysis_prompt_zero_shot(data):
    prompt = f"""
    Using the financial transactions and analysis till that transaction, provided in the JSON data below, write a comprehensive narrative that highlights changes in spending behavior with respect to earning changes over the course of a month.

    Start with an overview of the user's spending and earning patterns. Then, detail specific behavior changes observed at different points in the month. Conclude with a comparison between past and current analyses.

    Ensure each observation is supported by data from the JSON and provide a clear, coherent narrative.

    Here is the data:
    {json.dumps(data, indent=4)}
    """
    return prompt

def generate_financial_analysis_prompt_few_shot(data):
    prompt = f"""
    Below are examples of financial analysis narratives based on user transactions and analysis data. Use these examples to write a narrative for the given JSON data.

    Example 1:
    "In January 2023, the user showed a high spending pattern during the first week of the month, primarily on utility bills and rent payments. Towards the end of the month, the spending significantly reduced as the user prepared for the upcoming month. During busy work hours, there was an increase in transactions related to food delivery services."

    Example 2:
    "In February 2023, the user's spending behavior indicated a spike in grocery and household item purchases mid-month. There was a gradual decrease in non-essential purchases towards the end of the month. Food delivery service usage was higher during lunch and dinner times on weekdays."

    Now, write a similar narrative based on the following data:
    {json.dumps(data, indent=4)}
    """
    return prompt

def generate_financial_analysis_prompt_cot(data):
    prompt = f"""
    Using the financial transactions and analysis provided, generate a narrative by following a chain of thought process. Break down the analysis into logical steps to explain changes in spending behavior with respect to earning changes over the month.

    Step 1: Overview of spending and earning patterns.
    "The data from the given period shows that the user typically spends a large portion of their income at the beginning of the month due to fixed expenses like rent and utilities."

    Step 2: Specific behavior changes at different times of the month.
    "As the month progresses, there is a noticeable reduction in spending, especially after the 25th day. This suggests a cautious approach towards the end of the month."

    Step 3: Impact of daily routines on spending.
    "During weekdays, the user relies heavily on food delivery services during lunch and dinner times, indicating busy work hours. This pattern is consistent throughout the data."

    Step 4: Comparative analysis between past and current data.
    "Comparing the current month's data with the previous months, there is an increase in discretionary spending on weekends, which highlights a change in leisure activities."

    Now, using this chain of thought, write a detailed narrative based on the following data:
    {json.dumps(data, indent=4)}
    """
    return prompt
