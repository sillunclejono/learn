import sys
import datetime
from crewai import Crew, Process, Task, Agent
from browserbase import browserbase
from kayak import kayak
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

flights_agent = Agent(
    role="Flights",
    goal="Search flights",
    backstory="I am an agent that can search for flights.",
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
Here are our top 5 international flights from Adelaide (ADL) this week for 2 adults + 1 infant:
1. Singapore Airlines: ADL → SIN, Departure: 10:30, Arrival: 16:45, Duration: 8 hours 15 minutes, Price: AUD 950 per adult, Details: https://www.kayak.com/flights/ADL-SIN/2026-03-05/2adults/1infant_on_lap?currency=AUD
"""

search_task = Task(
    description=(
        "Search flights according to criteria {request}. Current year: {current_year}"
    ),
    expected_output=output_search_example,
    agent=flights_agent,
)

output_providers_example = """
Here are our top 5 international picks from Adelaide (ADL) this week for 2 adults + 1 infant:
1. Singapore Airlines (ADL → SIN):
    - Departure: 10:30
    - Arrival: 16:45
    - Duration: 8 hours 15 minutes
    - Price: AUD 950 per adult (infant fee may apply)
    - Booking: [Singapore Airlines](https://www.kayak.com/flights/ADL-SIN/2026-03-05/2adults/1infant_on_lap?currency=AUD)
    ...
"""

search_booking_providers_task = Task(
    description="Load every flight individually and find available booking providers",
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
            "request": (
                "International flights from Adelaide (ADL) this week "
                "(between 2026-03-01 and 2026-03-07) for 2 adults and 1 infant (on lap). "
                "Find the best available international routes and prices. "
                "Use AUD currency."
            ),
            "current_year": datetime.date.today().year,
        }
    )

    print(result)