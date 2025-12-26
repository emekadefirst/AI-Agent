from src.tools.flight.amadeus import auth, core, router
import asyncio


token = asyncio.run(auth.AmadeusAuth.get_token())
print(token)


# async def test_unified():
#     # Flight offers
#     offers = await amadeus_flight.AmadeusFlightTool.search_flights(
#         origin="PAR",
#         destination="ICN",
#         departure_date="2026-01-07",
#         return_date="2026-01-21",
#         adults=2
#     )
#     print("Flight Offers:", len(offers))
#     print("data:", offers)
# asyncio.run(test_unified())