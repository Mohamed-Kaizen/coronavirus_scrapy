from fastapi import FastAPI, status
from pydantic import BaseModel, ValidationError
from requests_html import HTMLSession
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

session = HTMLSession()

app = FastAPI(
    title="corona virus real time data",
    description="",
    version="0.3.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_data(*, country: str):

    respond = session.get("https://www.worldometers.info/coronavirus/")

    tbody = respond.html.find("tbody", first=True)

    trs = tbody.find("tr")

    data = {}

    for tr in trs:
        if f"{country}" in tr.text.lower():
            tds = tr.find("td")
            country = 0 if tds[1].text == "" else tds[1].text
            total_case = 0 if tds[2].text == "" else tds[2].text
            new_case = 0 if tds[3].text == "" else tds[3].text
            total_death = 0 if tds[4].text == "" else tds[4].text
            new_death = 0 if tds[5].text == "" else tds[5].text
            total_recovered = 0 if tds[6].text == "" else tds[6].text
            new_recovered = 0 if tds[7].text == "" else tds[7].text
            active_case = 0 if tds[8].text == "" else tds[8].text
            serious_critical = 0 if tds[9].text == "" else tds[9].text
            total_cases_1_m_pop = 0 if tds[10].text == "" else tds[10].text
            total_deaths_1_m_pop = 0 if tds[11].text == "" else tds[11].text
            total_test = 0 if tds[12].text == "" else tds[12].text
            total_test_1_m_pop = 0 if tds[13].text == "" else tds[13].text
            population = 0 if tds[14].text == "" else tds[14].text
            continent = 0 if tds[15].text == "" else tds[15].text
            one_case_every_x_ppl = 0 if tds[16].text == "" else tds[16].text
            one_death_every_x_ppl = 0 if tds[17].text == "" else tds[17].text
            one_test_every_x_ppl = 0 if tds[18].text == "" else tds[18].text
            data.update(
                {
                    "country": country,
                    "total_case": total_case,
                    "new_case": new_case,
                    "total_death": total_death,
                    "new_death": new_death,
                    "total_recovered": total_recovered,
                    "new_recovered":new_recovered,
                    "active_case": active_case,
                    "serious_critical": serious_critical,
                    "total_cases_1_M_pop": total_cases_1_m_pop,
                    "total_deaths_1_m_pop": total_deaths_1_m_pop,
                    "total_test": total_test,
                    "total_test_1_m_pop": total_test_1_m_pop,
                    "population": population,
                    "continent": continent,
                    "one_case_every_x_ppl": one_case_every_x_ppl,
                    "one_death_every_x_ppl": one_death_every_x_ppl,
                    "one_test_every_x_ppl": one_test_every_x_ppl,
                }
            )

    return data


class CoronaVirusData(BaseModel):
    country: str
    total_case: str
    new_case: str
    total_death: str
    new_death: str
    total_recovered: str
    new_recovered: str
    active_case: str
    serious_critical: str
    total_cases_1_M_pop: str
    total_deaths_1_m_pop: str
    total_test: str
    total_test_1_m_pop: str
    population: str
    continent: str
    one_case_every_x_ppl: str
    one_death_every_x_ppl: str
    one_test_every_x_ppl: str


@app.get("/", response_model=CoronaVirusData)
async def get_country_corona_virus_data(country: str = "Ethiopia"):
    """Getting corona virus data from any country.

    Args:
        country: Tell what country data to get. Default to Ethiopia.

    Example:

        https://example.com/?country=china
    """
    return get_data(country=country.lower())


@app.get("/total/")
async def get_total_corona_virus_cases():
    """Getting total corona virus cases."""
    respond = session.get("https://www.worldometers.info/coronavirus/")

    cases, deaths, recovered = respond.html.find(".maincounter-number")

    total_currently_infected_patients = respond.html.find(
        ".number-table-main", first=True
    ).text

    total_cases_which_had_an_outcome = respond.html.find(".number-table-main")[1].text

    total_in_mild_condition = respond.html.find(".number-table", first=True).text

    total_serious_or_critical = respond.html.find(".number-table")[1].text

    totals_cases = cases.find("span", first=True).text

    totals_deaths = deaths.find("span", first=True).text

    totals_recovered = recovered.find("span", first=True).text

    return {
        "totals_cases": totals_cases,
        "totals_deaths": totals_deaths,
        "totals_recovered": totals_recovered,
        "total_currently_infected_patients": total_currently_infected_patients,
        "total_cases_which_had_an_outcome": total_cases_which_had_an_outcome,
        "total_in_mild_condition": total_in_mild_condition,
        "total_serious_or_critical": total_serious_or_critical,
    }


async def http400_error_handler(_, exc):
    return JSONResponse(
        {"detail": "Country doesn't exist"}, status_code=status.HTTP_400_BAD_REQUEST
    )


app.add_exception_handler(ValidationError, http400_error_handler)
