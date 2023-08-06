import datetime

from .types import (
    VaccinationByDayRow,
    VaccinationByAgeRow,
    VaccineSupplyUsage,
    VaccinationByRegionRow,
    VaccinationByManufacturerRow,
    VaccinationDose,
    VaccinationMunShare,
    VaccinationAgeGroupByRegionOnDayDose,
    VaccinationAgeGroupByRegionOnDay,
)


def parse_date(raw):
    return datetime.datetime.utcfromtimestamp(float(raw) / 1000.0)


def _parse_vaccinations_timestamp(data):
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        # ? raise exception or return error obj
        return error
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    return resp[0]["M0"]


def _parse_vaccinations_by_day(data) -> "list[VaccinationByDayRow]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        date = parse_date(element["G0"])
        people_vaccinated = element["X"][0]["M0"]
        people_fully_vaccinated = element["X"][1]["M0"] if len(element["X"]) > 1 else 0

        parsed_data.append(
            VaccinationByDayRow(
                date=date,
                first_dose=people_vaccinated,
                second_dose=people_fully_vaccinated,
            )
        )

    return parsed_data


def _parse_vaccinations_by_age(data) -> "list[VaccinationByAgeRow]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        age_group = str(element["G0"])
        count_first = int(element["X"][0]["C"][1])
        count_second = int(element["X"][1]["C"][1])
        share_first = float(element["X"][0]["C"][0]) / 100.0
        share_second = float(element["X"][1]["C"][0]) / 100.0

        parsed_data.append(
            VaccinationByAgeRow(
                age_group=age_group,
                count_first=count_first,
                count_second=count_second,
                share_first=share_first,
                share_second=share_second,
            )
        )

    return parsed_data


def _parse_vaccines_supplied_and_used(data) -> "list[VaccineSupplyUsage]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:

        date = parse_date(element["C"][0])

        if "Ø" in element:
            supplied = int(element["C"][1]) if len(element["C"]) > 1 else 0
            used = 0
        else:
            used = (
                int(element["C"][1]) if len(element["C"]) > 1 else parsed_data[-1].used
            )
            supplied = (
                int(element["C"][2])
                if len(element["C"]) > 2
                else parsed_data[-1].supplied
            )

        row = VaccineSupplyUsage(
            date=date,
            supplied=supplied,
            used=used,
        )
        parsed_data.append(row)

    return parsed_data


def _parse_vaccinations_by_region(data) -> "list[VaccinationByRegionRow]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        region = str(element["G0"])
        count_first = int(element["X"][0]["C"][1])
        count_second = int(element["X"][1]["C"][1])
        share_first = float(element["X"][0]["C"][0]) / 100.0
        share_second = float(element["X"][1]["C"][0]) / 100.0

        parsed_data.append(
            VaccinationByRegionRow(
                region=region,
                count_first=count_first,
                count_second=count_second,
                share_first=share_first,
                share_second=share_second,
            )
        )

    return parsed_data


def _parse_vaccines_supplied_by_manufacturer(
    data,
) -> "list[VaccinationByManufacturerRow]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][1]["DM1"]
    manufacturers = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["ValueDicts"][
        "D0"
    ]
    parsed_data = []

    if len(manufacturers) > 4:
        print(manufacturers)
        raise Exception("New manufacturer!")

    def get_manufacturer(num):
        manu_keys = ["pfizer", "moderna", "az", "janssen"]
        if num > 3 or num == None:
            print(num)
            raise Exception("Missing manufacturer!")
        return manu_keys[num]

    r_list = [None, 1, 2, 6]

    date = None
    manufacturer = None
    value = None

    for element in resp:
        R = element["R"] if "R" in element else None
        C = element["C"]

        if R not in r_list:
            print(R, C, sep="\t")
            raise Exception("Unknown R value!")

        manu_row = VaccinationByManufacturerRow(
            date=None, pfizer=None, moderna=None, az=None, janssen=None
        )

        if R == None:
            # all data
            date = parse_date(C[0])
            manufacturer = get_manufacturer((C[1]))
            value = int(C[2])
            setattr(manu_row, "date", date)
            setattr(manu_row, manufacturer, value)

        if R == 1:
            # same date as previous
            manufacturer = get_manufacturer((C[0]))
            value = int(C[1])
            setattr(parsed_data[-1], manufacturer, value)

        if R == 2:
            # same manufacturer as previous
            date = parse_date(C[0])
            value = int(C[1])
            setattr(manu_row, "date", date)
            setattr(manu_row, manufacturer, value)

        if R == 6:
            # same manufacturer and value as previous
            date = parse_date(C[0])
            setattr(manu_row, "date", date)
            setattr(manu_row, manufacturer, value)

        if R != 1:
            parsed_data.append(manu_row)
    return parsed_data


def _parse_vaccines_supplied_by_manufacturer_cum(
    data,
) -> "list[VaccinationByManufacturerRow]":
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for element in resp:
        elements = list(filter(lambda x: "M0" in x, element["X"]))

        date = parse_date(element["G0"])
        moderna = None
        pfizer = None
        az = None
        janssen = None

        for el in elements:
            if el.get("I", None) == 1:
                janssen = int(el["M0"])
            elif el.get("I", None) == 2:
                moderna = int(el["M0"])
            elif el.get("I", None) == 3:
                pfizer = int(el["M0"])
            else:
                az = int(el["M0"])

        parsed_data.append(
            VaccinationByManufacturerRow(
                date=date, pfizer=pfizer, moderna=moderna, az=az, janssen=janssen
            )
        )

    return parsed_data


def _parse_vaccinations_by_age_group(data) -> "list[VaccinationDose]":
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    date = None
    dose = None
    r_list = [None, 1]
    for element in resp:
        date = parse_date(element["G0"])
        R = R = element["X"][0]["R"] if "R" in element["X"][0] else None

        if R not in r_list:
            print(R)
            raise Exception("Unknown R value!")

        if R == None:
            dose = element["X"][0]["M0"]

        parsed_data.append(VaccinationDose(date=date, dose=dose))

    return parsed_data


# ? most likely we can refactor _parse_vaccinations_by_day
def _parse_vaccinations_by_region_by_day(data):

    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        # ? raise exception or return error obj
        return error

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    r_list = [None, 1]

    people_vaccinated = None
    people_fully_vaccinated = None
    for element in resp:
        date = parse_date(element["G0"])

        R = element["X"][0]["R"] if "R" in element["X"][0] else None

        if R == None:
            people_vaccinated = element["X"][0]["M0"]
            people_fully_vaccinated = (
                element["X"][1]["M0"] if len(element["X"]) > 1 else 0
            )

        if R == 1:
            # as far as we know people_vaccinated same as previous
            people_fully_vaccinated = (
                element["X"][1]["M0"] if len(element["X"]) > 1 else 0
            )

        parsed_data.append(
            VaccinationByDayRow(
                date=date,
                first_dose=people_vaccinated,
                second_dose=people_fully_vaccinated,
            )
        )

    return parsed_data


def _parse_vaccinations_by_municipalities_share(data) -> "list[VaccinationMunShare]":
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")
    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]
    parsed_data = []

    for el in resp:
        name, share1, population, share2 = el["C"]
        print(name, share1, population, share2, sep="\t")
        dose1 = round(int(population) * float(share1))
        dose2 = round(int(population) * float(share2))
        parsed_data.append(
            VaccinationMunShare(
                name=name,
                dose1=dose1,
                share1=float(share1),
                dose2=dose2,
                share2=float(share2),
                population=population,
            )
        )

    return parsed_data


def _parse_vaccinations_age_group_by_region_on_day(
    data,
) -> "list[VaccinationAgeGroupByRegionOnDay]":
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]

    def parse_resp_data(region, item):
        if len(item) == 4:
            return VaccinationAgeGroupByRegionOnDayDose(
                region=region,
                total_share=float(item[0]),
                group_share=float(item[1]),
                total_count=item[2],
                group_count=item[3],
            )
        if len(item) == 3:
            print(3, item)
            return VaccinationAgeGroupByRegionOnDayDose(
                region=region,
                total_share=float(item[0]),
                group_share=float(item[1]),
                total_count=item[2],
            )
        if len(item) == 2:
            return VaccinationAgeGroupByRegionOnDayDose(
                region=region,
                total_share=float(item[0]),
                total_count=item[1],
            )
        raise Exception('Unknown item length!')

    parsed_data = []
    for el in resp:
        region = el["G0"]
        first_dose = parse_resp_data(region, el["X"][0]["C"])
        second_dose = parse_resp_data(region, el["X"][1]["C"])
        parsed_data.append(
            VaccinationAgeGroupByRegionOnDay(
                region=region, dose1=first_dose, dose2=second_dose
            )
        )

    return parsed_data


def _parse_vaccinations_by_manufacturer_supplied_used(
    data,
) -> "list[VaccineSupplyUsage]":
    if "DS" not in data["results"][0]["result"]["data"]["dsr"]:
        error = data["results"][0]["result"]["data"]["dsr"]["DataShapes"][0][
            "odata.error"
        ]
        print(error)
        raise Exception("Something went wrong!")

    resp = data["results"][0]["result"]["data"]["dsr"]["DS"][0]["PH"][0]["DM0"]

    parsed_data = []
    item = None
    for el in resp:
        C = el["C"]
        date = parse_date(C[0])
        if len(C) == 2:
            item = VaccineSupplyUsage(date=date, supplied=int(C[1]), used=0)
            parsed_data.append(item)
        elif len(C) == 3:
            item = VaccineSupplyUsage(date=date, supplied=int(C[2]), used=int(C[1]))
            parsed_data.append(item)
        else:
            raise Exception("Unknown [C] length")

    return parsed_data
