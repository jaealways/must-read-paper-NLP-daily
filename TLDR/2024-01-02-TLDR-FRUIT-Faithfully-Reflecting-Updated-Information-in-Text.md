---
layout: post
title:  "[TLDR] FRUIT: Faithfully Reflecting Updated Information in Text"
author: jaealways
categories: [ paper, NLP]
tags: [TLDR, NAACL'22, Information]
---


# [TLDR] FRUIT : Faithfully Reflecting Updated Information in Text


[reference: Robert L. Logan IV et al, "FRUIT : Faithfully Reflecting Updated Information in Text", 2022](https://arxiv.org/pdf/2112.08634.pdf)



# Abstract
- 위키피디아와 같은 **텍스트 지식 베이스를 최신 상태로 유지**하기 위해 **외부 지식에 기반**한  **편집제안 문제**는 
충분히 탐구 되지 않았다.
- 이 논문에서는 **텍스트에서 업데이트된 정보를 충실히 반영**하여 **기존 문서를 업데이트**하는  것을 목표로 하는 **FRUIT** 방법 제안.
- **FRUIT-WIKI dataset**: Wikipedia snapshot 쌍에서 생성된 17만 개 이상의 distantly supervised data로 구성된 데이터
- 편집용 T5 기반 모델인 **EDIT5**를 소개.

# 1 Introduction

- 스포츠, 엔터테인먼트, 일반 지식 등 분야에서 **정보**는 **동적으로 변화**
- 이러한 **변화된 정보**를 **반영**하여 **텍스트 기반 지식 베이스를 유지**하는 노력 필요
    - 영어 위키백과에서 12만명의 인원이 분당 약 120회의 편집을 하고 매일 600개의 새로운 문서 작성 <br />→ 지식 베이스가 확장됨에 따라 유지보수 작업의 양도 증가하여 정보의 일관성을 유지하는데 어려움
- 다양한 선행 연구들이 있었지만 외부 지식에 기반한 편집을 제안하는 문제는 충분히 탐구되지 않았다.<br />→ **기존 텍스트**에 **새로운 정보를 통합**하는 "**FRUIT**"라는 새로운 텍스트 생성 작업 제안
  ![image](https://github.com/in-sukim/NLP-Paper/assets/43094223/d2a886bb-2c5b-438a-93ef-b0d28d80a2e9)

- **도전과제**
  - 새로운 정보가 기존 정보와 모순되는 경우, 기존 정보를 우선시해야 한다.
  - 생성된 텍스트는 원본 문서와 새로운 정보를 모두 반영,기존 정보와 새로운 정보가 모순되는 경우를 제외하고는 일관성을 유지해야 한다. <br />→ 따라서 이 작업은 다중 문서 요약과 데이터-텍스트 생성 태스크에서 발생할 수 있는 도전 과제의 결합 유형

- **FRUIT-WIKI**
    - 자동화된 프로세스를 통해 생성된 17만개 데이터. 위키피디아 스냅샷을 비교하여 문서 업데이트를 식별하고 파이프라인을 통해 업데이트-기존 데이터 쌍 데이터 생성
    - Silver Dataset이기 때문에 human annotated된 914개의 Gold Dataset 구축
    - Silver Data로 모델을 훈련하고 검증한 후, Gold Dataset으로 최종 성능 평가
 
# 2. The FRUIT Task

## **2.1 Task Definition**
원본 텍스트에 대한 새로운 정보의 컬렉션이 주어지는 경우,목표는 원본 텍스트를 새로운 정보를 반영하도록 업데이트하는 것. <br />
- 특정 주제 $A$에 대해 시점 $t,t'$에 작성된 텍스트 쌍 $A^t, A^{t'}$<br />
- t 시점과 t' 사이의 새로운 정보를 입증하는 데 사용되는 증거 조각,즉 Evidence $\mathcal{E}^{t \rightarrow t'} = {E_1, .. E_{|\mathcal{E}|}}$ <br />
- 새로운 증거는 구조화된 객체와 그렇지 않은 텍스트가 포함될 수 있다.
- $A^t$와 $\mathcal{E}^{t \rightarrow t'}$가 주어졌을 때, 업데이트 된 $A^{t'}$를 생성하는 것이 목표

이 task를 수행하기 위해선 모델은 어떤 새로운 정보(Evidence)가 원본 텍스트와 모순되는지, 주제에 대해 새로운 중요한 정보를 도입하는지 식별 능력 필요 <br />
이를 통해 기존의 텍스트를 수정할지 새로운 텍스트를 추가할지 선택할 수 있다.

## **2.2 Evaluation**
- **Evaluate on Updated Text**
    - 업데이트 된 텍스트의 경우 원본 텍스트와 많은 중복이 있을 수 있다. ROUGE(Lin, 2004)와 같은 메트릭으로 평가한다면 어떠한 업데이트를 수행하지 않고 높은 점수를 얻을 수 있다.
    - FRUIT 시스템을 평가하기 위해 UpdateROUGE를 제안.
    - 전체 텍스트가 아닌 업데이트된 문장만을 고려.
- **Evaluate Faithfulness**
    - 생성된 내용이 Evidence와 업데이트된 기사의 정보를 얼마나 정확하게 반영하는지 평가하는 방법
    - **Unsupported Entity Tokens**
        - 생성된 Output에서 나타나는 Named Entity 중, 원본 텍스트,새로운 정보에는 없는 Named Entity의 평균 수를 측정:<br/> 높으면 신뢰성이 낮음.
    - **Entity Precision and Recall**
        - **Entity Precision**
            - 생성된 텍스트에 포함된 Named Entity들이 원본 텍스트,새로운 정보에 실제로 존재하는지 측정
            - 높은 정밀도는 생성된 텍스트 내의 Named Entity들이 원본 텍스트와 잘 일치함을 의미
        - **Entity Recall**
            - 원본 텍스트에 있는 Named Entity들이 생성된 텍스트에 잘 포함되어 있는지 나타낸다.
            - 높은 재현율은 원본 텍스트의 Named Entity를 생성된 텍스트에서 잘 포함하고 있음을 의미.
- **Parametric Knowledge Consideration**
    - FRUIT 시스템은 훈련 데이터에서 배운 정보에 의존하는 것이 아니라, 주어진 새로운 정보를 바탕으로 판단해야 한다.
    - 즉, 훈련 중에 얻는 Parametric Knowledge를 넘어서, 실제로 제공된 정보와 최신 정보를 분석하고 통합하는 능력을 가져야 한다.

# 3. Dataset Collection and Analysis
FRUIT-WIKI 데이터셋과 관련된 데이터 수집 파이프라인.

## 3.1 Pipeline
Wikipedia 스냅샷 쌍으로부터 annotated training, evalutaion 데이터 생성.
### Step 1.
source(원본 텍스트)과 target(새로운 정보)에 나타난 문서의 서론을 포함한 다른 부분의 변경 사항을 찾기 위해 분석($\mathcal{E}^{t \rightarrow t'})$<br />
텍스트 내의 문장 형태뿐만 아니라 새로운 테이블, 목록 등의 형태로 나타날 수 있다. Wikipedia 하이퍼링크를 사용하여 개체를 구분.

### Step 2.
새로운 정보의 추가 없이 기존 정보를 스타일적인 업데이트만 한 경우 분석에서 제외. 예를 들어 새로운 내용 추가 없이 문장을 다시 쓰는 것, 문법 수정, 형식 변경 등.

### Step 3.
Step 1에서 식별된 변경 사항을 검증하는 단계. 이를 통해 FRUIT-WIKI 데이터셋의 신뢰성을 유지하는데 도움이 된다.<br/>
업데이트 된 문장 $a \in A^{t'}$에 추가된 개체 $s'$가 포함된 경우, $s'$가 증거 조각 $\mathcal{E}^{t \rightarrow t'}$에서도 언급된 경우에만 a가 $\mathcal{E}$의 증거 조각에 의해 입증된다. <br/>업데이트된 문장에 추가된 개체가 어떤 증거에 언급되는지 확인하여 문장을 검증.

## 3.2 FRUIT-WIKI
![image](https://github.com/in-sukim/NLP-Paper/assets/43094223/dabf61cf-8153-4ef5-85b8-70e1ccac51f1)<br/>
훈련 데이터셋: 2019년 11월 20일 ~ 2020년 11월 20일. <br />
평가 데이터셋: 2020년 11월 20일 ~ 2021년 6월 1일. <br />
- 평균적으로, 각 문서당 약 3~4개의 업데이트가 있으며, 연관된 증거 조각은 약 7개 정도. 업데이트의 약 80%는 업데이트를 수행할 때 일부 증거를 무시하는 형태의 콘텐츠 선택이 필요. <br />
- 증거 조각에 의해 입증되지 않은 추가된 정보를 모델이 학습 시 hallucinate를 일으킬 수 있기 때문에 human annotations과 평가 메트릭을 사용하여 이 문제가 어느정도인지 연구.<br />
![image](https://github.com/in-sukim/NLP-Paper/assets/43094223/acb1ddae-8e52-48bc-bf0d-8ca0ec741283) <br />
Topic model(Asthana and Halfaker, 2018)을 통해 업데이트 된 데이터셋의 기사를 분류했을 때, 분포. <br/>
STEM: Science, Technology, Engineering, Mathematics(과학, 기술, 공학, 수학)

## 3.3 Gold Evaluation Data
- 9명의 annotators로 구성된 팀을 통해 생성. 914개의 update-evidence pair에 대한 annotation 수집<br/>
- 소스 기사, 증거, 그리고 목표 기사의 각 업데이트된 문장을 검토하도록 지시(Figure A7 Instructions 참고) <br />
- 원문 텍스트, 추가된 정보 변경 수정 불가, 업데이트된 정보를 주석으로 강조, 업데이트 된 텍스트 복사 후 기존 문서를 최소한으로 편집. <br />
- 작업 초기 단계에는 정기적인 피드백과 30분의 훈련. 다른 annotator의 작업을 점검하고 오류를 수정하는 인원 추가 고용
- 약 500시간 작업 투입.<br/>
![image](https://github.com/in-sukim/NLP-Paper/assets/43094223/95a96a0e-4005-4a72-a84d-4adce64f52ab)<br />
ROUGE-1:시스템 요약본과 참조 요약본 간 겹치는 unigram의 수를 보는 지표<br/>
ROUGE-2:시스템 요약본과 참조 요약본 간 겹치는 bigram의 수를 보는 지표<br />
ROUGE-N: unigram, bigram, trigram 등 문장 간 중복되는 n-gram을 비교하는 지표

# 4.Method
Baseline model로 T5(Raffel et al., 2020; Rothe et al., 2021) 사용.
## 4.1 Copy Baselines
- **Copy Source**: 원본 기사 생성.
- **Copy Source + Evidence**: 원본 기사 + 증거 조합. <br/>구조화되지 않지 않은 테이블의 텍스트 데이터를 변환하기 위해 전통적인 선형화 방법(Lebret et al., 2016; Wiseman et al., 2017)을 적용. 행과 열 구분자를 사용하여 테이블 항목 분리.

## 4.2 T5
- T5 Copy Source
- T5 + Copy Source + Evidence
- 두 실험 모두 비구조화된 테이블 항목에서 텍스트 데이터를 변환하기 위해 선형화 방법 적용

## 4.3 EDIT5
- 압축된 출력 형식을 사용하여 전체 업데이트를 처음부터 쓸 필요없다.
- Target 기사의 대부분의 텍스트는 원본 텍스트에서 복사되기 때문에 복사된 문장을 식별할 수 있는 토큰을 대체
- 모델이 입력에서 반복되는 시퀸스에 용량을 적게 할당할 수 있다.
- 업데이트된 문장이 적용된 증거 조각을 표시.(예. 업데이트 된 문장이 첫번째 증거 조각에 적용되었다면 (1)업데이트 문장)
- 모델이 업데이트된 문장을 생성하기 전에 증거 조각을 참조하여 계획하도록 학습.
- 참조 토큰들은 평가지표를 계산하기 전 모델의 출력 텍스트에서 제거.<br />
![image](https://github.com/in-sukim/NLP-Paper/assets/43094223/bc6e6da5-da5f-4cac-b8ba-c49cd2554566)<br/>

# 5. Results and Analysis
![image](https://github.com/in-sukim/NLP-Paper/assets/43094223/c2a2ae81-a87c-4577-96cd-42224c3a3a9b)<br/>
- Gold Dataset으로 평가된 결과
- Copy Source 방법 보다 Evidence를 함께 입력해주는 것이 더 좋은 성능
- Baseline model T5보다 EDIT5모델이 전체적으로 더 좋은 성능
- Unsupported Entity Tokens이 더 적은 것으로 보아 hallucination 현상이 더 적은 것을 의미.<br/>

![image](https://github.com/in-sukim/NLP-Paper/assets/43094223/d7d3a524-1feb-4911-ad09-c49989d4c74e)<br/>
- 잘못된 날짜를 반영한 모습<br/>
![image](https://github.com/in-sukim/NLP-Paper/assets/43094223/bbf26961-4c77-4618-b382-464fe446a990)<br/>
- EDIT5의 오류 유형을 파악하기 위해 Gold, Silver Dataset에서 100개의 무작위 예측
- 숫자와 날짜, hallucination, 증거 왜곡의 유형으로 발생.<br/>
![image](https://github.com/in-sukim/NLP-Paper/assets/43094223/76d523b6-3e8e-4a74-979d-7704b306772c)<br/>
- 추가적인 제어로 모델의 성능을 개선할 수 있는 가능성이 있다.
- Keskar et al. (2019) and Narayan et al. (2021)의 연구에 따라 special token을 이용한 상세한 instruction을 입력으로 추가.
- 모델에게 문장 추가,복사,편집,제거할 것인지 추가나 편집 시 어떤 증거를 사용할 것인지 지시
- 모든 지표에서 10% 정도의 성능 향상

