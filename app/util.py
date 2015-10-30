from flask import json
from bson import json_util, ObjectId

def bson_to_json(data):
    return json.dumps(data, default=json_util.default)

def bson_obj_id(id):
    return ObjectId(id)

class AllowFile:
    IMG_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'bmp'])

    @classmethod
    def is_img(cls, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in cls.IMG_EXTENSIONS

class TypeRender:

    _template = '''
        <tr class="center aligned" data-type="{type}">
          <td class="six wide">{name}</td>
          <td class="ten wide {attr_cls}">{attr}</td>
        </tr>
    '''

    _type = {
        'text': '{v}',
        'img': '<img src={v} width=200 height=150 />',
        'url': '<a href="{v}" target="_blank">{v}</a>',
        'num': '{v}',
        'star': '<div class="ui massive star rating">{v}</div>'
    }

    _star_tmp = '<i class="icon active"></i>'

    @classmethod
    def _content_of_type(cls, value, type):
        if type == 'star':
            content = cls._type['star'].format(v=int(value) * cls._star_tmp)
        elif type == 'bool':
            if type is True or value == 1:
                content = '是'
            else:
                content = '否'
        else:
            content = cls._type[type].format(v=value)
        return content

    @classmethod
    def _class_of_type(cls,value, type):
        if type == 'bool':
            if type is True or value == 1:
                return 'positive'
            else:
                return 'negative'
        return ''

    @classmethod
    def render_html(cls, attr_name, attr_value, attr_type):
        content = cls._content_of_type(attr_value, attr_type)
        td_class = cls._class_of_type(attr_value, attr_type)
        return cls.render(attr_name, content, attr_type, td_class)

    @classmethod
    def render_many(cls, attr_name, attr_list):
        begin = '<tr class="center aligned" "><td>{name}</td>'
        td = '<td class="{attr_cls}">{attr}</td>'
        end = '</tr>'

        td_arr = []
        for attr in attr_list:
            if not attr:
                td_arr.append(td.format(attr='?', attr_cls=''))
            else:
                td_arr.append(td.format(attr=cls._content_of_type(attr['attr_value'], attr['attr_type']), \
                            attr_cls=cls._class_of_type(attr['attr_value'], attr['attr_type'])))

        html = begin.format(name=attr_name, type='') + ''.join(td_arr) + end
        return html

    @classmethod
    def render(cls, name, attr, type, td_class=''):
        return cls._template.format(name=name, attr=attr, type=type, attr_cls=td_class)