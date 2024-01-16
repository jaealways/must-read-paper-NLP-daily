---
layout: post
title:  "[TLDR] Scaling Data-Constrained Language Models
"
author: jaealways
categories: [ paper, NLP]
tags: [TLDR, NeurIPS'23, LLM, Scaling ]
---


# [TLDR] Scaling Data-Constrained Language Models



[reference: Niklas Muennighoff et al, "Scaling Data-Constrained Language Models", 2023](https://arxiv.org/pdf/2305.16264.pdf)


# Abstract

- 요즘 언어모델은 파라미터와 훈련 데이터셋 사이즈를 모두 증가시키지만, 곧 인터넷 상에서 사용가능한 데이터는 한계에 도달
- 본 논문에선 데이터 제약 조건에서 scaling하는 방법을 조사함
- 4 에폭정도까지는 데이터 반복도 새 데이터 학습 정도의 가치가 있음
- 데이터 반복을 하면 모델의 크기를 줄이고, 학습 토큰을 늘리는 것이 더 optimal


# 1 Introduction

- 최근 LLM은 더 작은 모델 사이즈로 많은 데이터를 넣으면 좋은 성능을 보일 수 있음
- 하지만, 작은 사이즈의 모델을 좀 더 큰 사이즈로 확장시키려면, 현실적인 데이터 부족에 직면

- 본 논문에선 데이터 제약 상황에서 모델을 스케일링하는 방법에 대해 고민함
- 최근 Galactica 모델을 제외하고 대부분의 LLM은 한 번의 에폭만을 사용했기 때문에, compute vs additional data collection의 trade-off를 비교하기 어려움
- 본 논문에선 10M ~ 9B개의 파라미터를 가진 400개의 모델을 최대 1500 에폭까지 학습시켜서 mulitple epoch의 효과를 수치화하려 함
- 이 때 모델이 4에폭을 돌 때까지는, 새로운 데이터를 추가하는 것과 큰 차이가 나지 않음을 발견함
- 또한, 새로운 자연어 데이터를 추가하지 않아도 정확도를 높일 수 있는 방법에 대해 고민함
    - 코드 토큰 통합하고 데이터 필터링 완화하기



# 2 Background

- 훈련 리소스를 결정하기 위해서, LLM의 scaling behavior를 예측하는 것은 매우 중요함
    - Allocation: 최적의 리소스 균형은?
    - Return: 추가 자원의 기대치는?
- LLM을 확장할 땐 FLOPS를 통해 자원을 계산함
- 본 논문에서 자주 언급되는 Chinchilla(대표적인 epoch을 통한 경량화 모델)는 scaling prediction을 위해 세 가지 방법을 사용
    - FIxed Parameters: 모델 사이즈 고정
    - Fixed FLOPs: 연산량 고정
    - Parametric Fit: 손실 공식 도출
- 이를 통해 compute-optimal training을 위해선 $$ \alpha ≈ \beta $$이고, N(파라미터 수)과 D(훈련 토큰 수)가 비례적으로 확장해야 함

# 3 Method: Data-Constrained Scaling Laws

- 


## 3.1 Parametric Fit

# 4 Experimental Setup

# 5 Results: Resource Allocation for Data-Constrained Scaling


# 6 Results: Resource Return for Data-Constrained Scaling

# 7 Results: Complementary Strategies for Obtaining Additional Data


# 8 Related Work

# 9 Conclusion

