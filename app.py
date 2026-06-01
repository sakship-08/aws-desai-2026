from flask import Flask, request, render_template
import boto3
import uuid

app = Flask(__name__)

s3 = boto3.client("s3")

BUCKET_NAME = "my-photo-upload-bucket-123"

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("photo")

        if file:
            filename = f"{uuid.uuid4()}_{file.filename}"

            s3.upload_fileobj(
                file,
                BUCKET_NAME,
                filename,
                ExtraArgs={"ContentType": file.content_type}
            )

            return f"File uploaded successfully: {filename}"

        return "No file selected"

    return render_template("upload.html")


if __name__ == "__main__":
    print("First line")
    app.run(host="0.0.0.0", port=5000)
