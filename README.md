# MLT CP 27 Summer Project

This repository contains my work for **Build Your Own Full Stack LLM Service on AWS**, part of Gerald Spivey’s **MLT Career Prep (CP 27)** program. The project integrates **AWS Lambda**, **Bedrock (Claude Sonnet)**, and **SEC EDGAR filings** to answer financial questions from company reports.

## Project Files

| File            | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `cik_module.py` | Utility for looking up **company CIKs** from SEC’s `company_tickers.json`.  |
| `10Q_module.py` | AWS **Lambda function** that:<br>– Accepts a question, ticker, year, and quarter<br>– Retrieves the company’s 10-K or 10-Q filing<br>– Builds a context prompt<br>– Calls **Claude Sonnet** on AWS Bedrock to generate an answer. |

---

*Summer project for Gerald Spivey’s MLT CP 27 program*  
*Implemented by Ernest Azukaeme*  

