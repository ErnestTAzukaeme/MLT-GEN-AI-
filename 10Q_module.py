import json, boto3
from cik_module import SecEdgar

BUCKET   = "ernesta_lambda"
MODEL_ID = "us.anthropic.claude-sonnet-4-20250514-v1:0"
bedrock  = boto3.client("bedrock-runtime", region_name="us-east-1")

def ask_bedrock(prompt):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        "max_tokens": 400,
        "temperature": 0.0,
    }
    resp = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )
    result = json.loads(resp["body"].read())
    return result["content"][0]["text"]

def lambda_handler(event, context):
    try:
        # required inputs
        question = event.get("question")
        ticker   = event.get("ticker")
        year     = event.get("year")
        quarter  = event.get("quarter")

        if not (question and ticker and year):
            return {"statusCode": 400, "body": json.dumps("Missing required fields.")}

        # use cik_module to resolve ticker → CIK and fetch filing
        sec = SecEdgar("https://www.sec.gov/files/company_tickers.json")
        cik = sec.ticker_to_cik(ticker)
        if not cik:
            return {"statusCode": 404, "body": json.dumps("Company not found.")}

        if quarter:
            filing_url = sec.quarterly_filing(cik, year, quarter)
        else:
            filing_url = sec.annual_filing(cik, year)

        if not filing_url:
            return {"statusCode": 404, "body": json.dumps("Filing not found.")}

        # fetch filing text
        import requests
        headers = {"User-Agent": "ErnestaLambda/1.0 (ernesta@example.com)"}
        filing_text = requests.get(filing_url, headers=headers).text

        # build prompt
        prompt = f"""
You are a financial analyst. Use the SEC filing below for {ticker} in {year} to answer the question.

--- SEC Filing Start ---
{filing_text[:15000]}
--- SEC Filing End ---

Question: {question}
"""

        # call Claude
        answer = ask_bedrock(prompt)

        return {
            "statusCode": 200,
            "body": json.dumps({"question": question, "answer": answer, "filing_url": filing_url}),
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}
