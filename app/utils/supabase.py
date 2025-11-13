import os
import tempfile

from typing import Any
from datetime import datetime

from uuid import uuid4

def upload_images_to_bucket(
    supabase_client,
    avatar,
    bucket_name,
) -> list[dict[str, Any]]:
    
    """Uploads image to a Supabase bucket."""
    
    # Create a path inside the bucket

    file_path = f"{uuid4()}"

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(avatar.read())
        tmp_path = tmp.name

    # Upload directly from memory (no need to save locally)
    supabase_client.storage.from_(bucket_name).upload(
        file=tmp_path,
        path=file_path,
        file_options={
            "cache-control": "3600",
            "upsert": "true",
            "content-type": avatar.content_type,
        },
    )

    os.remove(tmp_path)

    # Get public URL
    public_url = supabase_client.storage.from_(bucket_name).get_public_url(
        file_path
    )

    return public_url


def delete_images_from_bucket(supabase_client, bucket_name, supabase_url, current_avatar_url):

    # If there's a current avatar, delete in bucket
    if current_avatar_url:
        # Extract bucket path
        file_path = current_avatar_url.replace(f"{supabase_url}/storage/v1/object/public/{bucket_name}/", "")
        supabase_client.storage.from_(bucket_name).remove([file_path])
