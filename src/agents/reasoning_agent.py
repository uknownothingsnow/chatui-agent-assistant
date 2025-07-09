from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

def create_reasoning_agent(model):
    return Agent(
        model=model,
        tools=[
            ReasoningTools(add_instructions=True),
            YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True),
        ],
        instructions="Use tables to display data.",
        show_tool_calls=True,
        markdown=True,
    )