# competi_plantfriend

### LIST
개발 요약
개발 기간
개발자

목적 및 필요성
차별화

하드웨어
소프트웨어

결과

참고자료




## 개발 요약
![개요](https://user-images.githubusercontent.com/82786563/135183208-4bd1df89-9ae7-4349-a3be-72ce69628a76.png)

✔ 화분과 AI 스피커를 합친 형태의 스마트 화분으로 식물의 생육 환경을 감지하고 필요한 양분을 제공하여 사용자에게 편의 제공<br>
✔ 기존의 AI 스피커에 식물의 생육 환경을 감지하고 자동으로 물을 주는 시스템을 추가한 형태<br>


## 개발 기간
2021.07 ~ 


## 개발자

김지원 geewon1117@gmail.com<br>
김창우<br>
조경민<br>


## 개발 목적 및 필요성
   #### 개발목적
    - 식물의 경우 동물과 달리 행동으로 의사표현을 하지 않음
    - 따라서 양분이 필요한 시기를 놓칠 수 있음
    - 사용자에게 식물의 생육환경 정보 및 솔루션을 제공하여 편의성 증대
   #### 작품의 차별화 및 사업성
    - 기존의 IoT로 구성된 스마트 화분에 인공지능스피커를 덧붙인 형태로 사용자의 음성에 맞춰 서비스를 제공함
    - 1인 가구의 증가와 미세먼지 등 환경 악화로 실내 식물의 수요 증가
    - 식물과의 소통에 중점을 두고 식물의 반려화 사업 가능성
    - 한국어 인식에 특화하기 위해 카카오 API 채용

![SWOT](https://user-images.githubusercontent.com/82786563/135183255-284f30d6-1666-4e6f-9e2b-b46178ddc273.png)

## 개발 목표
![함수종류](https://user-images.githubusercontent.com/82786563/135183245-d4be93ed-6383-4da7-9003-386debb9b495.png)
    - 라즈베리파이3 기반 카카오 음성인식 API를 이용한 AI 스피커 구현<br>
    - 라즈베리파이3의 GPIO 센서에 토양수분 센서를 연동한 후, 식물의 생육 환경을 탐지 및 모니터링<br>
    - 식물의 DB 정보를 읽어 들여 적절한 생육환경을 유지할 수 있도록 탐지된 토양의 습도, 실내온도 등을 기반으로 사용자에게 정보 제공<br>




## 하드웨어
- 라즈베리파이 3B+
- 토양습도센서
- - 모델명 : FC-28
- - 동작 전압 : 3.3V – 5V
- - 동작 전류 : 30mA
- - 핀구성 : 4핀(VCC/GND/DO/AO)
- usb 마이크 / 스피커


## 소프트웨어
#### 개요
![코드예시](https://user-images.githubusercontent.com/82786563/135183242-d2ad720e-2d87-49b3-968f-581d0c2549c3.png)


#### 알고리즘
![알고리즘](https://user-images.githubusercontent.com/82786563/135183239-4d5d380b-267b-4b90-984c-158c00f27b08.png)






 
