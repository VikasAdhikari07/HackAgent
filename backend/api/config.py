import os

model = os.getenv("IMAGE_GENERATION_MODEL")
response_modalities = ["TEXT", "IMAGE"]
save_dir = "generated_images"
image_format = "PNG"
return_base64 = False

