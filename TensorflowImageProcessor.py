
# coding=utf-8
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import tensorflow as tf

# sess = tf.InteractiveSession()

# �����λ�ã���ͬ�汾��ϵͳ���в�ͬ
font_path = 'C:/Users/Maxbin/AppData/Local/Programs/Python/Python35/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/cmb10.ttf'
# ���ɼ�λ������֤��
number = 4
# ������֤��ͼƬ�ĸ߶ȺͿ��
size = (60, 20)
# ������ɫ��Ĭ��Ϊ��ɫ
bgcolor = (255, 255, 255)
# ������ɫ��Ĭ��Ϊ��ɫ
fontcolor = (0, 0, 255)
# ��������ɫ��Ĭ��Ϊ��ɫ
linecolor = (255, 0, 0)
# �Ƿ�Ҫ���������
draw_line = False
# ���������������������
line_number = (1, 5)

# �����������һ���ַ���
def gene_text():
    source = ["0", "1", "2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    return ''.join(random.sample(source, number))  # number��������֤���λ��

# �������Ƹ�����
def gene_line(draw, width, height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=linecolor)

# ������֤��
def gene_code():
    width, height = size  # ��͸�
    image = Image.new('RGBA', (width, height), bgcolor)  # ����ͼƬ
    font = ImageFont.truetype(font_path, 20)  # ��֤�������
    draw = ImageDraw.Draw(image)  # ��������
    text = gene_text()  # �����ַ���
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number+2, (height - font_height) / number+2), text,
              font=font, fill=fontcolor)  # ����ַ���
    if draw_line:
        gene_line(draw, width, height)
    # image.save('E:\\'+text+'.jpg')  # ������֤��ͼƬ
    return text,image

# ��ͼ��ת��Ϊ�Ҷ�ͼ��
def convert2gray(img):
    gray = np.array(img.convert('L'))
    # gray = gray.flatten() / 255
    return gray

# �����ɵ��ĸ��ַ�ת��Ϊ����
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

# ����ת���ı�
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

# ����һ��ѵ��batch
def get_next_batch(batch_size):
    batch_x = np.zeros([batch_size, 20*60])
    batch_y = np.zeros([batch_size, 144])

    for i in range(batch_size):
        text, image = gene_code()
        image = convert2gray(image)

        # ��ͼƬ����һά�� ͬʱ���ı�Ҳ��Ӧ��������ά���ͬһ��
        batch_x[i,:] = image.flatten() / 255 # (image.flatten()-128)/128  meanΪ0
        batch_y[i,:] = text2vec(text)
    # ���ظ�ѵ������
    return batch_x, batch_y

# ����ռλ�� ����ͼƬ
X = tf.placeholder(tf.float32, [None, 20*60])
Y = tf.placeholder(tf.float32, [None, 4*36])
keep_prob = tf.placeholder(tf.float32) # dropout

# ����CNN
def crack_captcha_cnn(w_alpha=0.01, b_alpha=0.1):
    # ��ռλ�� ת��Ϊ ����ͼƬ��������ʽ
    x = tf.reshape(X, shape=[-1, 20, 60, 1])

    # 3 conv layer
    w_c1 = tf.Variable(w_alpha*tf.random_normal([3, 3, 1, 32])) # ����̫�ֲ�������ֵ
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

# ѵ��
def train_crack_captcha_cnn():
    output = crack_captcha_cnn()
    # Ϊʲô�����sigmoid_cross_entropy_with_logits���ܻ���softmax_cross_entropy_with_logits����������
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=Y))
    # ���һ�����������softmax��sigmoid��ʲô��ͬ��
    # optimizer Ϊ�˼ӿ�ѵ�� learning_rateӦ�ÿ�ʼ��Ȼ������˥
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

    # predict��һ����ά���󣬺�����4��36�еĶ�ά����
    predict = tf.reshape(output, [-1, 4, 36])
    # max_id_p��һ����ά���󣬵���ֻ��һ�У�������4�У�ÿ�����ִ���predict��ÿһ�������Ǹ��������ڵ���
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

            # ÿ100 step����һ��׼ȷ��
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
#            print("��ȷ: {}  Ԥ��: {}".format(text1, vec2text(vector)))
#            # return vec2text(vector)
#
# def get_captcha():
#    text, image = gene_code()
#    image = convert2gray(image)  # ����һ����ͼ
#    image = image.flatten() / 255  # ��ͼƬһά��
#    return text, image
#
#
# if __name__ == '__main__':
#    crack_captcha()

train_crack_captcha_cnn()
