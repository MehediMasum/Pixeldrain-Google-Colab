import requests
import subprocess
import json
import time
import os

# Function to download a file from a URL with real-time progress
def download_file(url, file_name):
    """
    Download a file from a specified URL and save it locally with real-time download progress.

    Parameters:
    url (str): The URL to download the file from.
    file_name (str): The local file name to save the downloaded file as.
    """
    print(f"Starting download from: {url}")

    # Start the timer for download speed calculation
    start_time = time.time()

    # Stream the download process to monitor progress
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))  # Get total file size

    if response.status_code == 200 and total_size > 0:
        with open(file_name, 'wb') as file:
            downloaded_size = 0
            for data in response.iter_content(chunk_size=8192):
                file.write(data)
                downloaded_size += len(data)

                # Calculate download progress and speed in MB/s
                progress = (downloaded_size / total_size) * 100
                download_speed = downloaded_size / (1024 * 1024) / (time.time() - start_time)  # Speed in MB/s

                # Real-time progress print
                print(f"\rDownload Progress: {progress:.2f}% | Speed: {download_speed:.2f} MB/s", end="")

        # End time for final download speed
        end_time = time.time()
        total_duration = end_time - start_time
        final_speed = total_size / (1024 * 1024) / total_duration

        print(f"\nDownload complete! File saved as: {file_name}")
        print(f"Total Size: {total_size / (1024 * 1024):.2f} MB")
        print(f"Total Duration: {total_duration:.2f} seconds")
        print(f"Average Download Speed: {final_speed:.2f} MB/s")
    else:
        print(f"\nFailed to download file.\nStatus Code: {response.status_code}\nResponse: {response.text}")

# Function to upload a file to PixelDrain using cURL with real-time progress
def upload_to_pixeldrain(file_name, api_key):
    """
    Upload a file to PixelDrain using cURL with real-time upload progress.

    Parameters:
    file_name (str): The local file name to upload.
    api_key (str): The PixelDrain API key for authentication.
    """
    file_size = os.path.getsize(file_name)  # Get file size in bytes
    print(f"\nInitiating file upload...\nFile: {file_name}\nFile Size: {file_size / (1024 * 1024):.2f} MB")
    print(f"Using API Key: {api_key[:5]}... (hidden for security)")

    # Start the timer for upload duration calculation
    start_time = time.time()

    # Prepare the cURL command for uploading the file
    curl_command = f'curl -T "{file_name}" -u :{api_key} https://pixeldrain.com/api/file/ -#'

    # Execute the cURL command with real-time progress tracking
    try:
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
        end_time = time.time()  # End time for upload duration calculation

        upload_duration = end_time - start_time
        upload_speed = file_size / (1024 * 1024) / upload_duration  # Speed in MB/s

        if result.returncode == 0:
            response_data = result.stdout.strip()

            print(f"\nFile uploaded successfully!")
            print(f"Upload Duration: {upload_duration:.2f} seconds")
            print(f"Average Upload Speed: {upload_speed:.2f} MB/s")

            # Parse and display important information from the response
            try:
                response_json = json.loads(response_data)
                file_id = response_json.get("id", "N/A")
                file_name = response_json.get("name", "N/A")
                file_size = response_json.get("size", "N/A")
                upload_date = response_json.get("date_upload", "N/A")
                download_url = f"https://pixeldrain.com/api/file/{file_id}"

                print(f"File ID: {file_id}")
                print(f"File Name: {file_name}")
                print(f"File Size: {file_size / (1024 * 1024):.2f} MB")
                print(f"Upload Date: {upload_date}")
                print(f"Download URL: {download_url}")
            except json.JSONDecodeError as e:
                print(f"Failed to parse response JSON.\nError: {e}")
                print(f"Response Data: {response_data}")
        else:
            print("\nUpload failed.")
            print(f"Error Code: {result.returncode}")
            print(f"Error Message: {result.stderr}")
    except Exception as e:
        print(f"\nAn unexpected error occurred during upload:\n{e}")

# Main function to take user input and run the process
def main():
    # Get user input for the download link and file name
    download_url = input("Enter the download URL: ")
    file_name = input("Enter the file name to save the downloaded file as: ")

    # Step 1: Download the file
    download_file(download_url, file_name)

    # Step 2: Upload the file to PixelDrain
    api_key = input("Enter your PixelDrain API key: ")
    upload_to_pixeldrain(file_name, api_key)

# Run the main function
if __name__ == "__main__":
    main()
