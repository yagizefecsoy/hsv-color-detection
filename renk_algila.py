# =============================================================================
# GÖKBÖRÜ - TEKNOFEST 2026 - Akıllı Fabrika Sistemleri Programlama
# Görev 3 - HSV ile Renk Algılama (renk_algila.py)
# -----------------------------------------------------------------------------
# Açıklama:
# Bu program, kameradan alınan canlı görüntüde kırmızı, yeşil ve mavi renklerini
# HSV renk uzayında algılar. Tespit edilen renk kamera penceresinde etiket olarak
# ve terminal ekranında RED / GREEN / BLUE şeklinde gösterilir.
# =============================================================================

# OpenCV kütüphanesini içe aktarıyoruz.
# Kamera ve görüntü işleme işlemlerini gerçekleştirmemizi sağlar.
import cv2


# Renk algılama için gerekli minimum beyaz piksel sayısını tanımlıyoruz.
PIKSEL_ESIGI = 5000

# Kamera görüntüsüne yazılacak etiketin yazı ayarlarını tanımlıyoruz.
YAZI_FONTU = cv2.FONT_HERSHEY_SIMPLEX
YAZI_BOYUTU = 1.8
YAZI_KALINLIGI = 4
DIS_CIZGI_KALINLIGI = 8


# etiket_yaz fonksiyonu, algılanan rengin adını kamera görüntüsüne yazar.
# Siyah dış çizgi sayesinde etiketin her arka planda belirgin görünmesini sağlar.
def etiket_yaz(goruntu, metin, konum, renk):
    cv2.putText(
        goruntu,
        metin,
        konum,
        YAZI_FONTU,
        YAZI_BOYUTU,
        (0, 0, 0),
        DIS_CIZGI_KALINLIGI,
        cv2.LINE_AA
    )

    cv2.putText(
        goruntu,
        metin,
        konum,
        YAZI_FONTU,
        YAZI_BOYUTU,
        renk,
        YAZI_KALINLIGI,
        cv2.LINE_AA
    )


# main fonksiyonu, kamera görüntüsünü alır, renk maskelerini oluşturur
# ve algılama sonuçlarını kamera penceresi ile terminalde gösterir.
def main():
    # Bilgisayarın varsayılan kamerasını açıyoruz.
    kamera = cv2.VideoCapture(0)

    # Kamera açılamadıysa programı sonlandırıyoruz.
    if not kamera.isOpened():
        print("[HATA] Kamera açılamadı.")
        return

    print("[INFO] Kamera açıldı. Çıkmak için Q tuşuna basın.")

    # Kırmızı rengin iki ayrı HSV aralığını tanımlıyoruz.
    # Kırmızı, HSV Hue skalasının hem başında hem sonunda bulunduğu için iki aralık kullanılır.
    # Kırmızı rengin birinci HSV aralığı.
    alt_kirmizi_1 = (0, 180, 100)
    ust_kirmizi_1 = (10, 255, 255)

    # Kırmızı rengin ikinci HSV aralığı.
    alt_kirmizi_2 = (170, 180, 100)
    ust_kirmizi_2 = (179, 255, 255)

    # Yeşil rengin HSV aralığını tanımlıyoruz.
    alt_yesil = (30, 70, 40)
    ust_yesil = (86, 255, 255)

    # Mavi rengin HSV aralığını tanımlıyoruz.
    alt_mavi = (88, 150, 100)
    ust_mavi = (140, 255, 255)

    # Bir önceki karede algılanan renkleri saklıyoruz.
    # Böylece aynı renk terminale sürekli yazdırılmaz.
    onceki_renkler = set()

    while True:
        # Kameradan bir görüntü karesi alıyoruz.
        basarili, goruntu = kamera.read()

        # Görüntü alınamadıysa kamera döngüsünü sonlandırıyoruz.
        if not basarili:
            print("[HATA] Kameradan görüntü alınamadı.")
            break

        # Kameradan gelen BGR görüntüyü HSV renk uzayına dönüştürüyoruz.
        hsv = cv2.cvtColor(goruntu, cv2.COLOR_BGR2HSV)

        # Kırmızı rengin iki HSV aralığı için ayrı maskeler oluşturuyoruz.
        kirmizi_maske_1 = cv2.inRange(
            hsv,
            alt_kirmizi_1,
            ust_kirmizi_1
        )

        kirmizi_maske_2 = cv2.inRange(
            hsv,
            alt_kirmizi_2,
            ust_kirmizi_2
        )

        # Kırmızının iki ayrı maskesini tek maskede birleştiriyoruz.
        kirmizi_maske = cv2.bitwise_or(
            kirmizi_maske_1,
            kirmizi_maske_2
        )

        # Yeşil ve mavi renk maskelerini oluşturuyoruz.
        yesil_maske = cv2.inRange(
            hsv,
            alt_yesil,
            ust_yesil
        )

        mavi_maske = cv2.inRange(
            hsv,
            alt_mavi,
            ust_mavi
        )

        # Her renk maskesindeki beyaz piksel sayısını hesaplıyoruz.
        kirmizi_piksel_sayisi = cv2.countNonZero(kirmizi_maske)
        yesil_piksel_sayisi = cv2.countNonZero(yesil_maske)
        mavi_piksel_sayisi = cv2.countNonZero(mavi_maske)

        # Mevcut kamera karesinde algılanan renkleri saklıyoruz.
        algilanan_renkler = set()

        if kirmizi_piksel_sayisi > PIKSEL_ESIGI:
            algilanan_renkler.add("RED")

        if yesil_piksel_sayisi > PIKSEL_ESIGI:
            algilanan_renkler.add("GREEN")

        if mavi_piksel_sayisi > PIKSEL_ESIGI:
            algilanan_renkler.add("BLUE")

        # Önceki karede bulunmayan yeni renkleri belirliyoruz.
        # Yeni algılanan renkleri terminale yalnızca bir kez yazdırıyoruz.
        yeni_renkler = algilanan_renkler - onceki_renkler

        for renk_adi in ("RED", "GREEN", "BLUE"):
            if renk_adi in yeni_renkler:
                print(renk_adi)

        # Algılanan renk etiketlerini kamera görüntüsüne alt alta yazdırıyoruz.
        y_konumu = 75

        if "RED" in algilanan_renkler:
            etiket_yaz(
                goruntu,
                "RED",
                (30, y_konumu),
                (0, 0, 255)
            )
            y_konumu += 75

        if "GREEN" in algilanan_renkler:
            etiket_yaz(
                goruntu,
                "GREEN",
                (30, y_konumu),
                (0, 255, 0)
            )
            y_konumu += 75

        if "BLUE" in algilanan_renkler:
            etiket_yaz(
                goruntu,
                "BLUE",
                (30, y_konumu),
                (255, 0, 0)
            )

        # Mevcut renkleri bir sonraki kamera karesi için kaydediyoruz.
        onceki_renkler = algilanan_renkler.copy()

        # Kamera görüntüsünü ve renk maskelerini ayrı pencerelerde gösteriyoruz.
        cv2.imshow("Kamera", goruntu)
        cv2.imshow("Kirmizi Maske", kirmizi_maske)
        cv2.imshow("Yesil Maske", yesil_maske)
        cv2.imshow("Mavi Maske", mavi_maske)

        # Q tuşuna basıldığında programı sonlandırıyoruz.
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Kamera kaynağını serbest bırakıyor ve açık pencereleri kapatıyoruz.
    kamera.release()
    cv2.destroyAllWindows()

    print("[INFO] Program sonlandırıldı.")

    son_renk = None
    mevcut_renk = None

    if kirmizi_piksel_sayisi > PIKSEL_ESIGI:
        mevcut_renk = "RED"
    elif yesil_piksel_sayisi > PIKSEL_ESIGI:
        mevcut_renk = "GREEN"
    elif mavi_piksel_sayisi > PIKSEL_ESIGI:
        mevcut_renk = "BLUE"

    if mevcut_renk is not None and mevcut_renk != son_renk:
        print(mevcut_renk)

    son_renk = mevcut_renk

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    kirmizi_maske = cv2.morphologyEx(
        kirmizi_maske,
        cv2.MORPH_OPEN,
        kernel
    )

    yesil_maske = cv2.morphologyEx(
        yesil_maske,
        cv2.MORPH_OPEN,
        kernel
    )

    mavi_maske = cv2.morphologyEx(
        mavi_maske,
        cv2.MORPH_OPEN,
        kernel
    )

# Dosya doğrudan çalıştırıldığında main fonksiyonunu başlatıyoruz.
if __name__ == "__main__":
    main()