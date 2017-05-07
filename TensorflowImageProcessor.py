
# coding=utf-8
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import tensorflow as tf

# sess = tf.InteractiveSession()

# 字体的位置，不同版本的系统会有不同
font_path = 'C:/Users/Maxbin/AppData/Local/Programs/Python/Python35/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/cmb10.ttf'
# 生成几位数的验证码
number = 4
# 生成验证码图片的高度和宽度
size = (60, 20)
# 背景颜色，默认为白色
bgcolor = (255, 255, 255)
# 字体颜色，默认为蓝色
fontcolor = (0, 0, 255)
# 干扰线颜色。默认为红色
linecolor = (255, 0, 0)
# 是否要加入干扰线
draw_line = False
# 加入干扰线条数的上下限
line_number = (1, 5)

# 用来随机生成一个字符串
def gene_text():
    source = ["0", "1", "2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    return ''.join(random.sample(source, number))  # number是生成验证码的位数

# 用来绘制干扰线
def gene_line(draw, width, height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=linecolor)

# 生成验证码
def gene_code():
    width, height = size  # 宽和高
    image = Image.new('RGBA', (width, height), bgcolor)  # 创建图片
    font = ImageFont.truetype(font_path, 20)  # 验证码的字体
    draw = ImageDraw.Draw(image)  # 创建画笔
    text = gene_text()  # 生成字符串
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number+2, (height - font_height) / number+2), text,
              font=font, fill=fontcolor)  # 填充字符串
    if draw_line:
        gene_line(draw, width, height)
    # image.save('E:\\'+text+'.jpg')  # 保存验证码图片
    return text,image

# 将图像转化为灰度图像
def convert2gray(img):
    gray = np.array(img.convert('L'))
    # gray = gray.flatten() / 255
    return gray

# 将生成的四个字符转化为向量
def text2vec(text):
    vector = np.zeros(144)

    def char2pos(c):
        k = ord(c) - 48
        if k > 9:
            k = ord(c) - 55
            if k > 35:
                k = ord(c) - 61
                if k > 61:
                    raise ValueError('No Map')
        return k
    for i, c in enumerate(text):
        idx = i * 36 + char2pos(c)
        vector[idx] = 1
    return vector

# 向量转回文本
def vec2text(vec):
  char_pos = vec.nonzero()[0]
  text=[]
  for i, c in enumerate(char_pos):
      char_at_pos = i #c/63
      char_idx = c % 36
      if char_idx < 10:
        char_code = char_idx + ord('0')
      elif char_idx <36:
        char_code = char_idx - 10 + ord('A')
      elif char_idx < 62:
        char_code = char_idx-  36 + ord('a')
      elif char_idx == 62:
        char_code = ord('_')
      else:
        raise ValueError('error')
      text.append(chr(char_code))
  return "".join(text)

# 生成一个训练batch
def get_next_batch(batch_size):
    batch_x = np.zeros([batch_size, 20*60])
    batch_y = np.zeros([batch_size, 144])

    for i in range(batch_size):
        text, image = gene_code()
        image = convert2gray(image)

        # 将图片数组一维化 同时将文本也对应在两个二维组的同一行
        batch_x[i,:] = image.flatten() / 255 # (image.flatten()-128)/128  mean为0
        batch_y[i,:] = text2vec(text)
    # 返回该训练批次
    return batch_x, batch_y

# 申请占位符 按照图片
X = tf.placeholder(tf.float32, [None, 20*60])
Y = tf.placeholder(tf.float32, [None, 4*36])
keep_prob = tf.placeholder(tf.float32) # dropout

# 定义CNN
def crack_captcha_cnn(w_alpha=0.01, b_alpha=0.1):
    # 将占位符 转换为 按照图片给的新样式
    x = tf.reshape(X, shape=[-1, 20, 60, 1])

    # 3 conv layer
    w_c1 = tf.Variable(w_alpha*tf.random_normal([3, 3, 1, 32])) # 从正太分布输出随机值
    b_c1 = tf.Variable(b_alpha*tf.random_normal([32]))
    conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, w_c1, strides=[1, 1, 1, 1], padding='SAME'), b_c1))
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv1 = tf.nn.dropout(conv1, keep_prob)

    w_c2 = tf.Variable(w_alpha*tf.random_normal([3, 3, 32, 64]))
    b_c2 = tf.Variable(b_alpha*tf.random_normal([64]))
    conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, w_c2, strides=[1, 1, 1, 1], padding='SAME'), b_c2))
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv2 = tf.nn.dropout(conv2, keep_prob)

    w_c3 = tf.Variable(w_alpha*tf.random_normal([3, 3, 64, 64]))
    b_c3 = tf.Variable(b_alpha*tf.random_normal([64]))
    conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, w_c3, strides=[1, 1, 1, 1], padding='SAME'), b_c3))
    conv3 = tf.nn.max_pool(conv3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv3 = tf.nn.dropout(conv3, keep_prob)

    # Fully connected layer
    w_d = tf.Variable(w_alpha*tf.random_normal([3*8*64, 1024]))
    b_d = tf.Variable(b_alpha*tf.random_normal([1024]))
    dense = tf.reshape(conv3, [-1, w_d.get_shape().as_list()[0]])
    dense = tf.nn.relu(tf.add(tf.matmul(dense, w_d), b_d))
    dense = tf.nn.dropout(dense, keep_prob)

    w_out = tf.Variable(w_alpha*tf.random_normal([1024, 4*36]))
    b_out = tf.Variable(b_alpha*tf.random_normal([4*36]))
    out = tf.add(tf.matmul(dense, w_out), b_out)
    return out

# 训练
def train_crack_captcha_cnn():
    output = crack_captcha_cnn()
    # 为什么这里的sigmoid_cross_entropy_with_logits不能换成softmax_cross_entropy_with_logits？？？？？
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=Y))
    # 最后一层用来分类的softmax和sigmoid有什么不同？
    # optimizer 为了加快训练 learning_rate应该开始大，然后慢慢衰
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

    # predict是一个三维矩阵，核心是4行36列的二维矩阵
    predict = tf.reshape(output, [-1, 4, 36])
    # max_id_p是一个二维矩阵，但是只有一行，但是有4列，每个数字代表predict中每一行最大的那个数字所在的列
    max_idx_p = tf.argmax(predict, 2)
    max_idx_l = tf.argmax(tf.reshape(Y, [-1, 4, 36]), 2)
    correct_pred = tf.equal(max_idx_p, max_idx_l)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        step = 0
        accCount = 0
        while True:
            batch_x, batch_y = get_next_batch(64)
            _, loss_ = sess.run([optimizer, loss], feed_dict={X: batch_x, Y: batch_y, keep_prob: 0.75})
            # print(step, loss_)

            # 每100 step计算一次准确率
            if step % 100 == 0:
                batch_x_test, batch_y_test = get_next_batch(100)
                acc = sess.run(accuracy, feed_dict={X: batch_x_test, Y: batch_y_test, keep_prob: 1.})
                print(step, acc)
                if acc > 0.95:
                    accCount += 1
                    if accCount > 8:
                        saver.save(sess, "E://testspider/save_net.ckpt", global_step=step)
                        break
            step += 1

# def crack_captcha():
#    output = crack_captcha_cnn()
#
#    saver = tf.train.Saver()
#    with tf.Session() as sess:
#        saver.restore(sess, tf.train.latest_checkpoint('./'))
#        predict = tf.argmax(tf.reshape(output, [-1, 4, 36]), 2)
#        for i  in range(10):
#            text1, captcha_image = get_captcha()
#            text_list = sess.run(predict, feed_dict={X: [captcha_image], keep_prob: 1})
#
#            text = text_list[0].tolist()
#            vector = np.zeros(4*36)
#            i = 0
#            for n in text:
#                    vector[i*36 + n] = 1
#                    i += 1
#            print("正确: {}  预测: {}".format(text1, vec2text(vector)))
#            # return vec2text(vector)
#
# def get_captcha():
#    text, image = gene_code()
#    image = convert2gray(image)  # 生成一张新图
#    image = image.flatten() / 255  # 将图片一维化
#    return text, image
#
#
# if __name__ == '__main__':
#    crack_captcha()

train_crack_captcha_cnn()
