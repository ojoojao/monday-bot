import requests
from html.parser import HTMLParser
import markdownify
import json

class HTMLFilter(HTMLParser):
    text = ""
    new_line = True
    def handle_data(self, data):
        if "." in data:
            self.text += data + "\n"
            self.new_line = True
        else:
            if self.new_line:
                self.text += "- " + data
                self.new_line = False
            else:
                self.text += data

class HTMLFilterRaw(HTMLParser):
    text = ""
    def handle_data(self, data):
            
        self.text += data


def get_reference(url):
    r = requests.get(url)
    r.encoding = 'UTF-8'

    i = r.text.find('<div class="main">')

    r = r.text[i:]

    i = r.find('<h1 id="twitch-api-reference">Twitch API Reference</h1>')
    

    return r[i:]

def get_functions(html:str):
    f = []

    inicio = '<section class="left-docs">'
    final = '<section class="doc-content">'

    t = html

    while t.find(final) != -1:
        i = t.find(inicio) + len(inicio)
        t = t[i:]
        _i = t.find(final)

        f.append(t[:_i])

        t = t[_i+len(final):]

    i = t.find(inicio) + len(inicio)
    t = t[i:]
    _i = t.find(final)

    f.append(t[:_i])

    return f

def get_info(functions: list):
    out = {}
    
    for i_f, f in enumerate(functions):
        inicio = '<h2 id="'
        final = '">'

        i = f.find(inicio) + len(inicio)
        f = f[i:]
        _i = f.find(final)

        f_id = f[:_i]

        out[f_id] = {}

        f = f[_i:]

        inicio = f'<a class="editor-link" href="cloudcannon:#content_blocks[{i_f}]" data-cms-editor-link-style="modal">&#x270E;</a>'
        final = '<h3>Request Query'

        i = f.find(inicio) + len(inicio)
        f = f[i:]
        _i = f.find(final)

        query = True
        if _i == -1:
            query = False
            _i = f.find('<h3>Request Body')
            if _i == -1:
                _i = f.find('<h3>Response Body</h3>')

        f_info = f[:_i]

        h = markdownify.markdownify(f_info, heading_style="ATX")
        
        out[f_id]['info'] = h

        out[f_id]['query'] = {}
        
        if query:
            f = f[_i:]

            inicio = final
            final = '</tbody>'

            i = f.find(inicio) + len(inicio)
            f = f[i:]
            _i = f.find(final)

            f_query = f[:_i]

            inicio = '<thead>'
            final = '</thead>'

            i = f_query.find(inicio) + len(inicio)
            f_query = f_query[i:]
            _i = f_query.find(final)

            heads = f_query[:_i]

            h_inicio = '<th>'
        
            head_count = 0
            while heads.find(h_inicio) != -1:
                h_i = heads.find(h_inicio) + len(h_inicio)
                heads = heads[h_i:]

                head_count += 1

            f_query = f_query[_i:]

            inicio = '<tr>'
            final = '</tr>'
            b_inicio = '<td>'
            b_final = '</td>'

            while f_query.find(inicio) != -1:
                i = f_query.find(inicio) + len(inicio)
                f_query = f_query[i:]
                _i = f_query.find(final)

                b = f_query[:_i]

                f_query = f_query[_i+len(final):]

                for __i in range(0, head_count):
                    i = b.find(b_inicio) + len(b_inicio)
                    b = b[i:]
                    _i = b.find(b_final)

                    if __i == 0:

                        var = b[:_i]

                        b = b[_i+len(b_final):]
                    if __i == 1:

                        tipo = b[:_i]

                        b = b[_i+len(b_final):]

                    if head_count > 3:
                        if __i == 2:
                            outro = b[:_i]

                            b = b[_i+len(b_final):]
                        if __i == 3:

                            descr = b[:_i]

                            b = b[_i+len(b_final):]
                    else:
                        if __i == 2:

                            descr = b[:_i]

                            b = b[_i+len(b_final):]
                        
                        outro = ''

                h = markdownify.markdownify(descr, heading_style="ATX")

                v = HTMLFilterRaw()
                v.feed(var)
                var = v.text.strip()

                out[f_id]['query'][var] = [var, tipo, outro, h] 

                f = f_query
        else:
            out[f_id]['query']["None"] = ""

        _i = f.find('<h3>Request Body')

        body = True
        if _i == -1:
            body = False
            if _i == -1:
                _i = f.find('<h3>Response Body</h3>')
            
        out[f_id]['body'] = {}

        if body:
            f = f[_i:]

            inicio = final
            final = '</tbody>'

            i = f.find(inicio) + len(inicio)
            f = f[i:]
            _i = f.find(final)

            f_body = f[:_i]

            inicio = '<thead>'
            final = '</thead>'

            i = f_body.find(inicio) + len(inicio)
            f_body = f_body[i:]
            _i = f_body.find(final)

            heads = f_body[:_i]

            h_inicio = '<th>'
        
            head_count = 0
            while heads.find(h_inicio) != -1:
                h_i = heads.find(h_inicio) + len(h_inicio)
                heads = heads[h_i:]

                head_count += 1

            f_body = f_body[_i:]

            inicio = '<tr>'
            final = '</tr>'
            b_inicio = '<td>'
            b_final = '</td>'

            while f_body.find(inicio) != -1:
                i = f_body.find(inicio) + len(inicio)
                f_body = f_body[i:]
                _i = f_body.find(final)

                b = f_body[:_i]

                f_body = f_body[_i+len(final):]

                for __i in range(0, head_count):
                    i = b.find(b_inicio) + len(b_inicio)
                    b = b[i:]
                    _i = b.find(b_final)

                    if __i == 0:

                        var = b[:_i]

                        b = b[_i+len(b_final):]
                    if __i == 1:

                        tipo = b[:_i]

                        b = b[_i+len(b_final):]

                    if head_count > 3:
                        if __i == 2:
                            outro = b[:_i]

                            b = b[_i+len(b_final):]
                        if __i == 3:

                            descr = b[:_i]

                            b = b[_i+len(b_final):]
                    else:
                        if __i == 2:

                            descr = b[:_i]

                            b = b[_i+len(b_final):]
                        
                        outro = ''

                h = markdownify.markdownify(descr, heading_style="ATX")

                v = HTMLFilterRaw()
                v.feed(var)
                var = v.text.strip()

                out[f_id]['body'][var] = [var, tipo, outro, h] 

                f = f_body
        else:
            out[f_id]['body']["None"] = ""


    return out

if __name__ == "__main__":
    page = get_reference("https://dev.twitch.tv/docs/api/reference/")
    
    l = get_functions(page)

    f = get_info(l)
    print(len(f.keys()))

    with open("./docs/docstrings/index.html", "w", encoding="UTF-8") as file:
        file.write(l[9])
    file.close()

    with open("./docs/docstrings/infos.json", "w", encoding="UTF-8") as file:
        json.dump(f, file, indent=4, ensure_ascii=False)
    file.close()

