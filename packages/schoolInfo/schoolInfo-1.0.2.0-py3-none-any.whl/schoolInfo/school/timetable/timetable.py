import asyncio

import schoolInfo.util as util


@util.except_keyError
async def timetable(
    ATPT_OFCDC_SC_CODE: str,
    SD_SCHUL_CODE: str,
    SCHUL_KND_SC_NM: str,
    AY: str = '',
    SEM: str = '',
    ALL_TI_YMD: str = '',
    GRADE: str = '',
    CLASS_NM: str = '',
    TI_FROM_YMD: str = '',
    TI_TO_YMD: str = '',
    auth_key: str = '',
):
    school_type: dict = {
        "초등학교": "elsTimetable",
        "중학교": "misTimetable",
        "고등학교": "hisTimetable",
        "특수학교": "spsTimetable",
    }

    addition: list = [
        f"ATPT_OFCDC_SC_CODE={ATPT_OFCDC_SC_CODE}",
        f"SD_SCHUL_CODE={SD_SCHUL_CODE}",
        f"AY={AY}",
        f"SEM={SEM}",
        f"ALL_TI_YMD={ALL_TI_YMD}",
        f"GRADE={GRADE}",
        f"CLASS_NM={CLASS_NM}",
        f"TI_FROM_YMD={TI_FROM_YMD}",
        f"TI_TO_YMD={TI_TO_YMD}",
    ]

    url: str = util.url_manager(
        type=school_type[SCHUL_KND_SC_NM], additions=addition, auth_key=auth_key
    ).get_url()
    return (await util.HTMLGetter().get_json(url))[school_type[SCHUL_KND_SC_NM]][1][
        "row"
    ]
