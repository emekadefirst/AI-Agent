from src.tools.flight.amadeus.agent_tool import AgentFlightTool
from src.tools.hotel.amadeus.agent_tool import AgentHotelTool

tools = [
    AgentFlightTool.search_flights_tool(),
    AgentFlightTool.get_flight_price_tool(),
    AgentFlightTool.create_order_tool(),
    AgentHotelTool.fetch_tool(),
    AgentHotelTool.rating_tool(),
    AgentHotelTool.offer_tool(),
    AgentHotelTool.book_tool()
]
