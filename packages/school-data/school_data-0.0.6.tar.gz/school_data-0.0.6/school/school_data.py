import asyncio
import aiohttp
from datetime import datetime
import json
from io import StringIO
import jwt
from base64 import b64decode, b64encode


# -- 서울 강월초등학교 코드 --
# 시도 교육청: 서울특별시교육청 (B10)
# 학교 코드: 7081423

pubkey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA81dCnCKt0NVH7j5Oh2+SGgEU0aqi5u6sYXemouJWXOlZO3jqDsHYM1qfEjVvCOmeoMNFXYSXdNhflU7mjWP8jWUmkYIQ8o3FGqMzsMTNxr+bAp0cULWu9eYmycjJwWIxxB7vUwvpEUNicgW7v5nCwmF5HS33Hmn7yDzcfjfBs99K5xJEppHG0qc+q3YXxxPpwZNIRFn0Wtxt0Muh1U8avvWyw03uQ/wMBnzhwUC8T4G5NclLEWzOQExbQ4oDlZBv8BM/WxxuOyu0I8bDUDdutJOfREYRZBlazFHvRKNNQQD2qDfjRz484uFs7b5nykjaMB9k/EJAuHjJzGs9MMMWtQIDAQAB=="
easter_egg_password = "# THIS IS PASSWORD # LENGTH IS 6"

# async def asyncEasterEgg(password):
#     if len(easter_egg_password) > len(password):
#         return "PASSWORD IS LOCK."
#     elif easter_egg_password == str(password):
#         return "# THIS IS EASTER EGG MESSAGE #"
#     else:
#         return "PASSWORD IS LOCK."

# def EasterEgg(password, loop=asyncio.get_event_loop()):
#     return loop.run_until_complete(asyncEasterEgg(password))



async def asyncNow(): # time function
    now = datetime.now()
    return now.strftime('%Y%m%d')

def now(loop=asyncio.get_event_loop()): # get now
    return loop.run_until_complete(asyncNow())


async def asyncSchoolTypeCheck(school_type):
    typelist = ["elsTimetable", "misTimetable", "hisTimetable", "spsTimetable", "els", "mis", "his", "sps", "초등", "중등", "고등", "특수", "초등학교", "중학교", "고등학교", "특수학교"]
    if school_type in typelist:
        if school_type in ["elsTimetable", "els", "초등", "초등학교"]:
            return {"error":False, "code": "SUCCESS", "message": "성공적으로 학교 타입에서 찾았습니다.", "url": "https://open.neis.go.kr/hub/elsTimetable?Type=json", "type": "elsTimetable"}
        elif school_type in ["misTimetable", "mis", "중등", "중학교"]:
            return {"error":False, "code": "SUCCESS", "message": "성공적으로 학교 타입에서 찾았습니다.", "url": "https://open.neis.go.kr/hub/misTimetable?Type=json", "type": "misTimetable"}
        elif school_type in ["hisTimetable", "his", "고등", "고등학교"]:
            return {"error":False, "code": "SUCCESS", "message": "성공적으로 학교 타입에서 찾았습니다.", "url": "https://open.neis.go.kr/hub/hisTimetable?Type=json", "type": "hisTimetable"}
        elif school_type in ["spsTimetable", "sps", "특수학교", "특수"]:
            return {"error":False, "code": "SUCCESS", "message": "성공적으로 학교 타입에서 찾았습니다.", "url": "https://open.neis.go.kr/hub/spsTimetable?Type=json", "type": "spsTimetable"}
    else:
        return {"error":True, "code": "WRONGSCHOOLTYPE", "message":"학교 타입에서 찾을수없습니다.", "school_type": school_type}

def SchoolTypeCheck(school_type, loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncSchoolTypeCheck(school_type=school_type))

async def asyncSchoolSchedule(school_type, country_code, school_code, grade, classNm, perio=None, date=now()):
    # type list url: elsTimetable, misTimetable, hisTimetable, spsTimetable
    typelist = ["elsTimetable", "misTimetable", "hisTimetable", "spsTimetable", "els", "mis", "his", "sps", "초등", "중등", "고등", "특수", "초등학교", "중학교", "고등학교", "특수학교"]
    if school_type in typelist:
        asyncSchoolType = await asyncSchoolTypeCheck(school_type)
        if asyncSchoolType["error"] == False:
            url = asyncSchoolType["url"]
            if perio != None:
                url = f"{url}&ATPT_OFCDC_SC_CODE={country_code}&SD_SCHUL_CODE={school_code}&GRADE={grade}&CLASS_NM={classNm}&ALL_TI_YMD={date}&perio={perio}"
            else:
                url = f"{url}&ATPT_OFCDC_SC_CODE={country_code}&SD_SCHUL_CODE={school_code}&GRADE={grade}&CLASS_NM={classNm}&ALL_TI_YMD={date}"

            # -- code escape --
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        data = await response.text()
                        data = StringIO(data)
                        data = json.load(data)
                        data = data[asyncSchoolType["type"]]

                        row = data[1]['row']

                        # one_perio = row[1]
                        perio_list = [{row[0]['PERIO']: row[0]['ITRT_CNTNT']}, {row[1]['PERIO']: row[1]['ITRT_CNTNT']}, {row[2]['PERIO']: row[2]['ITRT_CNTNT']}, {row[3]['PERIO']: row[3]['ITRT_CNTNT']}, {row[4]['PERIO']: row[4]['ITRT_CNTNT']}]
                        # return data[1]['row'][0]
                        return {"error": False, "code": "SUCCESS", "message": "성공적으로 시간표를 불러왔습니다.", "schedule": perio_list}
            except KeyError:
                return {"error": True, "code":"FORMET", "message":"입력하신 시간표를 찾을수 없습니다."}
            
            except Exception:
                return {"error": True, "code": "UNKNOWN", "message": "알수없는 오류."}

        else:
            return {"error": True, "code": "UNKNOWN", "message": "알수없는 오류."}
    else:
        return {"error": True, "code": "WRONGSCHOOLTYPE", "message": "학교 타입에서 찾을수없습니다.", "school_type":typelist}


def SchoolSchedule(school_type, country_code, school_code, grade, classNm, perio=None, date=now(), loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncSchoolSchedule(school_type, country_code, school_code, grade, classNm, perio=perio, date=date))







async def asyncMealData(country_code, school_code, meal_code="2", date=now()): # 급식 데이터
    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?&Type=json&ATPT_OFCDC_SC_CODE={country_code}&SD_SCHUL_CODE={school_code}&MMEAL_SC_CODE={meal_code}&MLSV_YMD={date}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text() # data setting
                data = data.replace("<br/>", "")
                data = data.replace("*", ", ")
                data = StringIO(data)
                data = json.load(data)
                data = data["mealServiceDietInfo"]

                # -- meal data setting --
                school_data = data[1]['row'][0]
                return {"error": False, "code": "SUCCESS", "message": "성공적으로 데이터를 불러왔습니다.", "area_name":school_data["ATPT_OFCDC_SC_NM"], "area_code":school_data["ATPT_OFCDC_SC_CODE"], "school_name": school_data["SCHUL_NM"], "school_code":school_data["SD_SCHUL_CODE"], "meal":school_data["DDISH_NM"], "nutrient": school_data["NTR_INFO"], "origin":school_data["ORPLC_INFO"]}
    except KeyError:
        return {"error": True, "code":"FORMET", "message":"입력하신 정보를 찾을수 없습니다."}

    except Exception as e:
        return {"error": True, "code":"UNKNOWN", "message":"알 수 없는 에러 발생."}

def meal_data(country_code, school_code, meal_code="2", date=now(), loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncSchoolData(country_code=country_code, school_code=school_code, meal_code=meal_code, date=date))


async def asyncSchoolData(school_name):
    url = f"https://open.neis.go.kr/hub/schoolInfo?SCHUL_NM={school_name}&Type=json"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text() # data setting
                data = StringIO(data)
                data = json.load(data)
                data = data["schoolInfo"]
                # -- school data setting --
                row = data[1]['row'][0]
                return {"error": False, "code":"SUCCESS", "message":"성공적으로 데이터를 불러왔습니다.", "area_code":row["ATPT_OFCDC_SC_CODE"], "area_name":row["ATPT_OFCDC_SC_NM"], "school_code":row["SD_SCHUL_CODE"], "school_name":row["SCHUL_NM"], "eng_school_name":row["ENG_SCHUL_NM"], "school_type":row["SCHUL_KND_SC_NM"], "phone_number":row["ORG_TELNO"], "website":row["HMPG_ADRES"], "location":row["ORG_RDNMA"], "fond":row["FOND_SC_NM"], "gender_type":row["COEDU_SC_NM"]}
    except KeyError:
        return {"error": True, "code":"FORMET", "message":"입력하신 학교를 찾을수 없습니다."}

def school_data(school_name, loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncSchoolData(school_name=school_name))





# -- get token --
async def asyncMealToken(school_name, meal_code="2"):
    api_result = await asyncSchoolData(school_name)

    if api_result["error"]:
        return api_result
    
    data = {
        "country_code": str(api_result["area_code"]),
        "school_code": str(api_result["school_code"]),
        "meal_code": str(meal_code)
    }

    jwt_token = jwt.encode(data, pubkey, algorithm="HS256")

    if isinstance(jwt_token, str):
        jwt_token = jwt_token.encode("utf-8")
    
    token = b64encode(jwt_token).decode("utf-8")

    return {"error": False, "code": "SUCCESS", "message": "토큰 발급 성공!", "token": token}



async def asyncMealTokenCheck(token: str, date=now()):
    try:
        data = jwt.decode(b64decode(token), pubkey, algorithms="HS256")

    except Exception:
        return {"error": True, "code": "WRONGTOKEN", "message": "올바르지 않은 토큰입니다."}


    return await asyncMealData(data["country_code"], data["school_code"], data["meal_code"], date)

def MealToken(school_name, loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncMealToken(school_name))

def MealTokenCheck(token, date=now(), loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncMealTokenCheck(token, date))


async def asyncScheduleToken(school_type, school_name, grade, classNm):
    api_result = await asyncSchoolData(school_name)

    if api_result["error"]:
        return api_result

    type_result = await asyncSchoolTypeCheck(school_type)

    if type_result["error"]:
        return type_result
    
    data = {
        "school_type": str(type_result['type']),
        "country_code": str(api_result["area_code"]),
        "school_code": str(api_result["school_code"]),
        "grade": str(grade),
        "classNm": str(classNm)
    }

    jwt_token = jwt.encode(data, pubkey, algorithm="HS256")

    if isinstance(jwt_token, str):
        jwt_token = jwt_token.endswith("utf-8")

    token = b64encode(jwt_token).decode("utf-8")

    return {"error": False, "code": "SUCCESS", "message": "토큰 발급 성공!", "token": token}

async def asyncScheduleTokenCheck(token: str, perio=None, date=now()):
    try:
        data = jwt.decode(b64decode(token), pubkey, algorithms="HS256")
    except Exception:
        return {"error": True, "code": "WRONGTOKEN", "message": "올바르지 않은 토큰입니다."}

    return await asyncSchoolSchedule(data['school_type'], data['country_code'], data['school_code'], data['grade'], data['classNm'], perio=perio, date=date)
def ScheduleToken(school_type, school_name, grade, classNm, loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncScheduleToken(school_type, school_name, grade, classNm))

def ScheduleTokenCheck(token, perio=None, date=now(), loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncScheduleTokenCheck(token, perio, date))


# -- testing --