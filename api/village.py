def coords_from_vid(vid):
    vid -= 1
    y = vid % 200
    if y > 100:
        y = y - 200
    x = vid // 200
    if x > 100:
        x = x - 200
    return x, y


def vid_from_coords(x, y):
    if x < 0:
        vid = 200 * (200 + x)
    else:
        vid = 200 * x
    if y < 0:
        vid += (200 + y)
    else:
        vid += y
    return vid + 1


class Village:
    def __init__(self, account, vid, name):
        self.account = account
        self.vid = vid
        self.name = name
        [self.x, self.y] = coords_from_vid(self.vid)

    def __str__(self):
        return "{0}({1})".format(self.vid, self.name)
