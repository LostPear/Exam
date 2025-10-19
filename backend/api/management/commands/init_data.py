"""
初始化数据命令
"""
from django.core.management.base import BaseCommand
from api.models import User, Question, UserStats


class Command(BaseCommand):
    help = '初始化系统数据（创建默认用户和示例题目）'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化数据...')
        
        # 创建管理员用户
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin',
                role='admin'
            )
            UserStats.objects.create(user=admin)
            self.stdout.write(self.style.SUCCESS('✓ 创建管理员用户: admin/admin'))
        else:
            self.stdout.write('管理员用户已存在')
        
        # 创建普通用户
        if not User.objects.filter(username='user').exists():
            user = User.objects.create_user(
                username='user',
                email='user@example.com',
                password='password',
                role='user'
            )
            UserStats.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS('✓ 创建普通用户: user/password'))
        else:
            self.stdout.write('普通用户已存在')
        
        # 创建示例题目
        if Question.objects.count() == 0:
            sample_questions = [
                {
                    'type': 'single',
                    'difficulty': 'easy',
                    'category': '交通信号',
                    'question': '红灯表示：',
                    'options': ['禁止通行', '准许通行', '警示', '减速'],
                    'correct_answer': 0,
                    'explanation': '红灯表示禁止通行，这是交通规则的基本常识。'
                },
                {
                    'type': 'single',
                    'difficulty': 'easy',
                    'category': '交通信号',
                    'question': '黄灯表示：',
                    'options': ['准许通行', '警示', '禁止通行', '加速'],
                    'correct_answer': 1,
                    'explanation': '黄灯表示警示，提醒驾驶员注意，准备停车或谨慎通过。'
                },
                {
                    'type': 'judge',
                    'difficulty': 'easy',
                    'category': '安全驾驶',
                    'question': '驾驶机动车时可以使用手机接打电话。',
                    'options': ['正确', '错误'],
                    'correct_answer': 1,
                    'explanation': '驾驶时使用手机会分散注意力，容易导致交通事故，是违法行为。'
                },
                {
                    'type': 'single',
                    'difficulty': 'medium',
                    'category': '安全驾驶',
                    'question': '在高速公路上行驶，车速超过每小时100公里时，应当与同车道前车保持多少米以上的距离？',
                    'options': ['50米', '80米', '100米', '120米'],
                    'correct_answer': 2,
                    'explanation': '根据交通法规，车速超过100km/h时，应保持100米以上的安全距离。'
                },
                {
                    'type': 'single',
                    'difficulty': 'medium',
                    'category': '违法处理',
                    'question': '驾驶机动车在高速公路上倒车、逆行、穿越中央分隔带掉头的，一次记多少分？',
                    'options': ['3分', '6分', '9分', '12分'],
                    'correct_answer': 3,
                    'explanation': '在高速公路上倒车、逆行、穿越中央分隔带掉头的，一次记12分。'
                },
                {
                    'type': 'judge',
                    'difficulty': 'medium',
                    'category': '安全驾驶',
                    'question': '夜间驾驶机动车通过人行横道时应使用远光灯。',
                    'options': ['正确', '错误'],
                    'correct_answer': 1,
                    'explanation': '通过人行横道时应使用近光灯，远光灯会影响行人和其他车辆的视线。'
                },
                {
                    'type': 'single',
                    'difficulty': 'hard',
                    'category': '紧急情况',
                    'question': '在道路上发生交通事故，造成人身伤亡的，驾驶人应当首先做什么？',
                    'options': ['保护现场', '抢救受伤人员', '报警', '拍照取证'],
                    'correct_answer': 1,
                    'explanation': '发生事故造成人员伤亡时，应首先抢救受伤人员，保护生命安全是第一位的。'
                },
                {
                    'type': 'single',
                    'difficulty': 'hard',
                    'category': '复杂路况',
                    'question': '在冰雪道路上行车时，车辆的稳定性降低，加速过急时车轮容易发生什么情况？',
                    'options': ['侧滑', '空转', '溜坡', '熄火'],
                    'correct_answer': 1,
                    'explanation': '冰雪路面附着力小，加速过急时车轮容易空转打滑。'
                },
                {
                    'type': 'judge',
                    'difficulty': 'hard',
                    'category': '安全驾驶',
                    'question': '车辆发生爆胎后，驾驶人应在控制住方向的情况下，轻踏制动踏板，使车辆缓慢减速。',
                    'options': ['正确', '错误'],
                    'correct_answer': 0,
                    'explanation': '爆胎后应握稳方向盘，轻踩制动，缓慢减速，避免急刹车导致车辆失控。'
                },
                {
                    'type': 'single',
                    'difficulty': 'easy',
                    'category': '交通标志',
                    'question': '这个标志是何含义？（圆形红色边框，中间有一个叉）',
                    'options': ['禁止通行', '禁止停车', '禁止驶入', '限速标志'],
                    'correct_answer': 0,
                    'explanation': '红色圆形边框内有叉号表示禁止通行。'
                },
            ]
            
            for q_data in sample_questions:
                Question.objects.create(**q_data)
            
            self.stdout.write(self.style.SUCCESS(f'✓ 创建 {len(sample_questions)} 道示例题目'))
        else:
            self.stdout.write(f'题库中已有 {Question.objects.count()} 道题目')
        
        self.stdout.write(self.style.SUCCESS('\n数据初始化完成！'))
        self.stdout.write('\n默认账户：')
        self.stdout.write('  管理员: admin / admin')
        self.stdout.write('  用户: user / password')
