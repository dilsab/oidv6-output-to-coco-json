import json
import datetime
import os
import argparse
from PIL import Image


def get_args():
    parser = argparse.ArgumentParser('OIDv6 output to COCO JSON - dilsab')
    parser.add_argument('--classes', type=str, nargs='+', default=[], required=True,
                        help='Sequence of class names separated by space')
    parser.add_argument('--datasets_directory', type=str, required=True, help='Path to datasets directory')
    parser.add_argument('--dataset_directory_names', type=str, nargs='+', default=[], required=True,
                        help='Sequence of dataset directory names inside --datasets_directory separated by space e.g. '
                             'train test')
    parser.add_argument('--custom_filenames', type=str, nargs='+', default=[],
                        help='Sequence of filenames separated by space. Specify filenames in the same order as '
                             '--dataset_directory_names. Default naming instances_dataset-directory-name.json')
    parser.add_argument('--labels_directory_name', type=str, default='labels',
                        help='Labels directory name inside image dataset directory (provided by '
                             '`--dataset_directory_names`)')
    parser.add_argument('--save_directory', type=str, default='annotations',
                        help='Directory where JSON files will be saved')
    parser.add_argument('--indent', action='store_true', help='Indent JSON (4 spaces)')
    args = parser.parse_args()

    return args


def get_image_date_captured(image_exif):
    # 36867 - TIFF Tag DateTimeOriginal
    # 36868 - TIFF Tag DateTimeDigitized
    # 306 - TIFF Tag DateTime
    return image_exif.get(36867) or image_exif.get(36868) or image_exif.get(306) or None


def collect_images_annotations_data(obj_name_list, images_dir, labels_dir_name):
    images_data = []
    annotations_data = []
    image_id = 0
    annotation_id = 0
    for filename in os.listdir(images_dir):
        if filename.endswith('.jpg'):
            with Image.open(os.path.join(images_dir, filename)) as image:
                image_size = image.size
                images_data.append({
                    'id': image_id,
                    'file_name': filename,
                    'width': image_size[1],
                    'height': image_size[0],
                    'date_captured': get_image_date_captured(image.getexif()),
                    'licence': 1,
                    'coco_url': '',
                    'flickr_url': '',
                })
            with open(os.path.join(images_dir, labels_dir_name, filename.rsplit('.', 1)[0] + '.txt')) as labels_file:
                for label in labels_file:
                    obj_class_name, xmin, ymin, xmax, ymax = label.split()
                    xmin = int(float(xmin))
                    ymin = int(float(ymin))
                    xmax = int(float(xmax))
                    ymax = int(float(ymax))
                    width = xmax - xmin
                    height = ymax - ymin
                    annotations_data.append({
                        'id': annotation_id,
                        'image_id': image_id,
                        'category_id': obj_name_list.index(obj_class_name) + 1,
                        'iscrowd': 0,
                        'bbox': [
                            xmin,
                            ymin,
                            width,
                            height,
                        ],
                        'segmentation': []
                    })
                    annotation_id += 1
            image_id += 1

    return images_data, annotations_data


def get_categories_data(obj_name_list):
    categories = []
    for idx, obj_name in enumerate(obj_name_list):
        categories.append({
            'id': idx + 1,
            'name': obj_name,
            'supercategory': 'None',
        })

    return categories


def get_base_licenses_data():
    return [
        {
            'id': 1,
            'name': None,
            'url': None,
        },
    ]


def get_base_info_data():
    datetime_now = datetime.datetime.now()

    return {
        'description': '',
        'url': '',
        'version': '',
        'year': datetime_now.year,
        'contributor': '',
        'data_created': datetime_now.strftime('%Y-%m-%d'),
    }


def should_use_custom_filenames(custom_filenames, dataset_directory_names):
    use_custom_filenames = False
    if len(custom_filenames) == len(dataset_directory_names):
        use_custom_filenames = True
    elif len(custom_filenames) > 0:
        print('Provided custom_filenames and dataset_directory_names argument amounts do not match. Using default names')

    return use_custom_filenames


def to_coco_data(options):
    dataset_dir_index = 0
    classes = options.classes
    datasets_directory = options.datasets_directory
    save_directory = options.save_directory
    custom_filenames = options.custom_filenames
    dataset_directory_names = options.dataset_directory_names

    use_custom_filenames = should_use_custom_filenames(custom_filenames, dataset_directory_names)

    for idx, dir_name in enumerate(dataset_directory_names):
        coco_data = {
            'info': get_base_info_data(),
            'licenses': get_base_licenses_data(),
            'categories': get_categories_data(classes),
        }
        images_data, annotations_data = collect_images_annotations_data(
            classes,
            os.path.join(datasets_directory, dir_name),
            options.labels_directory_name
        )
        coco_data['images'] = images_data
        coco_data['annotations'] = annotations_data

        if not os.path.isdir(save_directory):
            os.makedirs(save_directory)
            print(f'Created directory {os.path.join(os.getcwd(), save_directory)}')

        filename = custom_filenames[idx] if use_custom_filenames else f'instances_{dir_name}.json'
        absolute_file_path = os.path.join(os.getcwd(), options.save_directory, filename)
        with open(absolute_file_path, 'w') as file:
            json.dump(coco_data, file, indent=4) if options.indent else json.dump(coco_data, file)
            print(f'Created file {absolute_file_path}')

        dataset_dir_index += 1


if __name__ == '__main__':
    to_coco_data(get_args())
