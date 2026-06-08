"""
Stock Research Agent using Agno + Yahoo Finance.

Provides comprehensive stock analysis: price data, financials,
analyst ratings, and AI-powered investment summary.

Usage:
    python agent.py --ticker AAPL
    python agent.py --ticker NVDA
"""

import argparse
import os

from dotenv import load_dotenv

load_dotenv()

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


def get_stock_data(ticker: str) -> dict:
    if not HAS_YFINANCE:
        return {"ticker": ticker, "error": "yfinance not installed", "mock": True}

    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker,
        "name": info.get("longName", ticker),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
        "market_cap": info.get("marketCap", 0),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "forward_pe": info.get("forwardPE", "N/A"),
        "peg_ratio": info.get("pegRatio", "N/A"),
        "revenue_growth": info.get("revenueGrowth", "N/A"),
        "profit_margin": info.get("profitMargins", "N/A"),
        "dividend_yield": info.get("dividendYield", 0),
        "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "52w_low": info.get("fiftyTwoWeekLow", "N/A"),
        "analyst_rating": info.get("recommendationKey", "N/A"),
        "target_price": info.get("targetMeanPrice", "N/A"),
        "description": info.get("longBusinessSummary", "")[:500],
    }


def analyze_stock(data: dict) -> str:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    stock_info = "\n".join(f"{k}: {v}" for k, v in data.items() if k != "description")

    messages = [
        SystemMessage(content="You are a financial analyst. Provide a concise stock analysis covering: Investment Thesis (2-3 sentences), Key Strengths (3 bullets), Key Risks (3 bullets), Valuation Assessment, and a Verdict (Buy/Hold/Sell with brief reasoning). Keep it under 300 words."),
        HumanMessage(content=f"Analyze this stock:\n{stock_info}\n\nCompany description: {data.get('description', 'N/A')}"),
    ]

    response = llm.invoke(messages)
    return response.content


def format_number(n) -> str:
    if isinstance(n, (int, float)):
        if n >= 1e12:
            return f"${n/1e12:.2f}T"
        if n >= 1e9:
            return f"${n/1e9:.2f}B"
        if n >= 1e6:
            return f"${n/1e6:.2f}M"
        return f"${n:.2f}"
    return str(n)


def main():
    parser = argparse.ArgumentParser(description="Stock Research Agent")
    parser.add_argument("--ticker", required=True, help="Stock ticker symbol (e.g., AAPL)")
    args = parser.parse_args()

    print(f"\n📈 Researching {args.ticker}...\n")

    data = get_stock_data(args.ticker)

    print("=" * 60)
    print(f"📊 {data.get('name', args.ticker)} ({args.ticker})")
    print("=" * 60)
    print(f"Price: ${data.get('price', 'N/A')}  |  Market Cap: {format_number(data.get('market_cap', 0))}")
    print(f"Sector: {data.get('sector')}  |  Industry: {data.get('industry')}")
    print(f"P/E: {data.get('pe_ratio')}  |  Forward P/E: {data.get('forward_pe')}  |  PEG: {data.get('peg_ratio')}")
    print(f"52W Range: ${data.get('52w_low')} - ${data.get('52w_high')}")
    analyst_rating = data.get("analyst_rating") or "N/A"
    print(f"Analyst: {str(analyst_rating).upper()}  |  Target: ${data.get('target_price', 'N/A')}")

    print("\n🤖 AI Analysis:")
    print("-" * 40)
    analysis = analyze_stock(data)
    print(analysis)


if __name__ == "__main__":
    main()
