---
layout: post
title:  "[TLDR] Confident Learning: Estimating Uncertainty in Dataset Labels"
author: jaealways
categories: [ paper, data science]
tags: [TLDR, JAIR'21, ]
---


# [TLDR] Confident Learning: Estimating Uncertainty in Dataset Labels


[reference: Curtis G. Northcutt et al, "Confident Learning:
Estimating Uncertainty in Dataset Labels", 2021](https://arxiv.org/pdf/1911.00068.pdf)

# Abstract
- Confident Learning: prediction 보다 아래와 같은 방법으로 data centric한 접근을 하는 방법론
    - 노이즈 데이터 정리
    - 노이즈를 측정하기 위해 확률적 임계값으로 측정
    - confidence로 훈련시키기 위해 예제들을 ranking
- 본 논문에선 위의 가정들을 모두 조합해서, class-conditional noise process 만듦
    - noisy 라벨과 uncorrupted 라벨의 joint distribution을 측정함
- 

# 1. Introduction


# 2. CL Framework and Problem Set-up


# 3. CL Methods


## 3.1 Count: Characterize and Find Label Errors using the Confident Joint



## 3.2 Rank and Prune: Data Cleaning



# 4. Theory


## 4.1 Noiseless Predicted Probabilities



## 4.2 Noisy Predicted Probabilities




# 5. Experiments



## 5.1 Asymmetric Label Noise on CIFAR-10 dataset


## 5.2 Real-world Label Errors in ILSVRC12 ImageNet Train Dataset


## 5.3 Amazon Reviews Dataset: CL using logistic regression on noisy text data


## 5.4 Real-world Label Errors in Other Datasets


# 6. Related work


# 7. Conclusion and Future Work

