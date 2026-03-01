from crewai.tools import tool
from typing import Optional

@tool("Kayak tool")
def kayak_search(
    departure: str,
    destination: str,
    date: str,
    return_date: Optional[str] = None,
    adults: int = 1,
    infants: int = 0,
) -> str:
    """
    Generates a Kayak URL for flights between departure and destination on the specified date.

    :param departure: The IATA code for the departure airport (e.g., 'ADL' for Adelaide)
    :param destination: The IATA code for the destination airport (e.g., 'DPS' for Bali)
    :param date: The date of the flight in the format 'YYYY-MM-DD'
    :param return_date: Only for two-way tickets. The date of return flight in the format 'YYYY-MM-DD'
    :param adults: Number of adult passengers (default 1)
    :param infants: Number of infant passengers travelling on lap (default 0)
    :return: The Kayak URL for the flight search
    """
    print(f"Generating Kayak URL for {departure} to {destination} on {date} ({adults} adults, {infants} infants)")
    pax = f"{adults}adults"
    if infants:
        pax += f"/{infants}infant_on_lap"
    URL = f"https://www.kayak.com/flights/{departure}-{destination}/{date}"
    if return_date:
        URL += f"/{return_date}"
    URL += f"/{pax}?currency=AUD"
    return URL

# Export the decorated function
kayak = kayak_search