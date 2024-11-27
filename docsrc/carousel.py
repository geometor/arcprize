import os
from pathlib import Path

def create_carousel_index(directory='.'):
    """
    Creates an index.rst file with a carousel containing all images in the specified directory.
    
    Args:
        directory (str): Directory path to scan for images. Defaults to current directory.
    """
    # List of common image extensions to include
    IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg'}
    
    # Get all image files in the directory
    image_files = []
    for ext in IMAGE_EXTENSIONS:
        image_files.extend(Path(directory).glob(f'*{ext}'))
    
    # Sort files to ensure consistent ordering
    image_files.sort()
    
    if not image_files:
        print("No image files found in the specified directory.")
        return
    
    # Create the RST content
    rst_content = [
        "Image Gallery",
        "============",
        "",
        ".. carousel::",
        "    :show_controls:",
        ""
    ]
    
    # Add each image to the carousel
    for image_file in image_files:
        rst_content.extend([
            f"    .. image:: {image_file.name}",
            "        :alt: {image_file.stem}",
            ""
        ])
    
    # Write the RST file
    output_path = Path(directory) / 'index.rst'
    try:
        with open(output_path, 'w') as f:
            f.write('\n'.join(rst_content))
        print(f"Successfully created carousel index at: {output_path}")
        print(f"Added {len(image_files)} images to the carousel")
    except Exception as e:
        print(f"Error writing index.rst: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Create an RST carousel index for images in a directory.')
    parser.add_argument('--dir', '-d', default='.',
                       help='Directory containing images (default: current directory)')
    
    args = parser.parse_args()
    create_carousel_index(args.dir)
