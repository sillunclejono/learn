import sys
import datetime
from crewai import Crew, Process, Task, Agent
from browserbase import browserbase
from kayak import kayak
from dotenv import load_dotenv
from airline_search_optimizer import FareOption, optimize_fare_options

load_dotenv()  # take environment variables from .env.


def build_sample_fare_optimization_report() -> str:
    sample_fares = [
        FareOption(
            airline="Delta",
            booking_class="Y",
            base_fare=410,
            taxes=64.8,
            fare_type="public",
            refundable=False,
            baggage_included=True,
        ),
        FareOption(
            airline="United",
            booking_class="J",
            base_fare=520,
            taxes=70.5,
            contract_code="CORP-UNITED-042",
            fare_type="private_net",
            refundable=True,
            baggage_included=True,
        ),
        FareOption(
            airline="American",
            booking_class="D",
            base_fare=495,
            taxes=69.2,
            contract_code="TA-7781",
            fare_type="net",
            refundable=True,
            baggage_included=False,
        ),
    ]

    ranked = optimize_fare_options(sample_fares)
    lines = ["Ranked fare options (booking class + contracts + private/net fares):"]
    for idx, fare in enumerate(ranked, start=1):
        lines.append(
            f"{idx}. {fare['airline']} | class {fare['booking_class']} | "
            f"contract {fare['contract_code']} | type {fare['fare_type']} | "
            f"private/net={fare['is_private_net_fare']} | total ${fare['total_price']} | "
            f"score {fare['score']}"
        )
    return "\n".join(lines)


flights_agent = Agent(
    role="Flights",
    goal="Search and optimize flights including booking classes, contracts, and private net fares",
    backstory="I am an airline pricing analyst agent that can search flights, compare booking classes, inspect contract fares, and prioritize private net fares.",
    tools=[kayak, browserbase],
    allow_delegation=False,
)

summarize_agent = Agent(
    role="Summarize",
    goal="Summarize content",
    backstory="I am an agent that can summarize text.",
    allow_delegation=False,
)

output_search_example = """
Here are our top 5 flights from San Francisco to New York on 21st September 2024:
1. Delta Airlines: Departure: 21:35, Arrival: 03:50, Duration: 6 hours 15 minutes, Price: $125, Details: https://www.kayak.com/flights/sfo/jfk/2024-09-21/12:45/13:55/2:10/delta/airlines/economy/1
"""

search_task = Task(
    description=(
        "Search flights according to criteria {request}. Current year: {current_year}. "
        "Include booking classes for each option and identify potential contract fares and private net fares when visible."
    ),
    expected_output=output_search_example,
    agent=flights_agent,
)

output_providers_example = """
Here are our top 5 picks from San Francisco to New York on 21st September 2024:
1. Delta Airlines:
    - Departure: 21:35
    - Arrival: 03:50
    - Duration: 6 hours 15 minutes
    - Price: $125
    - Booking: [Delta Airlines](https://www.kayak.com/flights/sfo/jfk/2024-09-21/12:45/13:55/2:10/delta/airlines/economy/1)
    ...
"""

search_booking_providers_task = Task(
    description=(
        "Load every flight individually and find available booking providers. "
        "Capture booking class, contract identifiers (if present), and whether a fare appears private/net."
    ),
    expected_output=output_providers_example,
    agent=flights_agent,
)

crew = Crew(
    agents=[flights_agent, summarize_agent],
    tasks=[search_task, search_booking_providers_task],
    # let's cap the number of OpenAI requests as the Agents
    #   may have to do multiple costly calls with large context
    max_rpm=100,
    # let's also set verbose=True and planning=True
    #   to see the progress of the Agents
    #   and the Task execution. Remove these lines
    #   if you want to run the script without
    #   seeing the progress (like in production).
    verbose=True,
    planning=True,
)

if __name__ == "__main__":
    result = crew.kickoff(
        inputs={
            "request": "flights from SF to New York on November 5th",
            "current_year": datetime.date.today().year,
        }
    )

    print(result)
    print("\n" + build_sample_fare_optimization_report())