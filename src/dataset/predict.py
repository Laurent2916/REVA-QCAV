import pathlib

import datasets

dataset_path = pathlib.Path("./dataset_predict/")

_VERSION = "2.0.2"

_DESCRIPTION = ""

_HOMEPAGE = ""

_LICENSE = ""

_NAMES = [
    "Matte",
    "Shiny",
    "Chrome",
]


class SpherePredict(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            version=_VERSION,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            features=datasets.Features(
                {
                    "image_id": datasets.Value("int64"),
                    "image": datasets.Image(),
                    "objects": [
                        {
                            "category_id": datasets.ClassLabel(names=_NAMES),
                            "image_id": datasets.Value("int64"),
                            "id": datasets.Value("string"),
                            "area": datasets.Value("float32"),
                            "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
                            "iscrowd": datasets.Value("bool"),
                        }
                    ],
                }
            ),
        )

    def _split_generators(self, dl_manager):
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "dataset_path": dataset_path,
                },
            )
        ]

    def _generate_examples(self, dataset_path: pathlib.Path):
        """Generate images and labels for splits."""
        # create png iterator
        jpgs = dataset_path.rglob("*.jpg")

        for index, jpg in enumerate(jpgs):
            print(index, jpg, 2)

            # generate data
            data = {
                "image_id": index,
                "image": str(jpg),
                "objects": [],
            }

            yield index, data


if __name__ == "__main__":
    # load dataset
    dataset = datasets.load_dataset("src/spheres_predict.py", split="train")

    labels = dataset.features["objects"][0]["category_id"].names
    id2label = {k: v for k, v in enumerate(labels)}
    label2id = {v: k for k, v in enumerate(labels)}

    print(f"labels: {labels}")
    print(f"id2label: {id2label}")
    print(f"label2id: {label2id}")
    print()

    for idx in range(10):
        image = dataset[idx]["image"]

        print(f"image path: {image.filename}")
        print(f"data: {dataset[idx]}")

        # save image
        image.save(f"example_predict_{idx}.jpg")
