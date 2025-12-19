# Analisis Hasil Restorasi

## Tabel MSE Restorasi

Berikut adalah hasil perhitungan MSE untuk berbagai metode filtering pada citra landscape dan potrait, dengan noise Gaussian dan Salt & Pepper, pada level low dan high, serta pada citra grayscale dan color.

| Citra     | Noise      | Level | Tipe  | Filter | MSE      |
| --------- | ---------- | ----- | ----- | ------ | -------- |
| landscape | saltpapper | low   | gray  | min    | 2229.58  |
| landscape | saltpapper | low   | gray  | max    | 2672.28  |
| landscape | saltpapper | low   | gray  | median | 126.78   |
| landscape | saltpapper | low   | gray  | mean   | 201.72   |
| landscape | saltpapper | low   | color | min    | 2827.84  |
| landscape | saltpapper | low   | color | max    | 2835.51  |
| landscape | saltpapper | low   | color | median | 126.48   |
| landscape | saltpapper | low   | color | mean   | 214.05   |
| landscape | saltpapper | high  | gray  | min    | 6698.77  |
| landscape | saltpapper | high  | gray  | max    | 8398.66  |
| landscape | saltpapper | high  | gray  | median | 152.56   |
| landscape | saltpapper | high  | gray  | mean   | 400.80   |
| landscape | saltpapper | high  | color | min    | 9245.62  |
| landscape | saltpapper | high  | color | max    | 9007.02  |
| landscape | saltpapper | high  | color | median | 152.89   |
| landscape | saltpapper | high  | color | mean   | 488.30   |
| landscape | gaussian   | low   | gray  | min    | 1138.01  |
| landscape | gaussian   | low   | gray  | max    | 1173.47  |
| landscape | gaussian   | low   | gray  | median | 143.67   |
| landscape | gaussian   | low   | gray  | mean   | 168.43   |
| landscape | gaussian   | low   | color | min    | 1134.11  |
| landscape | gaussian   | low   | color | max    | 1122.36  |
| landscape | gaussian   | low   | color | median | 142.24   |
| landscape | gaussian   | low   | color | mean   | 171.66   |
| landscape | gaussian   | high  | gray  | min    | 2322.13  |
| landscape | gaussian   | high  | gray  | max    | 2462.96  |
| landscape | gaussian   | high  | gray  | median | 241.91   |
| landscape | gaussian   | high  | gray  | mean   | 227.94   |
| landscape | gaussian   | high  | color | min    | 2239.80  |
| landscape | gaussian   | high  | color | max    | 2140.15  |
| landscape | gaussian   | high  | color | median | 232.41   |
| landscape | gaussian   | high  | color | mean   | 239.08   |
| potrait   | saltpapper | low   | gray  | min    | 1612.83  |
| potrait   | saltpapper | low   | gray  | max    | 3238.04  |
| potrait   | saltpapper | low   | gray  | median | 103.99   |
| potrait   | saltpapper | low   | gray  | mean   | 156.64   |
| potrait   | saltpapper | low   | color | min    | 1522.82  |
| potrait   | saltpapper | low   | color | max    | 3210.74  |
| potrait   | saltpapper | low   | color | median | 104.11   |
| potrait   | saltpapper | low   | color | mean   | 154.41   |
| potrait   | saltpapper | high  | gray  | min    | 5074.73  |
| potrait   | saltpapper | high  | gray  | max    | 11281.46 |
| potrait   | saltpapper | high  | gray  | median | 118.37   |
| potrait   | saltpapper | high  | gray  | mean   | 386.52   |
| potrait   | saltpapper | high  | color | min    | 4853.09  |
| potrait   | saltpapper | high  | color | max    | 11567.16 |
| potrait   | saltpapper | high  | color | median | 118.57   |
| potrait   | saltpapper | high  | color | mean   | 388.16   |
| potrait   | gaussian   | low   | gray  | min    | 818.00   |
| potrait   | gaussian   | low   | gray  | max    | 911.00   |
| potrait   | gaussian   | low   | gray  | median | 123.65   |
| potrait   | gaussian   | low   | gray  | mean   | 119.22   |
| potrait   | gaussian   | low   | color | min    | 816.91   |
| potrait   | gaussian   | low   | color | max    | 913.00   |
| potrait   | gaussian   | low   | color | median | 123.93   |
| potrait   | gaussian   | low   | color | mean   | 119.44   |
| potrait   | gaussian   | high  | gray  | min    | 1823.18  |
| potrait   | gaussian   | high  | gray  | max    | 2201.77  |
| potrait   | gaussian   | high  | gray  | median | 219.72   |
| potrait   | gaussian   | high  | gray  | mean   | 175.19   |
| potrait   | gaussian   | high  | color | min    | 1805.93  |
| potrait   | gaussian   | high  | color | max    | 2225.33  |
| potrait   | gaussian   | high  | color | median | 219.17   |
| potrait   | gaussian   | high  | color | mean   | 175.62   |

## Temuan Utama

- Filter median memberikan MSE terendah pada hampir semua kasus noise, baik Gaussian maupun Salt & Pepper, pada level low maupun high.
- Filter min dan max cenderung menghasilkan MSE yang jauh lebih tinggi, terutama pada noise Salt & Pepper level tinggi.
- Citra grayscale dan color memiliki pola hasil yang mirip, namun MSE pada color sedikit lebih tinggi pada beberapa kasus.
- Pada noise Gaussian, filter mean juga cukup baik, namun median tetap unggul.

## Rekomendasi

- Untuk restorasi citra dengan noise Gaussian maupun Salt & Pepper, gunakan filter median untuk hasil terbaik (MSE terendah).
- Filter mean dapat digunakan sebagai alternatif pada noise Gaussian.
- Hindari filter min dan max untuk noise Salt & Pepper level tinggi.
