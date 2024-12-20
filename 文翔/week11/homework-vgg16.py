import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

# 加载 CIFAR-10 数据集
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# 数据预处理
x_train = x_train.astype('float32') / 255.0  # 标准化
x_test = x_test.astype('float32') / 255.0

y_train = to_categorical(y_train, 10)  # 独热编码
y_test = to_categorical(y_test, 10)

# 构建 VGG16 模型
model = models.Sequential()

# 第一组卷积层
model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=(32, 32, 3)))
model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(layers.MaxPooling2D((2, 2), strides=2))

# 第二组卷积层
model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(layers.MaxPooling2D((2, 2), strides=2))

# 第三组卷积层
model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(layers.MaxPooling2D((2, 2), strides=2))

# 第四组卷积层
model.add(layers.Conv2D(512, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(512, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(512, (3, 3), activation='relu', padding='same'))
model.add(layers.MaxPooling2D((2, 2), strides=2))

# 第五组卷积层
model.add(layers.Conv2D(512, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(512, (3, 3), activation='relu', padding='same'))
model.add(layers.Conv2D(512, (3, 3), activation='relu', padding='same'))
model.add(layers.MaxPooling2D((2, 2), strides=2))

# 扁平化层
model.add(layers.Flatten())

# 全连接层
model.add(layers.Dense(4096, activation='relu'))
model.add(layers.Dropout(0.5))

model.add(layers.Dense(4096, activation='relu'))
model.add(layers.Dropout(0.5))

# 输出层：10 个神经元，对应 CIFAR-10 的 10 个类别
model.add(layers.Dense(10, activation='softmax'))

# 编译模型
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 查看模型概况
model.summary()

# 训练模型
history = model.fit(x_train, y_train, epochs=20, batch_size=64, validation_data=(x_test, y_test))

# 评估模型
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f"Test accuracy: {test_acc:.4f}")

# 推理功能：预测输入的图像
def predict_image(img_path):
    # 加载图片，调整为 32x32 的大小
    img = image.load_img(img_path, target_size=(32, 32))

    # 转换为 NumPy 数组
    img_array = image.img_to_array(img)

    # 扩展维度以符合模型输入格式 (batch_size, height, width, channels)
    img_array = np.expand_dims(img_array, axis=0)

    # 归一化处理
    img_array = img_array.astype('float32') / 255.0

    # 使用模型进行预测
    predictions = model.predict(img_array)

    # 获取预测的类别（索引值）
    predicted_class = np.argmax(predictions, axis=1)

    # CIFAR-10 类别标签
    class_labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

    # 输出预测结果
    print(f"Predicted class: {class_labels[predicted_class[0]]}")
    plt.imshow(img)
    plt.show()

# 推理一张图像
image_path = 'test_image.jpg'  
predict_image(image_path)
