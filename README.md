# SK NETWORKS AI CAMP 17기 - 4th - 2Team 
- 주제 : LLM을 연동한 내외부 문서 기반 질의 응답 웹페이지 개발
- 개발 기간 : 2025.10.23 ~ 2025.10.27

# 목차 
- [01. 팀 소개](#1️⃣-팀-소개)
- [02. 프로젝트 개요](#2️⃣-프로젝트-개요)
- [03. 기술 스택](#3️⃣-기술스택)
- [04. WBS](#4️⃣-wbs)
- [05. 요구사항 정의서](#5️⃣-요구사항-명세서)
- [06. 화면설계서](#6️⃣-화면설계서)
- [07. 시스템 아키텍처](#7️⃣-시스템-아키텍처)
- [08. 테스트 계획 및 결과](#8️⃣-테스트-계획-및-결과)
- [09. 수행 결과 및 향후 개선점](#9️⃣-수행-결과-및-향후-개선점)
- [10. 한 줄 회고](#한-줄-회고)


# 1️⃣ 팀 소개 

## ✅ 팀명 : ROOM MATE 🏠
사용자의 가장 가까운 주거 파트너가 되어 안정적인 시작을 도와주는 주택청약 도우미 챗봇 

## ✅ 팀원 소개 
| 김주서 | 김태완 | 성기혁 | 양송이 | 임산별 |
|:---:|:---:|:---:|:---:|:---:|
| <img src="img/KakaoTalk_20250925_111729446_02.jpg" width="120"/> | <img src="img/KakaoTalk_20250925_111729446_03.jpg" width="120"/> | <img src="img/KakaoTalk_20250925_111729446_04.jpg" width="120"/> | <img src="img/KakaoTalk_20250925_111729446_01.jpg" width="120"/> | <img src="img/KakaoTalk_20250925_111729446.jpg" width="120"/> |
| [@kimjuseo71](https://github.com/kimjuseo71) | [@Kicangel](https://github.com/Kicangel) | [@venus241004](https://github.com/venus241004) | [@songeeeey](https://github.com/songeeeey) | [@ImMountainStar](https://github.com/ImMountainStar) |
<br>

# 2️⃣ 프로젝트 개요 
## ✅ 2.1  프로젝트 명 | 청년과 신혼부부를 위한 주택청약 상담 웹 서비스 


## ✅ 2.2 프로젝트 소개 
- 사용자가 **복잡한 청약 절차**를 손쉽게 이해하고, 본인 조건에 맞는 물량과 주거지원까지 바로 확인할 수 있는 **통합형 챗봇 서비스**를 제공하는 웹 서비스입니다. 
- **공신력 있는 공공기관 자료**(국토교통부, LH·SH공사)의 실제 공고문과 정책 데이터를 기반으로, **정확하고 맞춤화된 청약 정보**를 제공합니다.

## ✅ 2.3 프로젝트 필요성 
### (1) 프로젝트 배경 : 상황분석
🏠 주택청약의 공급과 수요 증가 
> **청약통장 가입자, 2년 9개월 만에 증가…·청약 혜택 확대 통했나**  
> 3월 가입자 전월 대비 4435명 증가…
> 3기 신도시 기대감  
> 정부, 청년·신혼부부 청약 혜택 확대  
>  
> *박영규 기자, [이코노믹리뷰](https://www.econovill.com/news/articleView.html?idxno=693037), 2025.04.22 23:14*


> ### 💡 주택청약에 대한 관심과 이용자는 꾸준히 증가하고 있음
<br>


### (2) 문제 분석 
🔎 [ 주택청약 관심도와 신청과정에 대한 설문조사 ]  
<br>
  •	조사 대상: 20~30대 청년층 중심<br>
	•	조사 기간: 2025년 10월 24일 ~ 26일 <br>
	•	조사 목적: 주택청약 정보 접근성과 챗봇 서비스 필요성 파악<br>
<img src="img/survey.png" width="800"/>
<br>

🔎 [ 주택청약 관심도와 신청과정에 대한 In-Depth Interview ]

<br>
<img src="img/indepth.png" width="800"/>

<br>
🔎 [ 복잡한 청약절차 과정 ]
<br>

| [청약 절차 과정](https://hkpm.co.kr/%EC%95%84%ED%8C%8C%ED%8A%B8-%EC%9D%BC%EB%B0%98-%EB%B6%84%EC%96%91-%EC%B2%AD%EC%95%BD-%EC%A0%88%EC%B0%A8-%EC%88%9C%EC%84%9C-2024/) | [청약 신청 및 가점 계산](https://news.bizwatch.co.kr/article/real_estate/2019/09/06/0001) |
|---|---|
| <img src="img/intro.png" width="500"/> | <img src="img/intro2.jpg" width="400"/> |

- 잦은 제도 개편과 복잡한 공급방식 및 자격 요건으로 **복잡도** 증가
- 다양한 공급방식과 공급처로 인해 정보가 **산발적**으로 존재함
- 주택청약 정보를 종합적으로 제공처의 부재 
> ### 💡 그러나 높은 관심에도 불구하고, 주택청약  관련된 정보 접근의 어려움과 복잡한 절차로 인해 사용자 불편함이 존재함 
<br>

### (3) 문제 정의
1. **정보 접근성의 한계**  
   - 청약 관련 정보가 국토교통부, SH/LH, 지자체 등 여러 사이트에 흩어져 있어, 사용자가 원하는 정보를 한 번에 얻기 어려움  

2. **복잡한 청약 절차 구조**  
   - 자격 확인 → 청약 신청 → 당첨 확인 → 대출 및 입주까지 이어지는 절차가 복잡하며, 제도 변경도 잦아 사용자가 전체 과정을 이해하고 준비하는 데 어려움이 큼

3. **개인 맞춤형 정보 부족**  
   - 연령, 소득, 무주택 기간 등 개인 조건에 따라 가능한 공고와 대출 상품이 달라지지만, 이를 **한눈에 확인할 수 있는 서비스 부재**

<br>

> ### 💡 신뢰할 수 있는 데이터를 기반으로, 사용자 맞춤형으로 청약 정보를 안내해주는 웹 서비스가 필요함 
<br>

----

### (4) 프로젝트 목적 
- 주택청약 관련 공식 문서와 공고문 데이터를 기반으로 신뢰도 높은 정보를 제공하는 **챗봇 웹서비스 구현**
- 사용자 개인의 조건(연령, 소득, 무주택 기간 등)에 따라 맞춤형 공고, 매물, 주거지원정책 정보를 제공
- **대화형 인터페이스**를 통해 청약 절차·정보 탐색·공고 추천 과정을 간소화하고, 전체 청약 프로세스를 한 곳에서 지원
<br>

-----

<br>

# 3️⃣ 기술스택
## 3.1 기술스택
| 카테고리 | 기술 스택 |
|----------|-----------|
| **개발 언어** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **개발 도구** | ![VSCode](https://img.shields.io/badge/VSCode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![DockerHub](https://img.shields.io/badge/Docker_Hub-2496ED?style=for-the-badge&logo=docker&logoColor=white) |
| **벡터 DB** | ![Chroma](https://img.shields.io/badge/Chroma-1A73E8?style=for-the-badge&logoColor=white) |
| **사용 모델** | ![OpenAI Embedding](https://img.shields.io/badge/OpenAI_Embedding-412991?style=for-the-badge&logo=openai&logoColor=white) ![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-2E5D80?style=for-the-badge&logo=chainlink&logoColor=white) |
| **서버** | ![AWS EC2](https://img.shields.io/badge/AWS_EC2-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white) ![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white) |
| **추론 서버** | ![RunPod](https://img.shields.io/badge/RunPod-000000?style=for-the-badge&logoColor=white) ![FastAI](https://img.shields.io/badge/FastAI-1D1D1D?style=for-the-badge&logo=fastapi&logoColor=white) |
| **데이터베이스** | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white) |
| **협업 도구** | ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white) ![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white) |
| **프론트엔드** | ![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white) |

<br>



---

# 4️⃣ WBS 
[🔗 WBS 구글 드라이브](https://docs.google.com/spreadsheets/d/1kz7RMf0SV2hCc74jAFm7UAGFna9LBW-TEkAd6hnelKc/edit?usp=sharing)

![WBS](img/WBS.png)


<br>

# 5️⃣ 요구사항 명세서 
[🔗 요구사항 명세서 구글 드라이브](https://docs.google.com/spreadsheets/d/126VGwogx4I7AnjeoOFfWYTbYr2ocJjFrdAXC-5z1lK4/edit?pli=1&gid=0#gid=0)
![요구사항명세서](img/request_list.png)
<br>
<br>

# 6️⃣ 화면설계서

Intro Page
|  |
|------|
| ![화면1](img/1.jpg) |

Login Page
|  |
|------|
| ![화면1](img/2.jpg) |

Password Reset Page
|  |  |
|--------|--------|
| ![화면1](img/3_1.jpg) | ![화면2](img/3_2.jpg) |

Password Modify Page
|  |  |
|--------|--------|
| ![화면1](img/4_1.jpg) | ![화면2](img/4_2.jpg) |

Sign Page
| | |   |
|--------|--------|--------|
| ![화면1](img/5_1.jpg) | ![화면2](img/5_2.jpg) | ![화면3](img/5_3.jpg) |

Chat Page
|  |  |
|--------|--------|
| ![화면1](img/6_1.jpg) | ![화면2](img/6_2.jpg) |
<br>

# 7️⃣ 시스템 아키텍처
![시스템 아키턱처](img/system.png)

# 8️⃣ 테스트 계획 및 결과 

# 9️⃣ 수행 결과 및 향후 개선점 

## ✅ 9.1 수행결과 (테스트/시연 페이지)

### 🙋 사용자 페르소나 
**주택청약 청년 대상 페르소나 & 사용자 분석**
<img src="img/per.png" width="800"/>

<br>

#### 🔍 사용자 분석 
- **Needs**: 강동구에서 대출 기반으로 보증금 1억 이하 안정적인 주거 정보를 한눈에 파악할 수 있는 통합 플랫폼 필요
- **Pain Points**: 복잡한 청약 절차와 정보가 여러 사이트에 분산되어 있어, 효율적인 탐색과 비교가 어려움
- **Expected Value**: 챗봇과 통합된 웹서비스를 통해 개인 조건 기반의 공고, 청약 자격, 대출 정보 등을 한번에 확인

<br>

#### ⛳️ 고객 여정 기반 시나리오

| 고객 여정 단계 | 사용자 행동 | 
|----------------|--------------|
| 1. 진입 | 웹페이지 접속 → 서비스 소개 확인 | 
| 2. 챗봇 시작 클릭 | 'Start Chatbot' 클릭 → 로그인 페이지 이동 | 
| 3. 로그인 | 이메일과 비밀번호 입력 | 
| 4. 챗봇 사용 (유형 선택) | 청년 유형 선택 | 
| 5. 챗봇 사용 (질문 입력) | <br> Q 주택청약에 대해서 알려줘 ” | 
| 6. 개인정보 확인 | 챗봇 페이지 내 정보 모달 클릭 | 
| 7. 비밀번호 수정 | 상단 메뉴 → 비밀번호 변경 |
| 8. 로고 클릭 | 상단 로고 클릭 |
| 9. 챗봇 재진입 | 메인 페이지 'Start Chatbot' 클릭 | 
| 10. 회원 탈퇴 | 마이페이지 → 회원 탈퇴 선택 |
<br>

## 테스트 결과서 
![룸메이트테스트](img/test.png)

<br>

## 시현 영상 

<br>



##  ✅ 9.2 기대효과 
- **개인화된 상호작용** : 사용자의 나이, 소득, 자산, 청약 통장 등 맥락 정보를 반영하여 맞춤형 주택 정보, 정책 및 대출 상품을 제공 → 불필요한 정보 탐색 시간 절감
- **접근성 및 신정확성 확대** : 흩어진 공식 공고문, 정책 자료, FAQ 등 복잡한 정보를 통합해 간단한 인터페이스로 제공 → 주거 지원 정보 접근성 강화
- **시간 및 비용 절감 **: 공고 확인, 자격 검증, 가점 계산, 대출 가능 여부 파악 등 복잡한 절차를 챗봇이 자동화 → 사용자 입장에서 절차 소요 시간 단축 및 정보 탐색 비용 감소

## ✅ 9.3 향후 개선점 
1. **응답 형식 통일 및 개선** 
2. **UI/UX 개선 및 사용자 흐름 개선**: 로그인 -> 챗봇이용 -> 공고확인까지 흐름을 직관적으로 설계하여 사용자 이털 최소화  
3. **개인화 기능 강화** : 사용자의 나이, 소득, 무주택 기간 등에 기반한 맞춤형 공고·정책 추천 외에도, 가점 계산기, 주거지원 시뮬레이터 등 고도화된 사용자 도구 제공
4. **회원 기능 확장** : 기존 로그인/비밀번호 관리 기능 외에 개인 조건 저장, 추천 이력 관리, 관심 공고 즐겨찾기 등 기능 추가를 통해 지속적 활용 유도


# 🔟 한 줄 회고 
<table>
  <tr>
    <th style="width:80px;">이름</th>
    <th>회고 내용</th>
  </tr>
  <tr>
    <td>김태완</td>
    <td>기획부터 배포까지의 전 단계를 직접 수행하며, 단순한 기능 구현을 넘어 제품이 어떤 필요를 충족하고 어떤 의미 있는 경험을 제공해야 하는지를 이해하는 것이 개발자로서 가장 중요하다는 것을 깨달았습니다. 사용자의 관점을 바탕으로 문제를 분석하고 해결 전략을 설계하는 과정을 거치며, 기획·디자인·개발·운영이 하나의 프로세스로 긴밀히 맞물려야 한다는 점을 몸소 느꼈습니다. </td>
  </tr>
  <tr>
    <td>성기혁</td>
    <td> LLM의 원리를 이해하면 끝이라고 여겼으나 모델의 배포를 위해 AWS, Docker 등 어떤 것이 필요한지 알게 되었습니다 </td>
  </tr>
  <tr>
    <td>임산별</td>
    <td> 기획 설계와 프론트 엔드를 구성하며 앱 서비스 기획 단계부터 구현, 배포까지 웹 서비스 설계의 전체를 배울 수 있었다.</td>
  </tr>
  <tr>
    <td>양송이</td>
    <td> 이메일 인증, API 연동 등의 기능을 직접 구현하며 프론트엔드 코드와 백엔드 코드를 하나씩 맞춰가는 과정을 통해 웹 연동을 성공하였을 때의 성취감이 크게 느껴졌습니다.</td>
  </tr>
  <tr>
    <td>김주서</td>
    <td> </td>
  </tr>
</table>


<br>
</file>
