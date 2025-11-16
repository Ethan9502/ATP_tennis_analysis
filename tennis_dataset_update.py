import kagglehub

# Download latest version
path = kagglehub.dataset_download("dissfya/atp-tennis-2000-2023daily-pull")

print("Path to dataset files:", path)