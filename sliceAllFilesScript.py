import os
import subprocess

# Путь к папке с исходными TIFF-файлами
input_dir = r"/u/product/temperatura/aqua/monthly_avg_year/day"

# Путь к папке для хранения выходных тайлов
output_dir = r"/u/product/temperatura/tiles/aqua/monthly_avg_year/day"

# Путь к gdal2tiles.py conda env
gdal2tiles_path = r"/usr/bin/gdal2tiles.py"

# Диапазон уровней масштабирования
zoom_levels = "8-12"

# файл переведенный в 8битный формат 
temp_vrt = "temp.vrt"

# Проверяем, что выходная папка существует, или создаём её
os.makedirs(output_dir, exist_ok=True)

# Проходим по всем файлам в папке
for filename in os.listdir(input_dir):
    if filename.lower().endswith(".tif"):
        input_path = os.path.join(input_dir, filename)
        
        # Генерация папки для текущего файла
        tile_output_dir = os.path.join(output_dir, os.path.splitext(filename)[0])
        
        # Проверяем, существует ли уже папка с тайлами и содержит ли файлы
        if os.path.exists(tile_output_dir) and os.listdir(tile_output_dir):
            print(f"Skipping {filename} - tiles already exist in {tile_output_dir}")
            continue
            
        os.makedirs(tile_output_dir, exist_ok=True)
        
        print(f"Processing file: {input_path}")

        try:
            # Команда 1: gdal_translate
            translate_command = [
                "gdal_translate",
                "-of", "VRT",
                "-ot", "Byte",
                "-scale",
                input_path,
                temp_vrt
            ]
            subprocess.run(translate_command, check=True)
            print("Step 1: gdal_translate completed.")

            # Команда 2: gdal2tiles.py
            tiles_command = [
                "python3", gdal2tiles_path,
                "-z", zoom_levels,
                "-w", "openlayers",
                temp_vrt,
                tile_output_dir
            ]
            subprocess.run(tiles_command, check=True)
            print("Step 2: gdal2tiles.py completed.")

        except subprocess.CalledProcessError as e:
            print(f"Error processing file {input_path}: {e}")

        finally:
            # Команда 3: Удаление временного файла temp.vrt
            if os.path.exists(temp_vrt):
                os.remove(temp_vrt)
                print("Step 3: temp.vrt deleted.")

        print(f"Finished processing: {filename}")