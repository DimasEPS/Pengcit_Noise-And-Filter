## Tugas Pengolahan Citra Noise & Filter

Skrip ini memproses 2 citra warna (landscape dan potrait), membuat versi grayscale, menambahkan derau (salt & pepper dan Gaussian) pada dua level, lalu menghilangkan derau dengan filter manual (min, max, median, mean) dan menghitung MSE.

### Struktur input/output
- Input citra: `images/original/landscape.jpg` dan `images/original/potrait.jpg` (hanya 2 pertama yang dipakai).
- Grayscale: `images/grayscale/<nama_citra>/`.
- Citra noisy: `images/noisy/<nama_citra>/<jenis_noise>/<level>/` (saltpapper/gaussian × low/high).
- Hasil filter: `filtered/<nama_citra>/<filter>/` (min/max/median/mean).
- Log MSE: `mse_results/mse_results.txt`, `mse_results/mse_gaussian.txt`, `mse_results/mse_saltpapper.txt`.

### Menjalankan
1) Clone repo dan masuk ke folder:
```
git clone <repo-url>
cd pengcit  # atau nama folder repo
```
2) (Opsional) Buat dan aktifkan virtualenv:
```
python -m venv venv
source venv/bin/activate
```
3) Pasang dependensi:
```
pip install opencv-python numpy
```
4) Jalankan:
```
python main.py
```
Hasil akan tertulis di folder output di atas dan log MSE terisi otomatis.

Membersihkan hasil tanpa menghapus subfolder:
```
find images/grayscale images/noisy filtered mse_results -type f -delete
```

### Alur program
1) Memuat 2 citra warna pertama di `images/original` (diasumsikan landscape dan potrait).
2) Membuat versi grayscale untuk masing-masing citra.
3) Menambahkan noise:
   - Salt & pepper level `low=0.02`, `high=0.10`.
   - Gaussian level `low=10`, `high=25`.
   - Dilakukan untuk citra warna dan grayscale.
4) Menghilangkan noise dengan filter manual (tanpa fungsi bawaan) min, max, median, mean menggunakan jendela 3×3 (dipercepat dengan `sliding_window_view` NumPy).
5) Menyimpan hasil filter ke subfolder per citra dan menulis MSE terhadap citra asli (warna dibandingkan warna, grayscale dibandingkan grayscale) ke file log.

Konfigurasi level noise dan ukuran jendela dapat diubah di bagian konstanta `SALT_PAPPER_LEVELS`, `GAUSSIAN_LEVELS`, dan `WINDOW_SIZE` pada `main.py`.
