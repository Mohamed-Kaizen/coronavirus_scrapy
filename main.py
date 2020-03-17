from fastapi import FastAPI
from requests_html import HTMLSession
from starlette.middleware.cors import CORSMiddleware

session = HTMLSession()

app = FastAPI(
    title="corona virus real time data",
    description="",
    version="0.1.0",
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


def get_data():

    respond = session.get("https://www.worldometers.info/coronavirus/")

    tbody = respond.html.find("tbody", first=True)

    trs = tbody.find("tr")

    data = {}

    for tr in trs:
        if "Ethiopia" in tr.text:
            tds = tr.find("td")
            country = 0 if tds[0].text == "" else tds[0].text
            total_case = 0 if tds[1].text == "" else tds[1].text
            new_case = 0 if tds[2].text == "" else tds[2].text
            total_death = 0 if tds[3].text == "" else tds[3].text
            new_death = 0 if tds[4].text == "" else tds[4].text
            total_recovered = 0 if tds[5].text == "" else tds[5].text
            active_case = 0 if tds[6].text == "" else tds[6].text
            serious_critical = 0 if tds[7].text == "" else tds[7].text
            total_cases_1_m_pop = 0 if tds[8].text == "" else tds[8].text
            data.update(
                {
                    "country": country,
                    "total_case": total_case,
                    "new_case": new_case,
                    "total_death": total_death,
                    "new_death": new_death,
                    "total_recovered": total_recovered,
                    "active_case": active_case,
                    "serious_critical": serious_critical,
                    "total_cases_1_M_pop": total_cases_1_m_pop,
                }
            )

    return data


@app.get("/")
async def get_ethiopia_data():

    return get_data()
