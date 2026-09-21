#포함 연산자
# # str
# print("---string---")
# # print("a" in "apple")
# print("ap" not in "apple")
# #문자열속 단어 가능, 문자열속 문자열 불가능 // Trie는 아닌가봄

# #arr
# print("---arr---")
# fruits= ["apple","banana","orange"]
# print('print("apple" in fruits)')
# print("apple" in fruits)
# print('print("Apple" in fruits)')
# print("Apple" in fruits) #대문자 구별함

#식별 연산자

a, b = 10, 10
print(a==b)
print(a is b)
a = [10]
c = [10]
print(a==c)
print(a is c)

#인덱싱

s = "abcdefgh"
print(s[])

#문자열 포맷
# 천 단위 쉼표 표시

money = 123456748
print(f"금액 : {money:,}원")


# 자릿수지정 : 서버번호-00X

server_number = 3
print(f"서버 번호-{server_number:3d}")

# import random
# random.randint(a, b)	#a ~ b 사이의 정수 난수
# random.uniform(a, b)	#a ~ b 사이의 실수 난수
# random.random()	#0 이상 1 미만의 실수 난수