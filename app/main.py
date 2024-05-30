import pandas as pd
import uuid
import json
import openai
import logging
from app.config import Config
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from app.utils.data_processing import preprocess_data, preprocess_single_transaction
from app.utils.prompts import generate_financial_analysis_prompt_zero_shot, generate_financial_analysis_prompt_few_shot, generate_financial_analysis_prompt_cot
from app.services.financial_analyzer import compare_last_three_analyses, get_historical_average_spending, get_current_week_spending, get_historical_average_earnings, get_current_week_earnings, get_monthly_totals, get_overall_totals, get_historical_monthly_totals
from app.services.transaction_service import save_transaction,  get_total_transaction_count, get_all_transactions, save_analysis, get_last_n_analyses
from app.schemas.models import Transaction, TransactionsAnalysisPayload
from app.services.interpretation import save_interpretation

app = FastAPI()

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/")
async def health_check():
    return {"status": "All good!"}

@app.post("/upload_single_transaction/", response_model=dict)
async def upload_single_transaction(transaction: Transaction):
    try:
        df = preprocess_single_transaction(pd.DataFrame([transaction.dict()]))
        unique_id = transaction.uuid or str(uuid.uuid4())
        save_transaction(df, unique_id)
        
        # Check if there are at least 30 transactions in the database
        total_transaction_count = get_total_transaction_count()
        if total_transaction_count < 30:
            return {
                "status": "success",
                "message": "Not enough data to give analysis, but the data is saved to the database.",
                "uuid": unique_id
            }

        # Retrieve all transactions to calculate statistics
        all_transactions = get_all_transactions()
        
        # Get the current transaction's year, month, and week
        year = df.iloc[0]['year']
        month = df.iloc[0]['month']
        week_of_month = df.iloc[0]['week_of_month']
        
        # Calculate historical average spending and earnings for the same week
        historical_avg_spending = get_historical_average_spending(all_transactions, year, month, week_of_month)
        historical_avg_earnings = get_historical_average_earnings(all_transactions, year, month, week_of_month)
        
        # Calculate current week's total spending and earnings
        current_week_spending = get_current_week_spending(all_transactions, year, month, week_of_month)
        current_week_earnings = get_current_week_earnings(all_transactions, year, month, week_of_month)

        # Calculate monthly totals
        current_month_spending, current_month_earnings = get_monthly_totals(all_transactions, year, month)
        historical_month_spending, historical_month_earnings = get_historical_monthly_totals(all_transactions, year, month)
        
        # Calculate overall totals
        overall_spending, overall_earnings = get_overall_totals(all_transactions)
        
        return {
            "status": "success",
            "uuid": unique_id,
            "historical_average_spending": historical_avg_spending,
            "current_week_spending": current_week_spending,
            "spending_comparison": current_week_spending - historical_avg_spending,
            "historical_average_earnings": historical_avg_earnings,
            "current_week_earnings": current_week_earnings,
            "earnings_comparison": current_week_earnings - historical_avg_earnings,
            "current_month_spending": current_month_spending,
            "current_month_earnings": current_month_earnings,
            "historical_month_spending": historical_month_spending,
            "historical_month_earnings": historical_month_earnings,
            "overall_spending": overall_spending,
            "overall_earnings": overall_earnings
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upload_transactions/")
async def upload_transactions(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        df = preprocess_data(df)
        unique_id = str(uuid.uuid4())  # Generate a UUID
        save_transaction(df, unique_id)
        
        # Check if there are at least 30 transactions in the database
        total_transaction_count = get_total_transaction_count()
        if total_transaction_count < 30:
            return {
                "status": "success",
                "message": "Not enough data to give analysis, but the data is saved to the database.",
                "uuid": unique_id
            }
        
        # Retrieve all transactions to calculate statistics
        all_transactions = get_all_transactions()
        
        # Process each transaction separately
        comparisons = []
        for _, row in df.iterrows():
            year = row['year']
            month = row['month']
            week_of_month = row['week_of_month']
            
            # Calculate historical average spending and earnings for the same week
            historical_avg_spending = get_historical_average_spending(all_transactions, year, month, week_of_month)
            historical_avg_earnings = get_historical_average_earnings(all_transactions, year, month, week_of_month)
            
            # Calculate current week's total spending and earnings
            current_week_spending = get_current_week_spending(all_transactions, year, month, week_of_month)
            current_week_earnings = get_current_week_earnings(all_transactions, year, month, week_of_month)

            # Calculate monthly totals
            current_month_spending, current_month_earnings = get_monthly_totals(all_transactions, year, month)
            historical_month_spending, historical_month_earnings = get_historical_monthly_totals(all_transactions, year, month)
            
            # Calculate overall totals
            overall_spending, overall_earnings = get_overall_totals(all_transactions)
            
            # Build the comparison object
            comparison = {
                "transaction_id": row['transaction_id'],
                "historical_average_spending": historical_avg_spending,
                "current_week_spending": current_week_spending,
                "spending_comparison": current_week_spending - historical_avg_spending,
                "historical_average_earnings": historical_avg_earnings,
                "current_week_earnings": current_week_earnings,
                "earnings_comparison": current_week_earnings - historical_avg_earnings,
                "current_month_spending": current_month_spending,
                "current_month_earnings": current_month_earnings,
                "historical_month_spending": historical_month_spending,
                "historical_month_earnings": historical_month_earnings,
                "overall_spending": overall_spending,
                "overall_earnings": overall_earnings
            }
            save_analysis(comparison)
            # Append comparison object to list
            comparisons.append(comparison)
        
        return {"status": "success", "uuid": unique_id, "comparisons": comparisons}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/compare_last_three_analyses/")
async def compare_last_three_analyses_endpoint():
    try:
        past_analyses = get_last_n_analyses(3)
        if len(past_analyses) < 3:
            raise HTTPException(status_code=404, detail="Not enough past analyses found for comparison")
        
        comparison_results = compare_last_three_analyses(past_analyses)
        return {"status": "success", "comparison_results": comparison_results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# OpenAI API key
openai.api_key = Config.OPENAI_API_KEY

@app.post("/generate-narrative/")
async def generate_narrative(data: TransactionsAnalysisPayload):
    transactions = [transaction.dict() for transaction in data.transactions]
    analysis = data.analysis.dict()
    
    # OpenAI API key
    openai.api_key = Config.OPENAI_API_KEY
    model = Config.OPEN_AI_MODEL
    versions = ['zero_shot', 'few_shot', 'cot']
    narratives = {version: "" for version in versions}

    async def response_stream():
        yield "event:start_narrative_stream\ndata: stream started\n\n"

        for version in versions:
            try:
                if version == 'zero_shot':
                    prompt = generate_financial_analysis_prompt_zero_shot({"transactions": transactions, "analysis": analysis})
                elif version == 'few_shot':
                    prompt = generate_financial_analysis_prompt_few_shot({"transactions": transactions, "analysis": analysis})
                elif version == 'cot':
                    prompt = generate_financial_analysis_prompt_cot({"transactions": transactions, "analysis": analysis})
                
                key_name = f"narrative_{version}"
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    stream=True
                )

                narrative = ""
                for event in response:
                    if 'content' in event['choices'][0]['delta']:
                        response_message = event['choices'][0]['delta']['content']
                        narrative += response_message
                        json_data = json.dumps({key_name: response_message})
                        yield f"event:narrative_{version}\ndata: {json_data}\n\n"

                # Save the complete narrative for this version
                narratives[version] = narrative

            except Exception as e:
                error_message = f"An error occurred for version {version}: {str(e)}"
                yield f"event:error\ndata: {json.dumps({'error': error_message})}\n\n"
                continue  # Continue to next version

            yield f"event:end_narrative_{version}\ndata: stream ended\n\n"

        # Save all narratives to the database
        save_interpretation(transactions[0]['transaction_id'], narratives)

        yield "event:end_narrative_stream\ndata: stream ended\n\n"

    return StreamingResponse(response_stream(), media_type="text/event-stream")
