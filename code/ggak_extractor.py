import os
import argparse
from pathlib import Path

def extract_frames(input_file, frame_length, sync_word, output_dir):
    # Convert sync word from hex string to bytes
    sync_bytes = bytes.fromhex(sync_word)
    sync_length = len(sync_bytes)
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Dictionary to store file handles for each marker
    marker_files = {}
    
    try:
        with open(input_file, 'rb') as f:
            data = f.read()
            data_length = len(data)
            pos = 0
            frame_counter = 0
            
            while pos <= data_length - frame_length:
                # Check for sync word at current position
                if data[pos:pos+sync_length] == sync_bytes:
                    # Skip every second frame (thanks Ivan)
                    if frame_counter % 2 == 0:
                        # Extract the frame
                        frame = data[pos:pos+frame_length]
                        
                        # Sync word is 4 bytes (32 bits), marker is in the next 4 bits
                        marker_byte = frame[sync_length]  # Get the byte containing marker and sub-marker
                        marker = (marker_byte & 0xF0) >> 4  # Extract upper 4 bits
                        
                        # Write frame to separate marker file
                        if marker not in marker_files:
                            marker_file = os.path.join(output_dir, f"marker_{marker}.bin")
                            marker_files[marker] = open(marker_file, 'ab')
                        
                        marker_files[marker].write(frame)
                    
                    frame_counter += 1
                    # Move to next frame
                    pos += frame_length
                else:
                    # Sync word not found, move to next byte
                    pos += 1
                    
    finally:
        # Close all open files
        for file in marker_files.values():
            file.close()

def main():
    parser = argparse.ArgumentParser(description='Extract GGAK frames by marker ID. (applying Ivan\'s skip-every-second-frame trick)')
    parser.add_argument('input_file', help='Input "cadu" file')
    parser.add_argument('--frame_length', type=int, default=224, 
                       help='Frame length in bytes (default: 224)')
    parser.add_argument('--sync_word', default='1ACFFC1D', 
                       help='Sync word in hex (default: 1ACFFC1D)')
    parser.add_argument('--output_dir', default='extracted', 
                       help='Output directory (default: extracted)')
    
    args = parser.parse_args()
    
    print(f"Extracting frames from {args.input_file}")
    print(f"Frame length: {args.frame_length} bytes")
    print(f"Sync word: 0x{args.sync_word}")
    print(f"Output directory: {args.output_dir}")
    
    extract_frames(args.input_file, args.frame_length, args.sync_word, args.output_dir)
    
    print("Done, bye")

if __name__ == "__main__":
    main()

# example usage:
# python ggak_extractor.py elektro_ggak.cadu 