import os
import xml.etree.ElementTree as ET

# Diretórios de entrada e saída
input_dir = "labels/validacao-xml"
output_dir = "labels/validacao"
classes = ['with-mask', 'without_mask', 'mask_weared_incorrect']  # Defina as classes aqui

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return (x * dw, y * dh, w * dw, h * dh)

def convert_annotation(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    label_path = os.path.join(output_dir, os.path.splitext(os.path.basename(xml_file))[0] + '.txt')
    with open(label_path, 'w') as out_file:
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bbox = convert((w, h), b)
            out_file.write(f"{cls_id} " + " ".join(f"{x:.6f}" for x in bbox) + '\n')

# Executa a conversão
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for xml_file in os.listdir(input_dir):
    if xml_file.endswith(".xml"):
        convert_annotation(os.path.join(input_dir, xml_file))

print("Conversão concluída!")
