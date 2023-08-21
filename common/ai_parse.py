# -*- coding:utf-8 -*-
# ☯ Author: Jingyq
# ☯ Email: woshijingyongqiang@163.com
# ☯ Date: 2023/8/21 20:53
# ☯ Notes:

from util.requests_util import Requests as requests


class Recognizer():

    def __init__(self):
        self.url = "https://api.xiaoxizn.com/v1/peipei/parse_jd"

        self.headers = {
            "Content-Type": "application/json",
            "id": "de147a90-35b9-11ee-8909-8f6e2d26ec33",
            "secret": "d1a07d0d-62cb-48ec-9241-7b15d9cce11c"
        }

    def recognizer(self, text):
        data = {
            "job":{
                "description": text
            }
        }
        parse_data = requests.post(self.url, headers=self.headers, json=data, timeout=120).json()

        position_require = {
            "degree": "|".join([j for i, j in parse_data.get("standard", {}).get("degree", {}).items()
                                if "bound" in i and j != ""]),
            "major": "|".join([i.values() for i in parse_data.get("standard", {}).get("major", [])]),
            "school_level": "|".join([j for i, j in parse_data.get("standard", {}).get("school_level", {}).items()
                                      if "bound" in i and j != ""]),
            "professional_skills": parse_data.get("origin", {}).get("professional_skills", ""),
            "soft_skills": parse_data.get("origin", {}).get("soft_skills", ""),
            "languages": parse_data.get("origin", {}).get("languages", ""),
            "bonus_skills": parse_data.get("origin", {}).get("bonus_skills", ""),
            "industry_requirement": parse_data.get("origin", {}).get("industry_requirement", "")
        }

        return parse_data, position_require
