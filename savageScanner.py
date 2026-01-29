import requests
import time
import argparse
import warnings
import os
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
from tqdm import tqdm

def check_link(url, verify_ssl=True):
    try:
        response = requests.head(url, allow_redirects=True, verify=verify_ssl)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def create_output_directory(domain, current_time):
    """Create results directory structure: results/domain-timestamp/"""
    output_dir = os.path.join("results", f"{domain}-{current_time}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def create_link_list_file(domain, current_time, output_dir):
    filename = os.path.join(output_dir, f"{domain}_link_list_{current_time}.txt")
    with open(filename, "w") as file:
        file.write("Link List:\n")
    return filename

def append_link_to_file(url, filename):
    with open(filename, "a") as file:
        file.write(url + "\n")

def process_links(file_path, base_url, passive=False, delay=2, verify_ssl=True):
    with open(file_path, "r") as file:
        lines = file.readlines()

    domain = base_url.split("//")[-1].split("/")[0]
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create organized output directory
    output_dir = create_output_directory(domain, current_time)
    filename = create_link_list_file(domain, current_time, output_dir)

    counter = 0
    pbar = None
    try:
        pbar = tqdm(total=len(lines), desc="Progress")
        for line in lines:
            line = line.strip()
            if line:
                if line.startswith("http://") or line.startswith("https://"):
                    url = line
                else:
                    url = f"https://{domain}{line}"
                if check_link(url, verify_ssl):
                    #print(f"Valid URL: {url}")
                    append_link_to_file(url, filename)
                    counter += 1
                if passive:
                    time.sleep(delay)
                pbar.update(1)
    except KeyboardInterrupt:
        print(f"\nUser stopped scan. {counter} results found and saved to {filename}")
    finally:
        if pbar is not None:
            pbar.close()

    print(f"Scan finished. {counter} results found and saved to {filename}")
    print(f"Output directory: {output_dir}")

# Example usage
if __name__ == "__main__":
    print("Starting scanner...")

    # Ignore InsecureRequestWarning
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)

    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="Path to the input file")
    parser.add_argument("base_url", help="Base URL to append the lines")
    parser.add_argument("--passive", type=float, help="Enable passive mode with a specified delay in seconds")
    parser.add_argument("--verifyssl", action="store_false", help="Disable SSL verification (not recommended in production)")
    args = parser.parse_args()

    if args.passive:
        process_links(args.file_path, args.base_url, passive=True, delay=args.passive, verify_ssl=args.verifyssl)
    else:
        process_links(args.file_path, args.base_url, verify_ssl=args.verifyssl)