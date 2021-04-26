# OIDv6 output to COCO JSON

Generate [COCO JSON (Object Detection)](https://cocodataset.org/#format-data) from [OIDv6](https://github.com/DmitryRyumin/OIDv6) 
or [OIDv4_ToolKit](https://github.com/EscVM/OIDv4_ToolKit) output.

As of April 21, 2021, this project works with [OIDv6](https://github.com/DmitryRyumin/OIDv6) 
and [OIDv4_ToolKit](https://github.com/EscVM/OIDv4_ToolKit).

### OIDv6
Download datasets using [OIDv6's](https://github.com/DmitryRyumin/OIDv6) `--multi_classes` argument.

### OIDv4_ToolKit
Download datasets using [OIDv4_ToolKit's](https://github.com/EscVM/OIDv4_ToolKit) `--multiclasses` argument.\
Provide `--labels_directory_name Label` when generating JSON using this project.

## Important note
This project generates base data for `info` and `licenses` keys as well as each image's `license` key.\
I make no warranties or representations regarding the license status of each image you will use and you should verify the license for each image yourself.

### Area
Area is calculated from bounding box not from segmentation. This is needed for a few specific projects.

## Installation

Clone repository
```shell
git clone https://github.com/dilsab/oidv6-output-to-coco-json.git
```
Install requirements
```shell
pipenv install
```

## Required packages

| Package | Minimum version | Used version |
| ------- | --------------- | ------------ |
| Pillow  | 6.2.1 | 8.2.0 |

## Usage

### Command line arguments

| Argument | Required | Type | Description |
| -------- | ---  | -------- | ------------------- |
| --classes | Yes | str | Sequence of class names separated by space |
| --datasets_directory | Yes | str | Path to datasets directory |
| --dataset_directory_names | Yes | str | Sequence of dataset directory names inside `--datasets_directory` separated by space e.g. `train test` |
| --custom_filenames | No | str | Sequence of filenames separated by space. Specify filenames in the same order as `--dataset_directory_names`. Default naming `instances_dataset-directory-name.json` |
| --labels_directory_name | No | str | Labels directory name inside image dataset directory (provided by `--dataset_directory_names`). Default `labels` |
| --save_directory | No | str | Directory where JSON files will be saved. Default `annotations` |
| --indent | No | No value argument | Indent JSON (4 spaces) |

Activate Pipenv shell
```shell
pipenv shell
```
Run command
```shell
python main.py <arguments>
```

## Examples

### Output

Output examples are inside `examples` directory.

`instances_train_indent.json` and `instances_validation_indent.json` generated using command
```shell
python main.py --classes apple lemon orange --datasets_directory datasets --dataset_directory_names train validation --custom_filenames instances_train_indent.json instances_validation_indent.json --save_directory examples --indent
```

`instances_train.json` and `instances_validation.json` generated using command
```shell
python main.py --classes apple lemon orange --datasets_directory datasets --dataset_directory_names train validation --save_directory examples
```

### File structure

```text
\---datasets
    +---train
    |   |   img0.jpg
    |   |   img1.jpg
    |   |   img2.jpg
    |   |   img3.jpg
    |   |   img4.jpg
    |   |   img5.jpg
    |   |   img6.jpg
    |   |   img7.jpg
    |   |   img8.jpg
    |   |
    |   \---labels
    |           img0.txt
    |           img1.txt
    |           img2.txt
    |           img3.txt
    |           img4.txt
    |           img5.txt
    |           img6.txt
    |           img7.txt
    |           img8.txt
    |
    \---validation
        |   img0.jpg
        |   img1.jpg
        |   img2.jpg
        |   img3.jpg
        |   img4.jpg
        |   img5.jpg
        |
        \---labels
                img0.txt
                img1.txt
                img2.txt
                img3.txt
                img4.txt
                img5.txt
```

### Label file

Example label file data (class xmin ymin xmax ymax)

```text
apple 230.1 322.5 357.3 414.4
apple 433.8 354.1 561.2 416.9
apple 603.6 401.8 761.12 566.5
```
