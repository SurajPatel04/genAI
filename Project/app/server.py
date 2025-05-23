from fastapi import FastAPI, UploadFile
from uuid import uuid4
from .utils.file import save_to_disk
from .db.collections.files import files_collection, FileSchema
app = FastAPI()

@app.get("/")
async def hello():
    return {"hello"}


@app.post("/upload")
async def file_upload(file: UploadFile):

    db_file = await files_collection.insert_one(
        document=FileSchema(
            name=file.filename,
            status="Saving"
        )
    )
    file_path=f"mnt/uploades/{str(db_file.inserted_id)}/{file.filename}"

    await save_to_disk(file=await file.read(), path=file_path)

    await files_collection.update_one({"_id": db_file.inserted_id},{
        "$set": {
            "status": "queued"
        }
    })
    return {"file_id": str(db_file.inserted_id)}



