import tensorflow as tf

from tensorflow.keras import layers, optimizers, Sequential
import os, pathlib, random
# tf配置
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = '/gpu:0'
# 1.读入所有文件并存入列表 并打乱
train_data_path = pathlib.Path('../dataset/train')
train_patch = list(train_data_path.glob("*/*"))
train_patch = [str(path) for path in train_patch]
random.shuffle(train_patch)
# 读入测试集
test_data_path = pathlib.Path('../dataset/test')
test_patch = list(test_data_path.glob("*/*"))
test_patch = [str(path) for path in test_patch]
random.shuffle(test_patch)
# 2.读入所有标签(文件夹名) 并 排序
train_labels = list(train_data_path.glob("*/"))
train_labels=list(map(lambda x:x.name,train_labels))
train_labels.sort()
#读入测试集标签
test_labels = list(test_data_path.glob("*/"))
test_labels=list(map(lambda x:x.name,test_labels))
test_labels.sort()
# 3.将标签存入字典
train_label_to_index = dict((name,index) for index,name in enumerate(train_labels))
test_label_to_index = dict((name,index) for index,name in enumerate(test_labels))
# 4.生成对应序号的数据集标签
train_image_labels = [train_label_to_index[pathlib.Path(path).parent.name]
                      for path in train_patch]
test_image_labels = [test_label_to_index[pathlib.Path(path).parent.name]
                      for path in test_patch]

# 二.tensorflow读入数据
def pre_process(path,label):
    img = tf.io.read_file(path)
    img =tf.io.decode_jpeg(img,channels=1) # 1 gray pic
    img = tf.cast(img,dtype=tf.float32) / 255.
    label =tf.convert_to_tensor(int(label))
    label = tf.one_hot(label,depth=8+26) # 34 分类任务
    return img,label

batch_size = 100
# 读入数据到tf
train_db = tf.data.Dataset.from_tensor_slices((train_patch,train_image_labels))
test_db = tf.data.Dataset.from_tensor_slices((test_patch,test_image_labels))
# 数据预处理
train_db =train_db.shuffle(10000).map(pre_process).batch(batch_size)
test_db =test_db.shuffle(10000).map(pre_process).batch(batch_size)
# 建立网络

network = Sequential([
    layers.Conv2D(22, (5, 5), activation='relu', input_shape=(22, 22,1)),
    layers.MaxPool2D((2, 2)),
    layers.Conv2D(32, (4, 4), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(rate=0.5),
    layers.Dense(128, activation='relu'),
    layers.Dropout(rate=0.5),
    layers.Dense(34, activation='softmax'),
])
network.summary()

network.compile(optimizer=optimizers.Adam(lr=1e-3),
		loss='categorical_crossentropy',
		metrics=['accuracy'])

network.fit(train_db,validation_data=test_db, epochs=10, validation_freq=1)
network.save("../model.h5")

#500数据集  0s 99ms/step - loss: 3.4084 - accuracy: 0.0951 - val_loss: 3.3525 - val_accuracy: 0.0556
#1000数据集 loss: 0.6837 - accuracy: 0.8083 - val_loss: 0.2254 - val_accuracy: 0.9534
#3000数据集  loss: 0.2575 - accuracy: 0.9542 - val_loss: 0.1514 - val_accuracy: 0.9765


