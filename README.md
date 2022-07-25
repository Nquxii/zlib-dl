# zlib-dl
Python tool allowing easy books downloads from the terminal 

## Features 
- Bypass z-library's randomly generated links to downloads, which is a roadblock to downloads
- Obtain a specified number of results

## Installation
Clone the repository and install dependencies
```
git clone https://github.com/Nquxii/zlib-dl
cd zlib-dl
```
```
pip install -r requirements.txt
```

Open help section
```
python3 zldl --h
```
## Usage
```
python3 zldl --s [query] --n [number of results] --p [number of pages]
```
Number of results defaults to all results available, which may not be relevant, so it is recommended to use a small value for --n, like 5.

Number of pages is only necessary for larger searches (> 50 results) and is not recommended for usability purposes.
