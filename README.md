## Tugas Pengolahan Citra Noise & Filter

Skrip ini memproses 2 citra warna (landscape dan potrait), membuat versi grayscale, menambahkan derau (salt & pepper dan Gaussian) pada dua level, lalu menghilangkan derau dengan filter manual (min, max, median, mean) dan menghitung MSE.

### Struktur input/output
- Input citra: `images/original/landscape.jpg` dan `images/original/potrait.jpg`.
- Grayscale: `images/grayscale/<nama_citra>/`.
- Citra noisy: `images/noisy/<nama_citra>/<jenis_noise>/<level>/`.
- Hasil filter: `filtered/<nama_citra>/<filter>/`.
- Log MSE: `mse_results/mse_results.txt`, `mse_results/mse_gaussian.txt`, `mse_results/mse_saltpapper.txt`.

### Menjalankan
1) Clone repo dan masuk ke folder:
```
git clone <repo-url>
cd repo-name
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

### Alur program
1) Memuat 2 citra warna pertama di `images/original` (diasumsikan landscape dan potrait).
2) Membuat versi grayscale untuk masing-masing citra.
3) Menambahkan noise:
   - Salt & pepper level `low=0.02`, `high=0.10`.
   - Gaussian level `low=10`, `high=25`.
   - Dilakukan untuk citra warna dan grayscale.
4) Menghilangkan noise dengan filter manual (tanpa fungsi bawaan) min, max, median, mean menggunakan jendela 3×3.
5) Menyimpan hasil filter ke subfolder per citra dan menulis MSE terhadap citra asli (warna dibandingkan warna, grayscale dibandingkan grayscale) ke file log.

Konfigurasi level noise dan ukuran jendela dapat diubah di bagian konstanta `SALT_PAPPER_LEVELS`, `GAUSSIAN_LEVELS`, dan `WINDOW_SIZE` pada `main.py`.
