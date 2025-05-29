# 📱 Non-Invasive Glucose Monitoring (NIGM) via Smartphone PPG

This project explores the feasibility of estimating blood glucose levels using smartphone-acquired photoplethysmography (PPG) signals and deep learning. It utilizes a CNN-GRU neural network to learn directly from raw PPG waveforms, with the long-term goal of building a non-invasive, accessible glucose monitoring system for diabetic and pre-diabetic individuals.

---

## 🧠 Overview

**Goal**: Predict blood glucose levels from raw PPG signals captured using a smartphone's camera and flash.

**Approach**:
- Use a CNN-GRU model to extract spatial and temporal features from 1D PPG signals.
- Avoid hand-crafted feature engineering to reduce bias and enhance generalizability.
- Apply subject-wise validation to realistically assess model performance and avoid data leakage.

---

## 🔍 Key Features

- 📈 **Deep Learning**: End-to-end learning with CNN-GRU model for time-series PPG signals.
- 🚫 **No Feature Engineering**: Direct use of raw waveform data.
- 🔄 **Subject-wise Validation**: Prevents overfitting and mimics real-world deployment.
- 📉 **Early Stopping & LR Scheduling**: Training optimization for stability and performance.

---

