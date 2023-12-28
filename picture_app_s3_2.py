import streamlit as st
import boto3

# AWS S3 Configuration
aws_access_key_id = st.secrets["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
region_name = st.secrets["AWS_DEFAULT_REGION"]
bucket_name = st.secrets["BUCKET_NAME"]

# Initialize S3 client
s3 = boto3.client('s3', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Function to list image names in S3 bucket
def list_image_names():
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        return [obj['Key'] for obj in response['Contents']]
    return []

# Function to display images from S3 with names
def display_images_with_names():
    st.subheader("List of Images from S3 with Names")
    images = list_image_names()
    for img_key in images:
        img_name = img_key.split('/')[-1]
        st.write(f"Image Name: {img_name}")
        st.image(read_image_from_s3(img_key), caption=img_name, use_column_width=True)

# Function to read image from S3
def read_image_from_s3(key):
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    img_data = obj['Body'].read()
    return img_data

# Streamlit app function
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
        display_images_with_names()

    elif choice == "Update":
        st.subheader("Update Pictures in S3")
        images = list_image_names()
        selected_image = st.selectbox("Select Image to Update", images)
        updated_file = st.file_uploader("Upload New Image", type=['png', 'jpg', 'jpeg'])
        if updated_file is not None:
            s3.delete_object(Bucket=bucket_name, Key=selected_image)
            s3.upload_fileobj(updated_file, bucket_name, updated_file.name)
            st.success("Image updated successfully in S3!")

    elif choice == "Delete":
        st.subheader("Delete Pictures from S3")
        images = list_image_names()
        selected_image = st.selectbox("Select Image to Delete", images)
        if st.button("Delete"):
            s3.delete_object(Bucket=bucket_name, Key=selected_image)
            st.success("Image deleted successfully from S3!")

if __name__ == '__main__':
    main()
