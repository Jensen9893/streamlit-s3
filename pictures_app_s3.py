import streamlit as st
import boto3
from botocore.exceptions import ClientError
from PIL import Image

# AWS S3 credentials
AWS_ACCESS_KEY = 'AKIAY3CGZFDXYJKOJRAM'
AWS_SECRET_KEY = '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'
BUCKET_NAME = 'streamlitbucket-datnh30'

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

# Function to upload image to S3
def upload_to_s3(file, filename):
    try:
        s3.upload_fileobj(file, BUCKET_NAME, filename)
        return True
    except ClientError as e:
        st.error(f"Error uploading file: {e}")
        return False

# Function to get image from S3
def get_from_s3(filename):
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
        return Image.open(obj['Body'])
    except ClientError as e:
        st.error(f"Error getting file: {e}")
        return None

# Function to delete image from S3
def delete_from_s3(filename):
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return True
    except ClientError as e:
        st.error(f"Error deleting file: {e}")
        return False

# Streamlit UI
st.title('Image Storage with AWS S3')

# Upload image to S3
uploaded_file = st.file_uploader("Upload Image")

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    if st.button('Save Image'):
        if upload_to_s3(uploaded_file, uploaded_file.name):
            st.success("Image saved successfully!")

# Display image from S3
filename = st.text_input("Enter Image Filename:")
if filename:
    retrieved_image = get_from_s3(filename)
    if retrieved_image:
        st.image(retrieved_image, caption='Retrieved Image', use_column_width=True)
        if st.button('Delete Image'):
            if delete_from_s3(filename):
                st.success("Image deleted successfully!")

