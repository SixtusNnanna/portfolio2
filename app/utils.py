# utils/upload.py  (or wherever your upload function is)

import os
from typing import Optional
from datetime import datetime, timezone
from urllib.parse import urlparse

from fastapi import UploadFile
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url


class CloudinaryUploader:
    # Configuration
    cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )

    # Upload an image
    @staticmethod
    async def upload_image(file: Optional[UploadFile], project_id: str):
        if file:
            public_id = f"projects/{project_id}"
            upload_result = cloudinary.uploader.upload(
                file.file,
                resource_type="raw",
                public_id=public_id,
            )
            print(upload_result)
            return upload_result["secure_url"]

    # Optimize delivery by resizing and applying auto-format and auto-quality
    @staticmethod
    async def fetch_optimized_file(file_public_id):
        optimize_url, _ = cloudinary_url(
            file_public_id, fetch_format="auto", quality="auto"
        )
        print(optimize_url)
        return optimize_url

    # Transform the image: auto-crop to square aspect_ratio
    @staticmethod
    async def transform_image(file_url):
        auto_crop_url, _ = cloudinary_url(
            file_url, width=500, height=500, crop="auto", gravity="auto"
        )
        print(auto_crop_url)
        return auto_crop_url

    @staticmethod
    def generate_public_id(filename: str):
        no_space_string = filename.replace(" ", "")
        split_no_space_string = no_space_string.split(".")
        no_space_string_name = "".join(
            split_no_space_string[: len(split_no_space_string) - 1]
        )
        current_datetime = datetime.now(timezone.utc)
        datetime_str = current_datetime.strftime("%Y%m%d%H%M%S")
        result_string = no_space_string_name + datetime_str
        return result_string
    
    # Delete image by public_id
    @staticmethod
    async def delete_file(public_id: str):
        try:
            result = cloudinary.uploader.destroy(public_id)
            print(f"Cloudinary deletion result: {result}")
            return result
        except Exception as e:
            print(f"Error deleting from Cloudinary: {e}")
            raise

    # Extract public_id from secure_url
    @staticmethod
    def extract_public_id(file_url: str) -> str:
        path = urlparse(file_url).path  # e.g., /demo/image/upload/v1234567890/folder/filename.jpg
        parts = path.split("/")

        if "upload" in parts:
            upload_index = parts.index("upload")
            rest = parts[upload_index + 1:]

            # Skip version part if it starts with "v" followed by digits
            if rest and rest[0].startswith("v") and rest[0][1:].isdigit():
                rest = rest[1:]

            public_id_with_ext = "/".join(rest)
        else:
            public_id_with_ext = parts[-1]

        public_id, _ = os.path.splitext(public_id_with_ext)
        return public_id



media_manager = CloudinaryUploader()

