import cloudinary
from cloudinary.uploader import upload
import os
from dotenv import load_dotenv
from fastapi import UploadFile, HTTPException

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

async def upload_image(image: UploadFile):
    try:
        upload_result = upload(image.file,folder="ecomart")
        file_url = upload_result['secure_url']
        return file_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading images: {e}")
