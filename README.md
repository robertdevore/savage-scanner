# :smiling_imp: Savage Scanner

Provide a wordlist to perform bruteforce recon on a domain in order to find vulnerable URL's

![python](https://img.shields.io/badge/python-3.x-green.svg) ![license](https://img.shields.io/badge/License-GPLv3-brightgreen.svg)

Savage Scanner is a Python-based script designed to validate and collect URLs from an input file. 

It processes links by appending them to a base URL, checks their validity, and saves valid links to a timestamped output file. 

The python script includes features such as passive scanning with delays and SSL verification handling.

## Features

- **URL Validation**: Validates URLs by sending HTTP HEAD requests.
- **Flexible Input**: Supports input files containing relative or absolute URLs.
- **Passive Mode**: Adds a delay between requests to avoid overloading servers.
- **SSL Handling**: Optionally disable SSL verification for testing with self-signed certificates.
- **Output Management**: Saves valid links to a timestamped file.
- **Interactive Progress**: Displays a progress bar during scanning.

## Requirements

- Python 3.7+
- Required libraries:
    - `requests`
    - `tqdm`

Install the dependencies using pip:

```
pip install requests tqdm
```

## Usage

Run the script with the following arguments:

```
python3 savageScanner.py file_path base_url [--passive DELAY] [--verifyssl]
```

### Arguments

- `file_path` (required): Path to the input file containing URLs or relative paths.
- `base_url` (required): Base URL to prepend to relative paths in the input file.
- `--passive` (optional): Enables passive mode and specifies a delay (in seconds) between requests.
- `--verifyssl` (optional): Disables SSL certificate verification (not recommended for production).

### Example

#### Example Input File

`wordlist.txt`:

```
/page1
/page2
https://example.com/page3
```

#### Command

```
python3 savageScanner.py wordlist.txt https://example.com --passive 2 --verifyssl
```

#### Output

Results are organized in timestamped directories under `results/`:

```
results/
  └── example.com-2024-12-23_12-34-56/
      └── example.com_link_list_2024-12-23_12-34-56.txt
```

The output file contains:

```
Link List:
https://targetwebsite.com/page1
https://targetwebsite.com/page2
https://targetwebsite.com/page3
```

## How It Works

1. **Input Parsing**: Reads the input file line by line.
2. **URL Construction**: Appends the base URL to relative paths.
3. **Validation**: Sends an HTTP HEAD request to verify the URL.
4. **Output Organization**: Creates organized directory structure for results.
5. **Output**: Writes valid URLs to a timestamped file.
6. **Progress Display**: Uses `tqdm` to show scanning progress.
7. **Passive Mode**: Introduces a delay between requests if enabled.

## Code Structure

- `**check_link(url, verify_ssl)**`:
    - Sends an HTTP HEAD request to validate the URL.
    - Returns `True` if the status code is 200, otherwise `False`.
- `**create_output_directory(domain, current_time)**`:
    - Creates organized results directory structure.
- `**create_link_list_file(domain, current_time, output_dir)**`:
    - Creates a timestamped output file for storing valid links.
- `**append_link_to_file(url, filename)**`:
    - Appends a valid URL to the output file.
- `**process_links(file_path, base_url, passive, delay, verify_ssl)**`:
    - Processes the input file, constructs URLs, validates them, and writes valid ones to the output file.
    - Displays progress using `tqdm`.

## Notes

- Use the `--verifyssl` option with caution, as it disables SSL verification and can expose your system to potential risks.
- The script skips URLs that cannot be reached or produce errors during validation.
- The progress bar can be interrupted safely with `Ctrl+C`, and valid URLs found up to that point are saved.

## License

Savage Scanner is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests via the [GitHub repository](https://github.com/robertdevore/savage-scanner).