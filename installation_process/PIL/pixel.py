from PIL import Image


class Pixel():
    def __init__(self, fp):
        self.img = Image.open(fp)

    def img_to_gray(self):
        self.img = self.img.convert('1')  # convert image to black and white

    def save(self, fp):
        self.img.save(fp)

    def judge_number(self):
        return len(self.img.getpixel((0, 0)))

    def print_pixel(self):
        x, y = self.img.size
        for i in range(x):
            for j in range(y):
                print((x, y), ">>>", self.img.getpixel((i, j)))

    def modify_pixel(self, x, y, rgb_tuple):
        self.img.putpixel((x, y), rgb_tuple)

    def noise_reduction(self, r1, r2, g1, g2, b1, b2):
        x, y = self.img.size
        for i in range(x):
            for j in range(y):
                rgb_list = self.img.getpixel((i, j))
                R = rgb_list[0]
                G = rgb_list[1]
                B = rgb_list[2]
                # self.scope_judge_modify(i, j)
                self.xx(i, j)
                # if r1<= R <= r2 or g1 <= G <= g2 or b1 <= B <= b2:
                #     self.modify_pixel(i, j, (0, 0, 0))
                # else:
                #     self.modify_pixel(i, j, (255, 255, 255))

                # if g1 > G > g2:
                #     self.modify_pixel(i, j, (0, 0, 0))
                # if b1 > B > b2:
                #     self.modify_pixel(i, j, (0, 0, 0))


    def scope_judge_modify(self, x, y):
        if x <2 or y<2:
            self.modify_pixel(x, y, (255, 255, 255))
            return
        if x>=self.img.size[0]-1 or y>=self.img.size[1]-1:
            self.modify_pixel(x, y, (255, 255, 255))
            return
        r, g, b = self.img.getpixel((x, y))
        if r==g==b==255:
            return

        r, g, b = self.img.getpixel((x+1, y))
        if r == g == b == 0:
            return

        r, g, b = self.img.getpixel((x-1, y))
        if r == g == b == 0:
            return

        r, g, b = self.img.getpixel((x, y+1))
        if r == g == b == 0:
            return

        r, g, b = self.img.getpixel((x, y-1))
        if r == g == b == 0:
            return

        print(x, y, self.img.getpixel((x, y)))
        self.modify_pixel(x, y, (255, 255, 255))

    def xx(self, a, b):
        n_list = []
        old_list = []
        xx = 0
        yy = 0
        print(">>> ", a, b)
        def hs(x, y):
            if [x, y] in old_list:
                return
            old_list.append([x, y])
            # print(x, y)
            # global n
            if len(set(n_list))>4:
                return
            if x <2 or y<2:
                self.modify_pixel(x, y, (255, 255, 255))
                return
            if x>=self.img.size[0]-1 or y>=self.img.size[1]-1:
                self.modify_pixel(x, y, (255, 255, 255))
                return
            # print(x, y)
            r, g, b = self.img.getpixel((x, y))
            if r==g==b==0:
                n_list.append((x, y))
                hs(x+xx, y+yy)
                hs(x-xx, y-yy)
            else:
                return 0
        xx = 1
        hs(a, b)
        xx = 0; yy=1
        old_list.remove([a, b])
        hs(a, b)
        if 0 < len(set(n_list)) <=2:
            print("x:", a, b, set(n_list))
            self.modify_pixel(a, b, (255, 255, 255))
        print("old:", old_list)
        print("<<< ", a, b, set(n_list))




if __name__ == '__main__':
    p = Pixel("11.png")
    # p.print_pixel()
    p.noise_reduction(200, 255, 200, 255, 200, 255)
    p.save("3.png")



# img = Image.open("result.png")
# print(img.size)
# for i in range(img.size[0]):
#     for j in range(img.size[1]):
#         print(i, j)
#         try:
#             # print(img.getpixel((i, j)))
#             # r, g, b, alpha = img.getpixel((i, j))
#             r, g, b = img.getpixel((i, j))
#             def zzz(x, y):
#                 r, g, b = img.getpixel((x, y))
#                 if r==g==b==255:
#                     return 1
#                 a=0;b=0;c=0;d=0
#                 if x<i+1:
#                     a = zzz(x+1, y)
#                 if y<j+1:
#                     b = zzz(x, y+1)
#                 if x>i-1:
#                     c = zzz(x-1, y)
#                 if y>j-1:
#                     d = zzz(x, y-1)
#
#                 if a==b==d==c==1:
#                     return 4
#
#
#             if r==g==b==0:
#                 if 4 == zzz(i, j):
#                     for a in range(i-1, i+1):
#                         for b in range(j-1, j+1):
#                             img.putpixel((a, b), (255, 255, 255))
#
#
#             # print(r, g, b)
#             """
#             if r == 0 and g == 0 and b == 0:
#                 # g = 204
#                 # img.putpixel((i, j), (255, 255, 255, alpha))
#                 img.putpixel((i, j), (255, 255, 255))
#             else:
#                 # img.putpixel((i, j), (0, 0, 0, alpha))
#                 img.putpixel((i, j), (0, 0, 0))
#             """
#
#         except Exception as e:
#             # print(i, j)
#             continue
# img.show()