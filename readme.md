---
title: Bike Sharing Demand Predictor
emoji: 🚲
colorFrom: green
colorTo: tiffany
sdk: streamlit
app_file: app.py
pinned: false
---


# 🚲 Bike Sharing Demand Predictor (Bisiklet Kiralama Talep Tahmini)

Bu proje, yapısal zaman ve hava durumu verilerini analiz ederek, akıllı bir şehir içi bisiklet paylaşım sisteminde **saatlik kiralama yoğunluğunu (talep sayısını)** tahmin etmek amacıyla geliştirilmiştir.

---

## 📊 Proje Özeti & Metrikler

* **Problem Türü:** Regresyon (Regression)
* **Hedef Değişken:** `cnt` (Saatlik toplam kiralama sayısı)
* **Değerlendirme Metriği:** **RMSLE (Root Mean Squared Logarithmic Error)**
  * *Akademik Not:* Talep verilerindeki büyük dalgalanmaların ve uç değerlerin (outliers) cezalandırma etkisini minimize etmek adına model logaritmik dönüşüm ($np.log1p$) ile eğitilmiş, performans RMSLE ile optimize edilmiştir.

---

## 🛠️ Uygulanan Mühendislik Adımları

1. **Özellik Mühendisliği (Feature Engineering):** Ham tarih verilerinden `yr` (yıl), `mnth` (ay), `day` (gün) ve `dayofweek` (haftanın günü) öznitelikleri türetilerek zaman serisi trendleri yakalanmıştır.
2. **Normalizasyon & Ölçekleme:** Sıcaklık (`temp`), hissedilen sıcaklık (`atemp`), nem (`hum`) ve rüzgar hızı (`windspeed`) gibi sürekli değişkenler model kararlılığı için normalize edilmiştir.
3. **Algoritma:** Skikit-Learn `RandomForestRegressor` mimarisi kullanılarak, aşırı öğrenmeyi (overfitting) engelleyen `max_depth` ve `n_estimators` hiperparametre optimizasyonları yapılmıştır.

---

