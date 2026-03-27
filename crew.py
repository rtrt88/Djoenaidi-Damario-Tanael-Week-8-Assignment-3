import os

from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv


# Load environment variables from .env and validate API key.
def load_environment() -> None:
    load_dotenv()
    # if not os.getenv("OPENAI_API_KEY"):
    #     raise ValueError("OPENAI_API_KEY not found. Add it to your .env file.")


# Create the three assignment-required agents.
def create_agents() -> tuple[Agent, Agent, Agent]:
    market_researcher = Agent(
        role="Consumer Insights Research Lead (Campus F&B)",
        goal=(
            "Deliver a customer evidence brief with exactly 5 ranked demand drivers, "
            "3 adoption barriers, and a demand-confidence rating that is justified by "
            "observable student behavior patterns."
        ),
        backstory=(
            "You spent 8 years running student-segment research for independent coffee shops "
            "located near universities in Hong Kong and Singapore. In your past role, "
            "you saw multiple cafes fail after launching discounts without validating "
            "real student willingness-to-pay. Because of that, you always separate "
            "stated preference from likely purchase behavior, prioritize evidence quality, "
            "and clearly flag assumptions when data is weak."
        ),
        verbose=True,
    )

    business_analyst = Agent(
        role="Commercial Strategy and Unit Economics Analyst",
        goal=(
            "Produce one decision-ready recommendation by comparing low/base/high adoption "
            "scenarios, including revenue impact, margin pressure, and operational risk, "
            "with transparent assumptions that can be checked by the owner."
        ),
        backstory=(
            "You are a former finance manager for a regional cafe chain who later advised "
            "small F&B owners on pricing and subscription design. You witnessed that small "
            "shops often overestimate sign-up rates and underestimate redemption costs. "
            "As a result, you are disciplined about downside scenarios, explicit assumptions, "
            "and recommendation logic that balances growth ambition with cash-flow safety."
        ),
        verbose=True,
    )

    report_writer = Agent(
        role="Executive Business Report and Implementation Specialist",
        goal=(
            "Convert prior analysis into a decision memo the owner can execute immediately, "
            "including a clear recommendation, a 30-day action roadmap, and 4 KPIs with "
            "defined target thresholds and review cadence."
        ),
        backstory=(
            "You worked as an operations chief of staff for two small hospitality businesses "
            "where plans failed when reports were too abstract. That experience makes you "
            "write in an owner-first style: plain language, concrete next steps, timeline-based "
            "execution, and measurable outcomes. You avoid vague recommendations and always "
            "translate strategy into accountable actions."
        ),
        verbose=True,
    )

    return market_researcher, business_analyst, report_writer


# Create three tasks with required dependency flow through context.
def create_tasks(
    market_researcher: Agent,
    business_analyst: Agent,
    report_writer: Agent,
) -> tuple[Task, Task, Task]:
    task_1 = Task(
        description=(
            "Role focus: Consumer insights research.\n"
            "Analyze the topic below and identify how students are likely to respond to a "
            "coffee subscription plan.\n\n"
            "Topic: {topic}\n\n"
            "Your output must:\n"
            "1) list the strongest student demand drivers,\n"
            "2) identify adoption barriers and objections,\n"
            "3) explain likely usage behavior (frequency/timing/value perception), and\n"
            "4) separate evidence-based points from assumptions,\n"
            "5) end with a one-line insight on whether demand appears strong, moderate, or weak."
        ),
        expected_output=(
            "A market insights brief with the exact sections below:\n"
            "- Student Demand Drivers (exactly 5, ranked 1-5)\n"
            "- Adoption Barriers (exactly 3, ranked high/medium/low impact)\n"
            "- Likely Student Usage Pattern (3 bullet points)\n"
            "- Evidence vs Assumptions (2-column list)\n"
            "- Demand Confidence Rating (High/Medium/Low) with 3 reasons\n"
            "- One-Line Insight (single sentence decision signal)"
        ),
        agent=market_researcher,
    )

    task_2 = Task(
        description=(
            "Role focus: commercial and unit economics analysis.\n"
            "Use Task 1 as required context and evaluate whether the subscription plan is "
            "commercially viable for a small coffee shop.\n\n"
            "You must:\n"
            "1) build low/base/high adoption scenarios,\n"
            "2) state assumptions clearly,\n"
            "3) compare upside, downside, and operational risk for each scenario, and\n"
            "4) explicitly reference at least 3 findings from Task 1,\n"
            "5) end with one decision recommendation (launch now / pilot first / do not launch)."
        ),
        expected_output=(
            "A business analysis memo with the exact sections below:\n"
            "- Scenario Table (Low/Base/High adoption)\n"
            "- Key Assumptions (at least 5 bullet points)\n"
            "- Financial Implication Summary (revenue and margin direction per scenario)\n"
            "- Risk Register (top 4 risks with mitigation ideas)\n"
            "- Decision Criteria Check (profitability, feasibility, risk)\n"
            "- Final Recommendation (one option only) with a clear rationale"
        ),
        agent=business_analyst,
        context=[task_1],
    )

    task_3 = Task(
        description=(
            "Role focus: executive reporting and implementation planning.\n"
            "Use both Task 1 and Task 2 as required context to produce a final owner-ready "
            "business report.\n\n"
            "The report must synthesize prior analysis into a practical decision and execution "
            "plan for a small team. If the recommendation is to pilot or launch, include a 30-day "
            "implementation roadmap. If the recommendation is not to launch, include a 30-day "
            "alternative growth plan for student sales.\n\n"
            "Make the report decision-ready for the owner with clear sections and no vague language."
        ),
        expected_output=(
            "A final business report with the exact sections below:\n"
            "- Executive Summary (5-7 sentences)\n"
            "- Final Decision and Why (linked to Task 1 + Task 2 findings)\n"
            "- 30-Day Plan by Week (Week 1-4 milestones)\n"
            "- Owner Action Checklist (8-10 concrete actions)\n"
            "- KPI Dashboard (exactly 4 KPIs, each with definition and target)\n"
            "- Trigger Points (what results should cause plan adjustment)\n"
            "- Final Recommendation Statement (exactly one of: launch now / pilot first / do not launch)"
        ),
        agent=report_writer,
        context=[task_1, task_2],
    )

    return task_1, task_2, task_3


# Build crew with sequential process as required.
def build_crew() -> Crew:
    market_researcher, business_analyst, report_writer = create_agents()
    task_1, task_2, task_3 = create_tasks(
        market_researcher, business_analyst, report_writer
    )

    return Crew(
        agents=[market_researcher, business_analyst, report_writer],
        tasks=[task_1, task_2, task_3],
        process=Process.sequential,
        verbose=True,
    )


# Run the crew with assignment-required inputs and print final result.
def main() -> None:
    load_environment()
    crew = build_crew()

    result = crew.kickoff(
        inputs={
            "topic": "Should a small coffee shop launch a student subscription plan?"
        }
    )
    print(result)


if __name__ == "__main__":
    main()
