import os

# --- Configuration ---
# ⚠️ IMPORTANT: Set this to the folder where your images and .txt files are located.
SOURCE_DIR = r""

# Add any other image extensions you use (e.g., '.webp', '.tiff')
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg'] 

# --- Script Logic ---
def rename_sidecar_files(source_directory, extensions):
    """
    Renames text files from 'image.txt' to 'image.ext.txt' for Hydrus sidecar compatibility.
    """
    print(f"Starting file scan in: {source_directory}")
    
    # Store all files that exist in the directory for quick lookup
    all_files = os.listdir(source_directory)
    
    # Counter for renamed files
    renamed_count = 0

    for filename in all_files:
        # 1. Look for the ComfyUI-generated tag files
        if filename.endswith(".txt"):
            
            # The base name is the filename without the ".txt" extension
            name_base = filename[:-4]
            original_txt_path = os.path.join(source_directory, filename)

            # 2. Check for a corresponding image file with a known extension
            found_extension = None
            for ext in extensions:
                image_filename = name_base + ext
                if image_filename in all_files:
                    found_extension = ext
                    break

            # 3. Perform the rename if a matching image is found
            if found_extension:
                
                # Create the new sidecar filename (e.g., 'image.png.txt')
                new_filename = name_base + found_extension + ".txt"
                new_txt_path = os.path.join(source_directory, new_filename)

                try:
                    os.rename(original_txt_path, new_txt_path)
                    print(f"Renamed: '{filename}' to '{new_filename}'")
                    renamed_count += 1
                except Exception as e:
                    print(f"Error renaming {filename}: {e}")
            else:
                # This happens if a .txt file is found, but the corresponding image is missing or has an unknown extension.
                print(f"Skipping: '{filename}' - No matching image file found.")

    print("\n--- Summary ---")
    print(f"Total files renamed: {renamed_count}")
    print("Files are ready for import into Hydrus Network.")

# Execute the function
if __name__ == "__main__":

    rename_sidecar_files(SOURCE_DIR, IMAGE_EXTENSIONS)
