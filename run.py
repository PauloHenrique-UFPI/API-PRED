import cv2
import torch
import numpy as np
import albumentations as A
from effdet import create_model
from albumentations.pytorch import ToTensorV2

BACKBONE = 'tf_efficientdet_d4'
MODEL_PATH = 'model.pth'
INPUT_SIZE = (512, 512)


def format_predictions(preds):
    return {"boxes": preds[:, :4], "scores": preds[:, 4], "labels": preds[:, 5]}


def init_model(model_path: str = MODEL_PATH):
    model = create_model(BACKBONE, bench_task='predict', num_classes=1, image_size=INPUT_SIZE, bench_labeler=True, pretrained=False)
    #model_weight = torch.load(model_path, map_location={'cuda:3': 'cuda:0'})
    model_weight = torch.load(model_path, map_location=torch.device('cpu'))
    model.load_state_dict(model_weight)
    model.eval()
    torch.cuda.empty_cache()
    return model


def init_transform(input_size: tuple = INPUT_SIZE):
    return A.Compose(
        [
            A.Resize(*input_size),
            ToTensorV2()
        ])


def run_model(model, image):
    with torch.no_grad():
        prediction = model(image)
        pred = format_predictions(prediction[0])

    return pred['boxes'][pred['scores'] >= 0.3]


def load_image(image_path: str = ''):
    return cv2.imread(image_path, cv2.IMREAD_UNCHANGED)


def pre_processing_image(transform, image):
    return torch.div(transform(image=image)['image'][None, ...], 255)

class pred:
    def main(img):
        PATH_IMAGE = 'img/'+img
        image = load_image(PATH_IMAGE)
        r, c, _ = image.shape

        model = init_model()
        transform = init_transform()

        tensor_input = pre_processing_image(transform, image)

        for box in run_model(model, tensor_input):
            p1, p2, p3, p4 = np.int_((box.numpy() / INPUT_SIZE[0]) * (c, r, c, r))
            cv2.rectangle(image, (p1, p2), (p3, p4), (0, 0, 0), 2)
        cv2.imwrite('pred/predictions.png', image)
        return 'pred/predictions.png'
