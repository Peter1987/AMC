from string import Template
import webbrowser

SVG ='<object data="/home/peter/Pictures/1296876353.svg" type="image/svg+xml"></object> '

template = Template("<html>\n<body>\n<h1>\n${name}\n</h1>\n</body>\n</html>")
#template = template.substitute(dict(name='Dinsdale'))
template = template.substitute(dict(name=SVG))



page = open('test.html','w')
page.write(str(template))
page.close()


webbrowser.open_new("test.html")