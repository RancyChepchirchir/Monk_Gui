import os
import sys
import json
import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class WindowObj7Yolov3Train(QtWidgets.QWidget):

    backward_hyper_param = QtCore.pyqtSignal();
    forward_7_yolov3 = QtCore.pyqtSignal(); 

    def __init__(self):
        super().__init__()
        self.title = 'Cornernet Lite - Train'
        self.left = 100
        self.top = 100
        self.width = 900
        self.height = 600
        self.load_cfg();
        self.initUI()

    def load_cfg(self):
        if(os.path.isfile("obj_7_yolov3.json")):
            with open('obj_7_yolov3.json') as json_file:
                self.system = json.load(json_file)


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height);



        # Backward
        self.b1 = QPushButton('Back', self)
        self.b1.move(700,550)
        self.b1.clicked.connect(self.backward)

        # Quit
        self.b2 = QPushButton('Quit', self)
        self.b2.move(800,550)
        self.b2.clicked.connect(self.close)


        self.tb1 = QTextEdit(self)
        self.tb1.move(20, 20)
        self.tb1.resize(400, 250)
        self.tb1.setText(self.get_params());
        self.tb1.setReadOnly(True)


        self.l1 = QLabel(self);
        self.l1.setText("Num Epochs: ");
        self.l1.move(20, 300);

        self.e1 = QLineEdit(self)
        self.e1.move(150, 300);
        self.e1.setText(self.system["epochs"]);
        self.e1.resize(200, 25);


        
        self.l3 = QLabel(self);
        self.l3.setText("Evolution generations: ");
        self.l3.move(20, 350);

        self.e3 = QLineEdit(self)
        self.e3.move(200, 350);
        self.e3.setText(self.system["num_generations"]);
        self.e3.resize(150, 25);

        if(self.system["evolve"] == "no"):
            self.e3.setEnabled(False);



        # Train
        self.b3 = QPushButton('Train', self)
        self.b3.move(20, 500)
        self.b3.clicked.connect(self.train)


        # Stop 
        self.b4 = QPushButton('Stop', self)
        self.b4.move(150, 500)
        self.b4.clicked.connect(self.stop)


        # Infer 
        self.b4 = QPushButton('Infer', self)
        self.b4.move(250, 500)
        self.b4.clicked.connect(self.forward)


        self.te1 = QTextBrowser(self);
        self.te1.move(450, 20);
        self.te1.setFixedSize(400, 500);


        self.l3 = QLabel(self);
        self.l3.setText("Status: ");
        self.l3.move(420, 550);

        self.tb2 = QTextEdit(self)
        self.tb2.move(470, 550)
        self.tb2.resize(200, 25)
        self.tb2.setText("Not Started");
        self.tb2.setReadOnly(True)


        self.process = QtCore.QProcess(self)
        self.process.readyReadStandardOutput.connect(self.stdoutReady)
        self.process.readyReadStandardError.connect(self.stderrReady)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)





    def get_params(self):
        wr = "";
        wr += "Anno Type -  {}\n".format(self.system["anno_type"]);
        if(self.system["anno_type"] == "monk"):
            wr += "Root Dir -   {}\n".format(self.system["monk_root_dir"]);
        elif(self.system["anno_type"] == "voc"):
            wr += "Root Dir -   {}\n".format(self.system["voc_root_dir"]);
        elif(self.system["anno_type"] == "coco"):
            wr += "Root Dir -   {}\n".format(self.system["coco_root_dir"]);
        else:
            wr += "Root Dir -   {}\n".format(self.system["yolo_root_dir"]);

        if(self.system["anno_type"] == "monk"):
            wr += "Anno Dir -   {}\n".format(self.system["monk_anno_file"]);
        elif(self.system["anno_type"] == "voc"):
            wr += "Anno File -  {}\n".format(self.system["voc_anno_dir"]);
        elif(self.system["anno_type"] == "coco"):
            wr += "Coco Dir -   {}\n".format(self.system["coco_coco_dir"]);
        else:
            wr += "Anno Dir -   {}\n".format(self.system["yolo_anno_dir"]);

        if(self.system["anno_type"] == "monk"):
            wr += "Img Dir -    {}\n".format(self.system["monk_img_dir"]);
        elif(self.system["anno_type"] == "voc"):
            wr += "Img Dir -    {}\n".format(self.system["voc_img_dir"]);
        elif(self.system["anno_type"] == "coco"):
            wr += "Img Dir -    {}\n".format(self.system["coco_img_dir"]);
        else:
            wr += "Img Dir -    {}\n".format(self.system["yolo_img_dir"]);
            wr += "Classes list file- {}\n".format(self.system["yolo_classes_file"]);

        if(self.system["val_data"] == "yes"):
            if(self.system["val_anno_type"] == "monk"):
                wr += "Root Dir -   {}\n".format(self.system["val_monk_root_dir"]);
            elif(self.system["val_anno_type"] == "voc"):
                wr += "Root Dir -   {}\n".format(self.system["val_voc_root_dir"]);
            elif(self.system["val_anno_type"] == "coco"):
                wr += "Root Dir -   {}\n".format(self.system["val_coco_root_dir"]);
            else:
                wr += "Root Dir -   {}\n".format(self.system["val_yolo_root_dir"]);

            if(self.system["val_anno_type"] == "monk"):
                wr += "Anno Dir -   {}\n".format(self.system["val_monk_anno_file"]);
            elif(self.system["val_anno_type"] == "voc"):
                wr += "Anno File -  {}\n".format(self.system["val_voc_anno_dir"]);
            elif(self.system["val_anno_type"] == "coco"):
                wr += "Coco Dir -   {}\n".format(self.system["val_coco_coco_dir"]);
            else:
                wr += "Anno Dir -   {}\n".format(self.system["val_yolo_anno_dir"]);

            if(self.system["val_anno_type"] == "monk"):
                wr += "Img Dir -    {}\n".format(self.system["val_monk_img_dir"]);
            elif(self.system["val_anno_type"] == "voc"):
                wr += "Img Dir -    {}\n".format(self.system["val_voc_img_dir"]);
            elif(self.system["val_anno_type"] == "coco"):
                wr += "Img Dir -    {}\n".format(self.system["val_coco_img_dir"]);
            else:
                wr += "Img Dir -    {}\n".format(self.system["val_yolo_img_dir"]);
                wr += "Classes list file- {}\n".format(self.system["val_yolo_classes_file"]);


        wr += "Batch size - {}\n".format(self.system["batch_size"]);
        wr += "Model - {}\n".format(self.system["model"]);
        
        wr += "Devices - {}\n".format(self.system["devices"]);
        wr += "Optimizer - {}\n".format(self.system["optimizer"]);
        wr += "Multi Scale - {}\n".format(self.system["multi_scale"]);
        wr += "Evolve - {}\n".format(self.system["evolve"]);
        wr += "Mixed Precision - {}\n".format(self.system["mixed_precision"]);
        wr += "Img Size - {}\n".format(self.system["img_size"]);
        wr += "Cache Images - {}\n".format(self.system["cache_images"]);
        wr += "Learning rate  - {}\n".format(self.system["lr"]);
        return wr;




    def train(self):
        self.te1.setText("");
        self.tb2.setText("Running");
        self.system["epochs"] = self.e1.text();
        self.system["num_generations"] = self.e3.text();

        with open('obj_7_yolov3.json', 'w') as outfile:
            json.dump(self.system, outfile);

        os.system("cp cfg/detection/object_detection/obj_7_yolov3/train_obj_7_yolov3.py .");
        os.system("cp cfg/detection/object_detection/obj_7_yolov3/train_obj_7_yolov3.sh .");


        self.process.start('bash', ['train_obj_7_yolov3.sh'])
        self.append("Process PID: " + str(self.process.pid()) + "\n");


    def stop(self):
        self.tb2.setText("Interrupted");
        QMessageBox.about(self, "Training Status", "Interrupted");
        self.process.kill();
        self.append("Training Stopped\n")


    def stdoutReady(self):
        text = str(self.process.readAllStandardOutput().data(), encoding='utf-8')
        if("Completed" in text):
            QMessageBox.about(self, "Training Status", "Completed");
            self.tb2.setText("Completed");
        if("Error" in text or "error" in text or "ImportError" in text):
            self.tb2.setText("Errors Found");
        self.append(text)


    def stderrReady(self):
        text = str(self.process.readAllStandardError().data(), encoding='utf-8')
        QMessageBox.about(self, "Training Status", "Errors Found");
        self.tb2.setText("Errors Found");
        self.append(text)


    def append(self, text):
        cursor = self.te1.textCursor()  
        self.te1.ensureCursorVisible() 
        cursor.movePosition(cursor.End)
        cursor.insertText(text)        


    def forward(self):
        self.system["epochs"] = self.e1.text();
        self.system["num_generations"] = self.e3.text();

        with open('obj_7_yolov3.json', 'w') as outfile:
            json.dump(self.system, outfile);

        self.forward_7_yolov3.emit();

    def backward(self):
        self.system["epochs"] = self.e1.text();
        self.system["num_generations"] = self.e3.text();

        with open('obj_7_yolov3.json', 'w') as outfile:
            json.dump(self.system, outfile);

        self.backward_hyper_param.emit();


'''
app = QApplication(sys.argv)
screen = WindowObj7Yolov3Train()
screen.show()
sys.exit(app.exec_())
'''