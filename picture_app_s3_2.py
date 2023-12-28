import streamlit as st
import boto3
from io import BytesIO
from PIL import Image as PILImage

# AWS S3 Configuration
s3 = boto3.client('s3', region_name=AWS_DEFAULT_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
bucket_name = 'streamlitbucket-datnh30'

# Function to list images in S3 bucket
def list_images():
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        return [obj['Key'] for obj in response['Contents']]
    return []

# Function to display images from S3
def display_images():
    st.subheader("List of Images")
    images = list_images()
    for img_key in images:
        st.image(read_image_from_s3(img_key), width=200)

# Function to read image from S3
def read_image_from_s3(key):
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    img_data = obj['Body'].read()
    return PILImage.open(BytesIO(img_data))

# Main function
def main():
    st.title("CRUD Operations on Pictures using S3")

    menu = ["Add", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Select operation", menu)

    if choice == "Add":
        st.subheader("Add Pictures to S3")
        uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            file_name = uploaded_file.name
            s3.upload_fileobj(uploaded_file, bucket_name, file_name)
            st.success("Image uploaded successfully to S3!")

    elif choice == "Read":
        display_images()

    elif choice == "Update":
        st.subheader("Update Pictures in S3")
        images = list_images()
        selected_image = st.selectbox("Select Image to Update", images)
        updated_file = st.file_uploader("Upload New Image", type=['png', 'jpg', 'jpeg'])
        if updated_file is not None:
            s3.delete_object(Bucket=bucket_name, Key=selected_image)
            s3.upload_fileobj(updated_file, bucket_name, updated_file.name)
            st.success("Image updated successfully in S3!")

    elif choice == "Delete":
        st.subheader("Delete Pictures from S3")
        images = list_images()
        selected_image = st.selectbox("Select Image to Delete", images)
        if st.button("Delete"):
            s3.delete_object(Bucket=bucket_name, Key=selected_image)
            st.success("Image deleted successfully from S3!")

if __name__ == '__main__':
    main()
