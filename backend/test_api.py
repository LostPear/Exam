#!/usr/bin/env python3
"""
API测试脚本
用于快速测试后端API是否正常工作
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_login():
    """测试登录功能"""
    print("\n=== 测试登录 ===")
    response = requests.post(
        f"{BASE_URL}/auth/login/",
        json={
            "username": "admin",
            "password": "admin"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 登录成功")
        print(f"   用户: {data['user']['username']}")
        print(f"   角色: {data['user']['role']}")
        print(f"   Token: {data['token'][:50]}...")
        return data['token']
    else:
        print(f"❌ 登录失败: {response.status_code}")
        print(f"   错误: {response.text}")
        return None

def test_questions(token):
    """测试获取题目列表"""
    print("\n=== 测试获取题目列表 ===")
    response = requests.get(
        f"{BASE_URL}/questions/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        count = data.get('count', len(data.get('results', [])))
        print(f"✅ 获取题目成功，共 {count} 道题")
        return True
    else:
        print(f"❌ 获取题目失败: {response.status_code}")
        return False

def test_random_questions(token):
    """测试获取随机题目"""
    print("\n=== 测试获取随机题目 ===")
    response = requests.get(
        f"{BASE_URL}/questions/random/?count=5",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 获取随机题目成功，共 {len(data)} 道题")
        if data:
            print(f"   示例题目: {data[0]['question'][:50]}...")
        return True
    else:
        print(f"❌ 获取随机题目失败: {response.status_code}")
        return False

def test_create_exam(token):
    """测试创建考试"""
    print("\n=== 测试创建考试 ===")
    response = requests.post(
        f"{BASE_URL}/exams/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "question_count": 5,
            "difficulty": "all"
        }
    )
    
    if response.status_code == 201:
        data = response.json()
        exam_id = data['id']
        print(f"✅ 创建考试成功，考试ID: {exam_id}")
        print(f"   题目数量: {data['total_questions']}")
        return exam_id
    else:
        print(f"❌ 创建考试失败: {response.status_code}")
        print(f"   错误: {response.text}")
        return None

def test_user_stats(token):
    """测试获取用户统计"""
    print("\n=== 测试获取用户统计 ===")
    response = requests.get(
        f"{BASE_URL}/stats/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ 获取统计成功")
        print(f"   练习总数: {data['total_practice']}")
        print(f"   考试总数: {data['total_exams']}")
        print(f"   练习正确率: {data['practice_accuracy']}%")
        return True
    else:
        print(f"❌ 获取统计失败: {response.status_code}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("Django后端API测试")
    print("=" * 50)
    
    # 测试登录
    token = test_login()
    if not token:
        print("\n❌ 登录失败，无法继续测试")
        return
    
    # 测试其他功能
    test_questions(token)
    test_random_questions(token)
    test_create_exam(token)
    test_user_stats(token)
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到服务器")
        print("   请确保Django服务器正在运行: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ 测试出错: {str(e)}")
