import configparser
import os

class Config:
    def __init__(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)

        # training
        train_config = config['TRAIN']
        self.batch_size = int(train_config['BATCH_SIZE'])
        self.max_epochs = int(train_config['MAX_EPOCHS'])
        self.log_interval = int(train_config['LOG_INTERVAL'])
        self.num_samples = int(train_config['NUM_SAMPLES'])
        self.drop_p = float(train_config['DROP_P'])
            
        # optimizer
        opt_config = config['OPTIMIZER']
        self.init_lr = float(opt_config['INIT_LR'])
        self.adam_eps = float(opt_config['ADAM_EPS'])
        self.adam_weight_decay = float(opt_config['ADAM_WEIGHT_DECAY'])

        # GCN
        gcn_config = config['GCN']
        self.hidden_size = int(gcn_config['HIDDEN_SIZE'])
        self.num_stages = int(gcn_config['NUM_STAGES'])

        # VIDEO_TRANFORMER
        tranfomer_config = config['VIDEO_TRANFORMER']
        self.input_path = str(tranfomer_config['INPUT_FOLDER_PATH'])
        self.output_path = str(tranfomer_config['OUTPUT_FOLDER_PATH'])
        self.total_pose_lm = int(tranfomer_config['TOTAL_POSE_LANDMARKS'])
        self.total_hand_lm = int(tranfomer_config['TOTAL_HAND_LANDMARKS'])
        self.total_hand = int(tranfomer_config['TOTAL_HANDS'])
        self.num_fr_process = int(tranfomer_config['NUM_FRAME_PROCESS'])
        self.nose_position = int(tranfomer_config['NOSE_POSITION'])

config_dir = os.path.dirname(os.path.abspath(__file__))
config = Config(os.path.join(config_dir, 'config.ini'))

