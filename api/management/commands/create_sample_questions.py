from django.core.management.base import BaseCommand
from api.models import Question


class Command(BaseCommand):
    help = 'Create sample questions for testing'

    def handle(self, *args, **options):
        questions_data = [
            # 交通法规类
            {
                'type': 'single',
                'difficulty': 'easy',
                'question': '驾驶机动车在道路上违反道路交通安全法的行为，属于什么行为？',
                'options': ['A.违章行为', 'B.违法行为', 'C.过失行为', 'D.违规行为'],
                'correct_answer': 1,
                'explanation': '违反道路交通安全法属于违法行为。'
            },
            {
                'type': 'single',
                'difficulty': 'easy',
                'question': '机动车驾驶人初次申领驾驶证后的实习期是多长时间？',
                'options': ['A.6个月', 'B.12个月', 'C.16个月', 'D.18个月'],
                'correct_answer': 1,
                'explanation': '机动车驾驶人初次申领驾驶证后的实习期是12个月。'
            },
            {
                'type': 'single',
                'difficulty': 'easy',
                'question': '驾驶机动车在高速公路上行驶，最高车速不得超过每小时多少公里？',
                'options': ['A.100公里', 'B.110公里', 'C.120公里', 'D.130公里'],
                'correct_answer': 2,
                'explanation': '在高速公路上行驶，最高车速不得超过每小时120公里。'
            },
            {
                'type': 'single',
                'difficulty': 'medium',
                'question': '驾驶机动车在高速公路上行驶，遇有雾、雨、雪、沙尘、冰雹等低能见度气象条件时，能见度在200米以下时，车速不得超过每小时多少公里？',
                'options': ['A.60公里', 'B.80公里', 'C.90公里', 'D.100公里'],
                'correct_answer': 0,
                'explanation': '在高速公路上，能见度在200米以下时，车速不得超过每小时60公里。'
            },
            {
                'type': 'single',
                'difficulty': 'medium',
                'question': '驾驶机动车在高速公路上行驶，遇有雾、雨、雪、沙尘、冰雹等低能见度气象条件时，能见度在100米以下时，车速不得超过每小时多少公里？',
                'options': ['A.40公里', 'B.50公里', 'C.60公里', 'D.70公里'],
                'correct_answer': 0,
                'explanation': '在高速公路上，能见度在100米以下时，车速不得超过每小时40公里。'
            },
            {
                'type': 'single',
                'difficulty': 'hard',
                'question': '驾驶机动车在高速公路上行驶，遇有雾、雨、雪、沙尘、冰雹等低能见度气象条件时，能见度在50米以下时，车速不得超过每小时多少公里？',
                'options': ['A.20公里', 'B.30公里', 'C.40公里', 'D.50公里'],
                'correct_answer': 0,
                'explanation': '在高速公路上，能见度在50米以下时，车速不得超过每小时20公里。'
            },
            # 判断题
            {
                'type': 'judge',
                'difficulty': 'easy',
                'question': '驾驶机动车在高速公路上行驶，遇有雾、雨、雪、沙尘、冰雹等低能见度气象条件时，能见度在50米以下时，车速不得超过每小时20公里。',
                'options': ['正确', '错误'],
                'correct_answer': 0,
                'explanation': '在高速公路上，能见度在50米以下时，车速不得超过每小时20公里。'
            },
            {
                'type': 'judge',
                'difficulty': 'easy',
                'question': '机动车驾驶人初次申领驾驶证后的实习期是12个月。',
                'options': ['正确', '错误'],
                'correct_answer': 0,
                'explanation': '机动车驾驶人初次申领驾驶证后的实习期确实是12个月。'
            },
            {
                'type': 'judge',
                'difficulty': 'medium',
                'question': '驾驶机动车在高速公路上行驶，最高车速可以超过每小时120公里。',
                'options': ['正确', '错误'],
                'correct_answer': 1,
                'explanation': '在高速公路上行驶，最高车速不得超过每小时120公里。'
            },
            {
                'type': 'judge',
                'difficulty': 'medium',
                'question': '驾驶机动车在高速公路上行驶，遇有雾、雨、雪、沙尘、冰雹等低能见度气象条件时，能见度在200米以下时，车速不得超过每小时60公里。',
                'options': ['正确', '错误'],
                'correct_answer': 0,
                'explanation': '在高速公路上，能见度在200米以下时，车速不得超过每小时60公里。'
            },
            # 交通标志类
            {
                'type': 'single',
                'difficulty': 'easy',
                'question': '这个标志是何含义？',
                'options': ['A.禁止通行', 'B.禁止驶入', 'C.禁止停车', 'D.禁止掉头'],
                'correct_answer': 1,
                'explanation': '这是禁止驶入标志，表示禁止车辆驶入。'
            },
            {
                'type': 'single',
                'difficulty': 'easy',
                'question': '这个标志是何含义？',
                'options': ['A.直行', 'B.左转', 'C.右转', 'D.掉头'],
                'correct_answer': 0,
                'explanation': '这是直行标志，表示车辆只能直行。'
            },
            {
                'type': 'single',
                'difficulty': 'medium',
                'question': '这个标志是何含义？',
                'options': ['A.注意行人', 'B.注意儿童', 'C.学校区域', 'D.人行横道'],
                'correct_answer': 2,
                'explanation': '这是学校区域标志，表示前方有学校，需要减速慢行。'
            },
            # 安全驾驶类
            {
                'type': 'single',
                'difficulty': 'easy',
                'question': '驾驶机动车在道路上行驶，应当遵守什么原则？',
                'options': ['A.安全第一', 'B.速度第一', 'C.方便第一', 'D.效率第一'],
                'correct_answer': 0,
                'explanation': '驾驶机动车在道路上行驶，应当遵守安全第一的原则。'
            },
            {
                'type': 'single',
                'difficulty': 'medium',
                'question': '驾驶机动车在雨天行驶时，应当注意什么？',
                'options': ['A.降低车速', 'B.保持车距', 'C.开启雨刷', 'D.以上都是'],
                'correct_answer': 3,
                'explanation': '驾驶机动车在雨天行驶时，应当降低车速、保持车距、开启雨刷等。'
            },
            {
                'type': 'single',
                'difficulty': 'hard',
                'question': '驾驶机动车在夜间行驶时，应当注意什么？',
                'options': ['A.正确使用灯光', 'B.降低车速', 'C.保持车距', 'D.以上都是'],
                'correct_answer': 3,
                'explanation': '驾驶机动车在夜间行驶时，应当正确使用灯光、降低车速、保持车距等。'
            },
            # 更多判断题
            {
                'type': 'judge',
                'difficulty': 'easy',
                'question': '驾驶机动车在道路上行驶，应当遵守安全第一的原则。',
                'options': ['正确', '错误'],
                'correct_answer': 0,
                'explanation': '驾驶机动车在道路上行驶，应当遵守安全第一的原则。'
            },
            {
                'type': 'judge',
                'difficulty': 'medium',
                'question': '驾驶机动车在雨天行驶时，可以超速行驶。',
                'options': ['正确', '错误'],
                'correct_answer': 1,
                'explanation': '驾驶机动车在雨天行驶时，应当降低车速，不能超速行驶。'
            },
            {
                'type': 'judge',
                'difficulty': 'hard',
                'question': '驾驶机动车在夜间行驶时，可以不开灯光。',
                'options': ['正确', '错误'],
                'correct_answer': 1,
                'explanation': '驾驶机动车在夜间行驶时，必须开启灯光。'
            },
            # 更多单选题
            {
                'type': 'single',
                'difficulty': 'easy',
                'question': '驾驶机动车在道路上行驶，应当携带什么证件？',
                'options': ['A.驾驶证', 'B.行驶证', 'C.身份证', 'D.以上都是'],
                'correct_answer': 3,
                'explanation': '驾驶机动车在道路上行驶，应当携带驾驶证、行驶证等证件。'
            },
            {
                'type': 'single',
                'difficulty': 'medium',
                'question': '驾驶机动车在高速公路上行驶，遇有雾、雨、雪、沙尘、冰雹等低能见度气象条件时，应当开启什么灯光？',
                'options': ['A.近光灯', 'B.远光灯', 'C.雾灯', 'D.以上都是'],
                'correct_answer': 3,
                'explanation': '在低能见度气象条件下，应当开启近光灯、远光灯、雾灯等。'
            }
        ]

        created_count = 0
        for q_data in questions_data:
            question, created = Question.objects.get_or_create(
                question=q_data['question'],
                defaults=q_data
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new questions')
        )