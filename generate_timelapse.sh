folder_path="$1"

ffmpeg -framerate 60 -pattern_type glob -i "${folder_path}/*.jpg" -vf scale=720:-1 -c:v libx264 -pix_fmt yuv420p "${folder_path}/out.mp4" -y
