# redirect output of a run to a txt file and provide as input here to plot Loss, top1, top5 for test, val and val ema

import os
import numpy as np
import matplotlib.pyplot as plt
import sys

class SummaryPlots(object):
    """
        Generate different kinds of summary plots from output from a run.
        
        Assumes : line after "*** Training summary" will have "loss=1.5650 || top1=64.6799 || top5=85.8776"
                  line after "*** Validation summary" will have "loss=2.8883 || top1=49.9630 || top5=75.2963"
                  line after "*** Validation (Ema) summary" will have "loss=2.4126 || top1=56.9259 || top5=80.8148
                  in input run output txt file
    """
    
    def __init__(self, path_to_run_output_file=None):
        self.path_to_run_output_file = path_to_run_output_file
        
        
    def input_file_exists(self):
        if os.path.exists(self.path_to_run_output_file):
            return True
        else: 
            print("Input file does not exists.")
            return False
        
    def parse_values_in_summary_line(self, next_line):
        # assumes values occur after "=" and in this order 
        # "loss=2.8883 || top1=49.9630 || top5=75.2963"
        split_parts = next_line.split("=")
        loss = float(split_parts[1].split("||")[0])
        top1 = float(split_parts[2].split("||")[0])
        top5 = float(split_parts[-1])
        
        return loss, top1, top5
    
    def parse_lr_values(self, prev_line):
        split_parts = prev_line.split("LR: [")
        lr_str = split_parts[1].split(",")[0]
        lr = float(lr_str)
        
        return lr
        
    def gen_loss_top1_top5(self):
        train_epoch_loss_top1_top5 = [] # np.zeros((lines.count, 4))
        val_epoch_loss_top1_top5 = [] # np.zeros((lines.count, 4))
        valema_epoch_loss_top1_top5 = [] # np.zeros((lines.count, 4))        
        if (self.input_file_exists()):
            lines = []
            with open(self.path_to_run_output_file) as f:
                lines = f.readlines()
                total_lines = len(lines)
                
                for line_num, line in enumerate(lines):
                    if line_num + 1 < total_lines: 
                        prev_line = lines[line_num - 1] # to get 
                        next_line = lines[line_num + 1]                        
                        if "*** Training summary" in line:
                            epoch = int(line.split(" ")[-1])
                            loss, top1, top5 = self.parse_values_in_summary_line(next_line)
                            lr = self.parse_lr_values(prev_line)
                            train_epoch_loss_top1_top5.append( (epoch, loss, top1, top5, lr) )
                        elif "*** Validation summary" in line:
                            epoch = int(line.split(" ")[-1])
                            loss, top1, top5 = self.parse_values_in_summary_line(next_line)   
                            lr = self.parse_lr_values(prev_line)
                            val_epoch_loss_top1_top5.append( (epoch, loss, top1, top5, lr) )                         
                        elif "*** Validation (Ema) summary" in line:
                            epoch = int(line.split(" ")[-1])
                            loss, top1, top5 = self.parse_values_in_summary_line(next_line)  
                            lr = self.parse_lr_values(prev_line)
                            valema_epoch_loss_top1_top5.append( (epoch, loss, top1, top5, lr) )                            
                        else: 
                            continue
         
        return np.array(train_epoch_loss_top1_top5), np.array(val_epoch_loss_top1_top5), np.array(valema_epoch_loss_top1_top5)             
        
    def plot_loss_train_val(self, train, val):        
        output_path = os.path.splitext(self.path_to_run_output_file)[0] + "_loss.png"
        
        fig, ax = plt.subplots()
        ax.plot(train[:,0], train[:,1], label="train") # epoch vs train loss
        ax.plot(val[:,0], val[:,1], label="val") # epoch vs val loss 
        ax.set_xlabel("epoch")
        ax.set_ylabel("loss")
        ax.set_ylim([0, 8.0])
        ax.set_title("training and validation loss")
        ax.legend(loc="upper center")
        
        ax2 = ax.twinx()
        ax2.plot(train[:,0], train[:,4], '.g', label="learn rate") # epoch vs lr 
        ax2.set_ylabel("learning rate")
        ax2.legend(loc='lower center')
        ax2.set_ylim([0.0, 0.5])
        fig.savefig(output_path, format='png', dpi=300, bbox_inches='tight')
    
    def plot_top1_train_val(self, train, val):
        output_path = os.path.splitext(self.path_to_run_output_file)[0] + "_top1.png"
        
        fig, ax = plt.subplots()
        ax.plot(train[:,0], train[:,2], label="train") # epoch vs train loss
        ax.plot(val[:,0], val[:,2], label="val") # epoch vs val loss 
        ax.set_xlabel("epoch")
        ax.set_ylabel("top1")
        ax.set_ylim([0, 100])
        ax.set_title("training and validation top1")
        ax.legend(loc="upper center")
        
        ax2 = ax.twinx()
        ax2.plot(train[:,0], train[:,4], '.g', label="learn rate") # epoch vs lr 
        ax2.set_ylabel("learning rate")
        ax2.legend(loc='lower center')
        ax2.set_ylim([0.0, 0.5])        
        fig.savefig(output_path, format='png', dpi=300, bbox_inches='tight')            
        
    
    def plot_top5_train_val(self, train, val):
        output_path = os.path.splitext(self.path_to_run_output_file)[0] +"_top5.png"
        
        fig, ax = plt.subplots()
        ax.plot(train[:,0], train[:,3], label="train") # epoch vs train loss
        ax.plot(val[:,0], val[:,3], label="val") # epoch vs val loss 
        ax.set_xlabel("epoch")
        ax.set_ylabel("top5")
        ax.set_ylim([0, 100])        
        ax.set_title("training and validation top5")
        ax.legend(loc="upper center")
        ax2 = ax.twinx()
        ax2.plot(train[:,0], train[:,4], '.g', label="learn rate") # epoch vs lr 
        ax2.set_ylabel("learning rate")
        ax2.legend(loc='lower center')
        ax2.set_ylim([0.0, 0.5])         
        fig.savefig(output_path, format='png', dpi=300, bbox_inches='tight')          
           
        
    def gen_plots(self, train, val):
        self.plot_loss_train_val(train, val)
        self.plot_top1_train_val(train, val)
        self.plot_top5_train_val(train, val)
        

## Test 
def main(argv):
    #input_run_file = "results\AU_results_resnet_tiny_correct_class.txt"
    #input_run_file = "results\AU_results_resnet_tiny_correct_class_depth18.txt"
    #input_run_file = "results\AU_results_resnet_tiny_correct_class_depth18_cyclic.txt"
    #input_run_file = "results\AU_results_resnet_tiny_correct_class_depth18_augment.txt"
    #input_run_file = "results\AU_results_resnet_tiny_correct_class_depth18_augment2.txt"
    #input_run_file = "results\AU_results_resnet_tiny_correct_class_depth50_augment3.txt"
    #input_run_file = "results\AU_results_resnet_tiny_correct_class_depth50_augment4_cutout.txt"
    #input_run_file = "results\AU_results_resnet_tiny_correct_class_depth50_augment4_cutout_300.txt"
    #input_run_file = "results\AU_results_resnet_tiny_correct_class_depth50_augment4_cutout_wd1.txt"
    #input_run_file = "results\AU_results_resnet_tiny_correct_class_depth50_augment4_cutout_wd2.txt"
    input_run_file = "results\AU_results_resnet_tiny_correct_class_depth50_lr0pt1.txt"
    #input_run_file = "results\AU_results_resnet_tiny_correct_class_depth50_lr0pt1-2.txt"
    
    if len(argv) < 1: 
        input_run_file = input_run_file        
    else:
        input_run_file = argv[0]
        
    plots = SummaryPlots(input_run_file)
    train, val, valema = plots.gen_loss_top1_top5()
    if len(train) == 0:
        print("No values to plot.")
    else:
        plots.gen_plots(train, valema)

if __name__ == "__main__":
    main(sys.argv[1:])