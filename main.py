import cv2
import numpy as np
import os

# Direktori utama yang dipakai pada struktur folder saat ini
ORIGINAL_DIR = "images/original"
GRAYSCALE_DIR = "images/grayscale"
NOISY_DIR = "images/noisy"
FILTERED_DIR = "filtered"
MSE_DIR = "mse_results"

# Konfigurasi noise dan filter
SALT_PAPPER_LEVELS = {"low": 0.02, "high": 0.10}
GAUSSIAN_LEVELS = {"low": 10, "high": 25}
FILTERS = ("min", "max", "median", "mean")
WINDOW_SIZE = 3  # ukuran jendela filter


def to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def add_salt_and_pepper(img, prob):
    noisy = img.copy()
    rand_matrix = np.random.rand(*img.shape[:2])
    salt_mask = rand_matrix < prob / 2
    pepper_mask = (rand_matrix >= prob / 2) & (rand_matrix < prob)

    if img.ndim == 2:
        noisy[salt_mask] = 255
        noisy[pepper_mask] = 0
    else:
        noisy[salt_mask] = 255
        noisy[pepper_mask] = 0

    return noisy


def add_gaussian(img, sigma):
    noise = np.random.normal(0, sigma, img.shape)
    noisy = img.astype(np.float32) + noise
    noisy = np.clip(noisy, 0, 255)
    return noisy.astype(np.uint8)


def _filter_channel(channel, window, mode):
    if window < 1 or window % 2 == 0:
        raise ValueError("Window harus bernilai ganjil dan lebih dari 0")

    pad = window // 2
    padded = np.pad(channel, pad_width=pad, mode="constant", constant_values=0)
    # Buat view 4D berisi semua window
    windows = np.lib.stride_tricks.sliding_window_view(padded, (window, window))

    if mode == "min":
        return windows.min(axis=(-1, -2)).astype(np.uint8)
    if mode == "max":
        return windows.max(axis=(-1, -2)).astype(np.uint8)
    if mode == "median":
        return np.median(windows, axis=(-1, -2)).astype(np.uint8)
    # mean
    return windows.mean(axis=(-1, -2)).astype(np.uint8)


def apply_filter(img, window, mode="mean"):
    mode = mode.lower()
    if img.ndim == 2:
        return _filter_channel(img, window, mode)

    channels = []
    for c in range(img.shape[2]):
        channel = _filter_channel(img[:, :, c], window, mode)
        channels.append(channel)
    return np.stack(channels, axis=2)


def mse(img1, img2):
    diff = img1.astype(np.float32) - img2.astype(np.float32)
    return float(np.mean(diff ** 2))


def ensure_directories():
    os.makedirs(GRAYSCALE_DIR, exist_ok=True)
    os.makedirs(NOISY_DIR, exist_ok=True)
    os.makedirs(FILTERED_DIR, exist_ok=True)
    os.makedirs(MSE_DIR, exist_ok=True)


def reset_logs(log_files):
    for path in log_files.values():
        open(path, "w").close()


def save_filtered_versions(
    noisy_img,
    reference,
    base,
    ext,
    noise_type,
    level,
    color_mode,
    filtered_dir,
    log_files,
):
    for flt in FILTERS:
        filtered_img = apply_filter(noisy_img, window=WINDOW_SIZE, mode=flt)
        filename = f"{base}_{color_mode}_{noise_type}_{level}_{flt}{ext}"
        cv2.imwrite(os.path.join(filtered_dir, flt, filename), filtered_img)

        error = mse(reference, filtered_img)
        line = f"{filename} -> MSE = {error}\n"
        with open(log_files["all"], "a") as out:
            out.write(line)
        with open(log_files[noise_type], "a") as out:
            out.write(line)


def process():
    ensure_directories()

    log_files = {
        "all": os.path.join(MSE_DIR, "mse_results.txt"),
        "gaussian": os.path.join(MSE_DIR, "mse_gaussian.txt"),
        "saltpapper": os.path.join(MSE_DIR, "mse_saltpapper.txt"),
    }
    reset_logs(log_files)

    valid_ext = (".jpg", ".jpeg", ".png")
    files = [f for f in os.listdir(ORIGINAL_DIR) if f.lower().endswith(valid_ext)]
    files.sort()

    # Sesuaikan instruksi: hanya butuh 2 citra warna (mis. landscape & potrait).
    # Jika lebih dari 2 ada di folder, sisanya diabaikan.
    files = files[:2]

    print(f"Ditemukan {len(files)} citra untuk diproses.")

    for f in files:
        color_img = cv2.imread(os.path.join(ORIGINAL_DIR, f))
        if color_img is None:
            continue

        base, ext = os.path.splitext(f)
        print(f"\nMemproses: {base}")

        # Buat subfolder per citra supaya hasil tidak menumpuk di satu folder
        gray_dir = os.path.join(GRAYSCALE_DIR, base)
        noisy_dir = os.path.join(NOISY_DIR, base)
        filtered_dir = os.path.join(FILTERED_DIR, base)

        os.makedirs(gray_dir, exist_ok=True)
        os.makedirs(noisy_dir, exist_ok=True)
        os.makedirs(filtered_dir, exist_ok=True)
        for flt in FILTERS:
            os.makedirs(os.path.join(filtered_dir, flt), exist_ok=True)

        # Buat subfolder noise (saltpapper/gaussian + level)
        noise_subdirs = {}
        for noise_type, levels in (
            ("saltpapper", SALT_PAPPER_LEVELS.keys()),
            ("gaussian", GAUSSIAN_LEVELS.keys()),
        ):
            for level in levels:
                path = os.path.join(noisy_dir, noise_type, level)
                os.makedirs(path, exist_ok=True)
                noise_subdirs[(noise_type, level)] = path

        gray_img = to_grayscale(color_img)
        gray_name = f"{base}_gray{ext}"
        cv2.imwrite(os.path.join(gray_dir, gray_name), gray_img)
        print(f"  -> Grayscale disimpan: {os.path.join(gray_dir, gray_name)}")

        for level, prob in SALT_PAPPER_LEVELS.items():
            noisy_gray = add_salt_and_pepper(gray_img, prob)
            noisy_color = add_salt_and_pepper(color_img, prob)
            print(f"  -> Noise saltpapper {level} (warna & gray) dibuat")

            cv2.imwrite(
                os.path.join(
                    noise_subdirs[("saltpapper", level)],
                    f"{base}_gray_saltpapper_{level}{ext}",
                ),
                noisy_gray,
            )
            cv2.imwrite(
                os.path.join(
                    noise_subdirs[("saltpapper", level)],
                    f"{base}_color_saltpapper_{level}{ext}",
                ),
                noisy_color,
            )

            save_filtered_versions(
                noisy_gray,
                gray_img,
                base,
                ext,
                noise_type="saltpapper",
                level=level,
                color_mode="gray",
                filtered_dir=filtered_dir,
                log_files=log_files,
            )
            save_filtered_versions(
                noisy_color,
                color_img,
                base,
                ext,
                noise_type="saltpapper",
                level=level,
                color_mode="color",
                filtered_dir=filtered_dir,
                log_files=log_files,
            )

        for level, sigma in GAUSSIAN_LEVELS.items():
            noisy_gray = add_gaussian(gray_img, sigma)
            noisy_color = add_gaussian(color_img, sigma)
            print(f"  -> Noise gaussian {level} (warna & gray) dibuat")

            cv2.imwrite(
                os.path.join(
                    noise_subdirs[("gaussian", level)],
                    f"{base}_gray_gaussian_{level}{ext}",
                ),
                noisy_gray,
            )
            cv2.imwrite(
                os.path.join(
                    noise_subdirs[("gaussian", level)],
                    f"{base}_color_gaussian_{level}{ext}",
                ),
                noisy_color,
            )

            save_filtered_versions(
                noisy_gray,
                gray_img,
                base,
                ext,
                noise_type="gaussian",
                level=level,
                color_mode="gray",
                filtered_dir=filtered_dir,
                log_files=log_files,
            )
            save_filtered_versions(
                noisy_color,
                color_img,
                base,
                ext,
                noise_type="gaussian",
                level=level,
                color_mode="color",
                filtered_dir=filtered_dir,
                log_files=log_files,
            )

    print("Selesai memproses semua citra.")


if __name__ == "__main__":
    process()
