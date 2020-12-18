import markdown
import codecs
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension


css = '''
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!-- 此处省略掉markdown的css样式，因为太长了 -->
</style>
'''

def main(name):
    in_file = 'docs/%s.md' % (name)
    out_file = 'app_src/templates/main/%s.html' % (name)

    input_file = codecs.open(in_file, mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text, extensions=[FencedCodeExtension(), TableExtension()])

    output_file = codecs.open(out_file, "w",encoding="utf-8",errors="xmlcharrefreplace")
    output_file.write(css+html)


if __name__ == "__main__":
    main('updateLog')
    main('how2use')