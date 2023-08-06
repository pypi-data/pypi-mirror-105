import asyncio
import aiohttp
from datetime import datetime
import json
from io import StringIO


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


async def main():
    data = await asyncSchoolSchedule("초등", "B10", "7081423", "6", "5")
    print(data)
asyncio.get_event_loop().run_until_complete(main())