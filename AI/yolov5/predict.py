import torch
model = torch.hub.load('ultralytics/yolov5', 'custom', 'test.pt')  # custom trained model

# Images
im = 'data/images/mia/1/raw/012.jpg'  # or file, Path, URL, PIL, OpenCV, numpy, list

# Inference
results = model(im)

# Results
results.show()  # or .show(), .save(), .crop(), .pandas(), etc.

print(results.pandas().xyxy[0])  # im predictions (tensor)
#      xmin    ymin    xmax   ymax  confidence  class    name
# 0  749.50   43.50  1148.0  704.5    0.874023      0  person
# 2  114.75  195.75  1095.0  708.0    0.624512      0  person
# 3  986.00  304.00  1028.0  420.0    0.286865     27     tie