from PIL import Image, ImageFont, ImageDraw
from collections import namedtuple
from io import BytesIO
import base64

def outp_b64(outp_img):
    if isinstance(outp_img, str):
        outp_img = Image.open(outp_img)
    buf = BytesIO()
    outp_img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    return f'[CQ:image,file={base64_str}]'

def position_tuple(*args):
    Position = namedtuple('Position', ['top', 'right', 'bottom', 'left'])
    if len(args) == 0:
        return Position(0, 0, 0, 0)
    elif len(args) == 1:
        return Position(args[0], args[0], args[0], args[0])
    elif len(args) == 2:
        return Position(args[0], args[1], args[0], args[1])
    elif len(args) == 3:
        return Position(args[0], args[1], args[2], args[1])
    else:
        return Position(args[0], args[1], args[2], args[3])


def draw_table(table, header=[], font=ImageFont.load_default(), cell_pad=(20, 10), margin=(10, 10), align=None, colors={}, stock=False) -> Image.Image:
    """
    Draw a table using only Pillow
    table:    an 2d list, must be str
    header:   turple or list, must be str
    font:     an ImageFont object
    cell_pad: padding for cell, (top_bottom, left_right)
    margin:   margin for table, css-like shorthand
    align:    None or list, 'l'/'c'/'r' for left/center/right, length must be the max count of columns
    colors:   dict, as follows
    stock:    bool, set red/green font color for cells start with +/-
    """
    _color = {
        'bg': 'white',
        'cell_bg': 'white',
        'header_bg': 'gray',
        'font': 'black',
        'rowline': 'black',
        'colline': 'black',
        'red': 'red',
        'green': 'green',
    }


    _color.update(colors)
    _margin = position_tuple(*margin)

    table = table.copy()
    if header:
        table.insert(0, header)
    row_max_hei = [0] * len(table)
    col_max_wid = [0] * len(max(table, key=len))
    tab = Image.new(size=(1000, 1000), mode='RGB')
    draw = ImageDraw.Draw(tab)
    for i in range(len(table)):
        for j in range(len(table[i])):
            col_max_wid[j] = max(draw.textsize(table[i][j], font)[0], col_max_wid[j])
            row_max_hei[i] = max(draw.textsize(table[i][j], font)[1], row_max_hei[i])
    tab_width = sum(col_max_wid) + len(col_max_wid) * 2 * cell_pad[0]
    tab_heigh = sum(row_max_hei) + len(row_max_hei) * 2 * cell_pad[1]

    tab = Image.new('RGB', (tab_width + _margin.left + _margin.right, tab_heigh + _margin.top + _margin.bottom), _color['bg'])
    draw = ImageDraw.Draw(tab)

    # draw.rectangle([(_margin.left, _margin.top), (_margin.left + tab_width, _margin.top + tab_heigh)], 
                   # fill=_color['cell_bg'], width=0)
    if header:
        draw.rectangle([(_margin.left, _margin.top), (_margin.left + tab_width, _margin.top + row_max_hei[0] + cell_pad[1] * 2)], 
                       fill=_color['header_bg'], width=0)

    top, left = _margin.top + cell_pad[1], 0
    for i in range(len(table)):
        left = _margin.left + cell_pad[0]
        row_color = _color['even_row_cell_bg'] if (i & 1) else _color['odd_row_cell_bg']
        if not header or i != 0:
            bg_left, bg_top = left - cell_pad[0], top - cell_pad[1]
            draw.rectangle([(bg_left, bg_top), (bg_left + tab_width, bg_top + row_max_hei[i] + cell_pad[1] * 2)], 
                           fill=row_color, width=0)
        for j in range(len(table[i])):
            color = _color['font']
            if stock:
                if table[i][j].startswith('#'):
                    table[i][j] = table[i][j][1:]
                    status = table[i][j]
                    bg_color = _color[status]
                    bg_left, bg_top = left - cell_pad[0], top - cell_pad[1]
                    draw.rectangle([(bg_left, bg_top), (bg_left + col_max_wid[j] + cell_pad[0] * 2, bg_top + row_max_hei[i] + cell_pad[1] * 2)], 
                                   fill=bg_color, width=0)
            _left = left
            if (align and align[j] == 'c') or (header and i == 0):
                _left += (col_max_wid[j] - draw.textsize(table[i][j], font)[0]) // 2
            elif align and align[j] == 'r':
                _left += col_max_wid[j] - draw.textsize(table[i][j], font)[0]
            _top = top 
            _top += (row_max_hei[i] - draw.textsize(table[i][j], font)[1]) // 2 # always vertical center
            draw.text((_left, _top), table[i][j].replace('\t', ' '), font=font, fill=color)
            left += col_max_wid[j] + cell_pad[0] * 2
        top += row_max_hei[i] + cell_pad[1] * 2

    left = _margin.left
    for col_w in col_max_wid:
        draw.line([(left, _margin.top), (left, tab_heigh +_margin.top)], fill=_color['colline'])
        left += col_w + cell_pad[0] * 2
    draw.line([(left, _margin.top), (left, tab_heigh + _margin.top)], fill=_color['colline'])

    top = _margin.top
    for row_h in row_max_hei:
        draw.line([(_margin.left, top), (tab_width + _margin.left, top)], fill=_color['rowline'])
        top += row_h + cell_pad[1] * 2
    draw.line([(_margin.left, top), (tab_width + _margin.left, top)], fill=_color['rowline'])

    return tab

def json2imgb64(records, titles=None, font=ImageFont.load_default(), cell_pad=(20, 10), margin=(10, 10), align=None, colors={}, stock=False) -> str:
    '''
    :param records: 格式: [dict, dict, ..., dict]。E:[{"x":1, "y":2}, {"x":3, "y":4}]
    :param titles: E:["x", "y"]。当titles=None时，尝试从grid[0]获取。
    :return 可直接向qq发送的图片b64。
    '''
    assert len(records)
    if titles == None:
        titles = records[0].keys()
    assert sum([set(record) != set(titles) for record in records]) == 0

    outp = [[] for _ in titles]
    for i, title in enumerate(titles):
        for record in records:
            outp[i].append(record[title])

    return outp_b64(draw_table(outp, titles, font, cell_pad, margin, align, colors, stock))

def grid2imgb64(grid, titles, font=ImageFont.load_default(), cell_pad=(20, 10), margin=(10, 10), align=None, colors={}, stock=False) -> str:
    '''
    :param grid: 格式: [list,list,...,list]。E:[[1, 2],[3, 4]]
    :param titles: progress中每条记录中的每一项的title。E:["key", "value"]
    :return 可直接向qq发送的图片b64。
    '''

    assert len(grid)
    assert len(titles)
    assert sum([len(record) != len(titles) for record in grid]) == 0

    return outp_b64(draw_table(grid, titles, font, cell_pad, margin, align, colors, stock))

def grid2img(grid, titles, font=ImageFont.load_default(), cell_pad=(20, 10), margin=(10, 10), align=None, colors={}, stock=False) -> Image.Image:
    '''
    :param grid: 格式: [list,list,...,list]。E:[[1, 2],[3, 4]]
    :param titles: progress中每条记录中的每一项的title。E:["key", "value"]
    :return 返回Image变量
    '''

    assert len(grid)
    assert len(titles)
    assert sum([len(record) != len(titles) for record in grid]) == 0

    return draw_table(grid, titles, font, cell_pad, margin, align, colors, stock)
