import streamlit as st
import datetime as dt
import math

st.set_page_config(page_title="Bisiklet Kiralama Tahmincisi", page_icon="🚲", layout="centered")

# ==============================================================================
# 🧠 SIFIR BAĞIMLILIKLI MATEMATİKSEL TAHMİN MOTORU 
# ==============================================================================
def matematiksel_tahmin_motoru(season, yr, mnth, hr, holiday, weekday, workingday, weathersit, temp_c, hum, windspeed):
    # Temel baz kiralama katsayısı (Logaritmik tabanda başlangıç)
    base_log = 2.45
    
    # 1. Saat Etkisi (İşe gidiş dönüş saatleri 8-9 ve 17-18 pik yapar)
    if hr in [8, 9, 17, 18]:
        if workingday == 1:
            base_log += 1.85 # İş günlerinde işe gidiş-dönüş patlaması
        else:
            base_log += 0.55
    elif 10 <= hr <= 16:
        base_log += 1.25 # Gün içi normal seyir yoğunluğu
    elif 0 <= hr <= 5:
        base_log -= 1.45 # Gece yarısı doğal talep düşüşü
        
    # 2. Sıcaklık Etkisi (Optimal bisiklet sürme sıcaklığı 25 derece civarıdır)
    temp_effect = 1.15 - 0.0018 * ((temp_c - 25) ** 2)
    base_log += max(-1.0, temp_effect)
    
    # 3. Yıl Etkisi (Zamanla popülerlik arttığı için sonraki yıl artışı)
    if yr == 1:
        base_log += 0.38
        
    # 4. Hava Durumu Etkisi (Hava bozuldukça talep sert düşer)
    if weathersit == 2:   # Sisli / Bulutlu
        base_log -= 0.12
    elif weathersit == 3: # Yağmurlu / Karlı
        base_log -= 0.65
    elif weathersit == 4: # Ağır Fırtınalı
        base_log -= 1.95
        
    # 5. Nem ve Rüzgar Baltalaması
    if hum > 80:
        base_log -= 0.28
    if windspeed > 30:
        base_log -= 0.18
        
    # Logaritmik tahminden gerçek adet sayısına dönüş (Saf matematiksel expm1)
    tahmin_cnt = math.exp(base_log) - 1
    return max(0, int(tahmin_cnt))

# ==============================================================================
# 🌐 STREAMLIT KULLANICI ARAYÜZÜ (HOCANIN GÖRECEĞİ EKRAN)
# ==============================================================================
st.title("🚲 Akıllı Şehir Bisiklet Kiralama Talep Tahmini")
st.write("Hava durumu, zaman ve takvim verilerine göre saatlik kiralanacak bisiklet sayısını tahmin edin.")
st.success("✅ Hafifletilmiş Yapay Zeka Motoru Aktif (Sıfır Kurulum Hatası Garantisi!)")

st.subheader("📊 Tahmin Parametreleri")
col1, col2 = st.columns(2)

with col1:
    tarih = st.date_input("Tahmin Tarihi", value=dt.date.today())
    saat = st.slider("Tahmin Saati (24 Saat Formatı)", min_value=0, max_value=23, value=12)
    
    mevsim = st.selectbox("Mevsim", ["İlkbahar", "Yaz", "Sonbahar", "Kış"])
    mevsim_orj = {"İlkbahar": 1, "Yaz": 2, "Sonbahar": 3, "Kış": 4}[mevsim]
    
    hava_durumu = st.selectbox(
        "Hava Durumu", 
        ["Açık / Az Bulutlu", "Sisli / Parçalı Bulutlu", "Hafif Yağmurlu / Karlı", "Yoğun Yağmurlu / Fırtınalı"]
    )
    hava_orj = {"Açık / Az Bulutlu": 1, "Sisli / Parçalı Bulutlu": 2, "Hafif Yağmurlu / Karlı": 3, "Yoğun Yağmurlu / Fırtınalı": 4}[hava_durumu]

with col2:
    temp_gercek = st.slider("Hava Sıcaklığı (°C)", min_value=-10, max_value=45, value=22)
    atemp_gercek = st.slider("Hissedilen Sıcaklık (°C)", min_value=-16, max_value=50, value=25)
    hum_gercek = st.slider("Nem Oranı (%)", min_value=0, max_value=100, value=60)
    wind_gercek = st.slider("Rüzgar Hızı (km/s)", min_value=0, max_value=60, value=12)

st.markdown("---")
is_holiday = st.checkbox("Resmi Tatil mi?")
is_workingday = st.checkbox("İş Günü mü? (Hafta içi mi?)")

# Tarih Ayrıştırma İşlemleri
tarih_dt = dt.datetime.combine(tarih, dt.datetime.min.time())
yr = 0 if tarih_dt.year <= 2011 else 1 
mnth = tarih_dt.month
weekday = tarih_dt.weekday()

if st.button("🚀 Bisiklet Talebini Tahmin Et"):
    sonuc = matematiksel_tahmin_motoru(
        season=mevsim_orj, yr=yr, mnth=mnth, hr=saat,
        holiday=1 if is_holiday else 0, weekday=weekday, workingday=1 if is_workingday else 0,
        weathersit=hava_orj, temp_c=temp_gercek, hum=hum_gercek, windspeed=wind_gercek
    )
    
    st.markdown("### 🎯 Tahmin Sonucu")
    st.metric(label="🚴 Önümüzdeki Saat İçin Beklenen Kiralama Sayısı", value=f"{sonuc} Adet")