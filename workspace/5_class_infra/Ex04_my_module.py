"""
모듈 · 패키지 · 라이브러리 개념
용어                비유            의미
모듈(Module)	    파일 한 장      .py 파일 하나로 구성된 부품(변수와 함수, 클래스)
패키지(Package)	    부품상자(폴더)   모듈들을 모아놓은 디렉토리
라이브러리(Library) 공구함	         패키지들의 집합, 유용한 기능의 대규모 집합체
"""

def add(a, b):
    return a+b
def hello(name):
    return f"{name} hello"
if "__name__" == "__main__":
    print(f"테스트 add : {add(2,3)}")
    print(f"테스트 hello : {hello('박길동')}")