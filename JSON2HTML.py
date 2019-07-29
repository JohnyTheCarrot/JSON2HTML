import json, sys

print("\033[1;34;40m======================================================================================================")
print("\033[1;34;40m __ __  ______  ___ ___  _          ______  ____    ____  ____   _____ ____ ____  _        ___  ____  ")
print("\033[1;34;40m|  |  ||      ||   |   || |        |      ||    \  /    ||    \ / ___/|    \    || |      /  _]|    \ ")
print("\033[1;34;40m|  |  ||      || _   _ || |        |      ||  D  )|  o  ||  _  (   \_ |  o  )  | | |     /  [_ |  D  )")
print("\033[1;34;40m|  _  ||_|  |_||  \_/  || |___     |_|  |_||    / |     ||  |  |\__  ||   _/|  | | |___ |    _]|    / ")
print("\033[1;34;40m|  |  |  |  |  |   |   ||     |      |  |  |    \ |  _  ||  |  |/  \ ||  |  |  | |     ||   [_ |    \ ")
print("\033[1;34;40m|  |  |  |  |  |   |   ||     |      |  |  |  .  \|  |  ||  |  |\    ||  |  |  | |     ||     ||  .  \\")
print("\033[1;34;40m|__|__|  |__|  |___|___||_____|      |__|  |__|\_||__|__||__|__| \___||__| |____||_____||_____||__|\_|")
print("\033[1;34;40m======================================================================================================")
print("\033[1;34;40mMade by JohnyTheCarrot.\033[1;37;40m")
print("\033[1;34;40mhttps://github.com/JohnyTheCarrot/JSON2HTML\n")

error_msg = "An error occured. If you're a visitor, this should be fixed soon. If you're an administator, please check your console."

def from_json(code, to_replace = []):
    """
    Use this to transpile
    """
    html = "<html>"
    #f = open(filename, "r").read()
    #code = json.loads(filename)
    if 'head' in code:
        head = load_head(code["head"], to_replace)
        if head is None:
            return error(error_msg)
        html+=head
    if 'body' in code:
        body = load_body(code["body"], to_replace)
        if body is None:
            return error(error_msg)
        html+=body
    html+="\n</html>"
    return html

def error(error: str):
    return "<h1>JSON2HTML Error</h1><h3>{}</h3>".format(error)

def from_json_file(filename: str, to_replace = []):
    try:
        f = open(filename, "r").read()
        try:
            code = json.loads(f)
        except json.decoder.JSONDecodeError:
            return error("Invalid JSON.")
        return from_json(code, to_replace)
    except FileNotFoundError:
        return error("Not Found."), 404

def load_head(code, to_replace = []):
    html = "<head>"
    if 'title' in code:
        to_add = f"<title>{code['title']}</title>"
        for replace_node in to_replace:
            to_add.replace(str(list(replace_node.items())[0][0]), str(list(replace_node.items())[0][1]))
        html+=to_add
    if 'style' in code:
        to_add = f"<style>{code['style']}</style>"
        for replace_node in to_replace:
            to_add.replace(str(list(replace_node.items())[0][0]), str(list(replace_node.items())[0][1]))
        html+=to_add
    if 'links' in code:
        if not isinstance(code["links"], type([])):
            fatal(f"'links' object must be of type array")
            fatal("Code:")
            fatal("\033[1;31;40m{}".format(str(code)))
            return None
        for link in code['links']:
            returned_link = load_link(link)
            if returned_link is None:
                return error(error_msg)
            html+=returned_link
    if 'scripts' in code:
        if not isinstance(code["scripts"], type([])):
            fatal(f"'scripts' object must be of type array")
            fatal("Code:")
            fatal("\033[1;31;40m{}".format(str(code)))
            return None
        for scripts in code['scripts']:
            returned_script = load_script(scripts)
            if returned_script is None:
                return error(error_msg)
            html+=returned_script
    html+="</head>"
    return html

def load_body(code, to_replace = []):
    html = "<body>"
    for element in code:
        el = handle_element(element, to_replace=to_replace)
        if el is None:
            return None
        html+=""+el
    html+="</body>"
    return html

def handle_element(element, to_replace = []):
    if 'type' not in element:
        fatal("Missing 'type' in element.")
        fatal("Code:")
        fatal("\033[1;31;40m{}".format(str(element)))
        return None
    _type = element["type"]
    if _type in ["h1", "h2", "h3", "h4", "h5", "h6", "p"]:
        return load_text(element, to_replace)
    elif _type == "div":
        return load_div(element, to_replace)
    elif _type == "img":
        return load_img(element)
    elif _type == "table":
        return load_table(element, to_replace)
    elif _type == "hr":
        return load_hr(element)
    elif _type == "br":
        return load_br(element)
    elif _type == "a" or _type == "nav" or _type == "ul" or _type == "li" or _type == "button" or _type == "span":
        return load_div(element, to_replace)
    elif _type == "pure":
        return load_pure(element, to_replace)
    elif _type == "input":
        return load_input(element, to_replace)
    elif _type == "iframe":
        return load_iframe(element)
    fatal("Unknown type: {}".format(_type))

def load_text(code, to_replace = []):
    html = "<{} {}>{}</{}>" if 'arguments' in code else "<{}>{}</{}>"
    _type = code["type"]
    arguments = ""
    if 'arguments' in code:
        for argument in code["arguments"]:
            arguments+="{}=\"{}\"".format(list(argument.items())[0][0], list(argument.items())[0][1])
    content = code["content"] if 'content' in code else ""
    for replace_node in to_replace:
        content = content.replace(str(list(replace_node.items())[0][0]), str(list(replace_node.items())[0][1]))
    if 'content' not in code or content == "":
        warning("Your content is either empty or undefined, is this normal?")
        warning("Code:")
        warning("\033[1;33;40m"+str(code))
    if 'arguments' in code:
        return html.format(_type, arguments, content, _type)
    return html.format(_type, content, _type)

def load_div(code, to_replace = []):
    html = "<{} {}>{}</{}>" if 'arguments' in code else "<{}>{}</{}>"
    _type = code["type"]
    arguments = ""
    if 'arguments' in code:
        for argument in code["arguments"]:
            arguments+="{}=\"{}\"".format(list(argument.items())[0][0], list(argument.items())[0][1])
    if 'children' not in code:
        fatal("Missing 'children' in div element.")
        fatal("Code:")
        fatal("\033[1;31;40m{}".format(str(code)))
        return None
    children = ""
    for child in code["children"]:
        el = handle_element(child, to_replace)
        if el is None:
            return None
        children+=el
    if 'arguments' in code:
        return html.format(_type, arguments, children, _type)
    return html.format(_type, children, _type)

def load_img(code):
    if 'src' not in code:
        fatal("Missing 'src' in img element.")
        fatal("Code:")
        fatal("\033[1;31;40m{}".format(str(code)))
        return None
    src = code["src"]
    arguments = ""
    if 'arguments' in code:
        for argument in code["arguments"]:
            arguments+="{}=\"{}\"".format(list(argument.items())[0][0], list(argument.items())[0][1])
    html = "<img src=\"{}\"/>" if 'arguments' not in code else "<img src=\"{}\" {}/>"
    if 'arguments' in code:
        return html.format(src, arguments)
    return html.format(src)

def load_iframe(code):
    if 'src' not in code:
        fatal("Missing 'src' in img iframe.")
        fatal("Code:")
        fatal("\033[1;31;40m{}".format(str(code)))
        return None
    src = code["src"]
    arguments = ""
    if 'arguments' in code:
        for argument in code["arguments"]:
            arguments+="{}=\"{}\"".format(list(argument.items())[0][0], list(argument.items())[0][1])
    html = "<iframe src=\"{}\"></iframe>" if 'arguments' not in code else "<iframe src=\"{}\" {}></iframe>"
    if 'arguments' in code:
        return html.format(src, arguments)
    return html.format(src)

def load_table(code, to_replace = []):
    if 'table_headers' not in code:
        fatal("Missing 'table_headers' in table element.")
        fatal("Code:")
        fatal("\033[1;31;40m{}".format(str(code)))
        return None
    instance = 0
    for table_header in code["table_headers"]:
        if not isinstance(table_header, str):
            fatal(f"table_header at index {instance} must be of type string")
            fatal("Code:")
            fatal("\033[1;31;40m{}".format(str(code)))
            return None
        instance+=1
    arguments = ""
    if 'arguments' in code:
        for argument in code["arguments"]:
            arguments+="{}=\"{}\"".format(list(argument.items())[0][0], list(argument.items())[0][1])
    html = "<table>" if 'arguments' not in code else "<table {}>"
    html+="<tr>"
    for table_header in code["table_headers"]:
        to_add = f"<th>{table_header}</th>"
        for replace_node in to_replace:
            to_add.replace(str(list(replace_node.items())[0][0]), str(list(replace_node.items())[0][1]))
        html+=to_add
    html+="</tr>"
    table_data_instance = 0
    if 'table_data' in code:
        if isinstance(code["table_data"], str):
            for replace_node in to_replace:
                if code["table_data"] == list(replace_node.items())[0][0]:
                    code["table_data"] = list(replace_node.items())[0][1]
        for table_data_field in code["table_data"]:
            html+="<tr>"
            if not isinstance(table_data_field, type([])):
                fatal(f"table_data at index {table_data_instance} must be of type {type([])}")
                fatal("Code:")
                fatal("\033[1;31;40m{}".format(str(code)))
                return None
            if len(table_data_field) != len(code["table_headers"]):
                fatal(f"table_data at index {table_data_instance} must be the same length as the table header array")
                fatal("Code:")
                fatal("\033[1;31;40m{}".format(str(code)))
                return None
            for td_field in table_data_field:
                to_add = f"<td>{td_field}</td>"
                for replace_node in to_replace:
                    to_add.replace(str(list(replace_node.items())[0][0]), str(list(replace_node.items())[0][1]))
                html+=to_add
            table_data_instance+=1
            html+="</tr>"
    html+="</table>"
    return html

def load_hr(code):
    return "<hr>"

def load_br(code):
    return "<br>"

def load_link(code):
    html = "<link "
    if 'rel' in code:
        html+=f"rel=\"{code['rel']}\""
    if 'href' in code:
        html+=f"href=\"{code['href']}\""
    if 'crossorigin' in code:
        html+=f"crossorigin=\"{code['crossorigin']}\""
    if 'integrity' in code:
        html+=f"integrity=\"{code['integrity']}\""
    return html+"/>"

def load_script(code):
    html = "<script>"
    if 'code' in code:
        html+=code
    return html+"</script>"

def load_pure(code, to_replace):
    if 'content' not in code:
        fatal("Field 'content' is missing.")
        fatal("Code:")
        fatal("\033[1;31;40m{}".format(str(code)))
        return None
    content = code["content"]
    for replace_node in to_replace:
        content = content.replace(str(list(replace_node.items())[0][0]), str(list(replace_node.items())[0][1]))
    return content

def load_input(code, to_replace):
    html = "<input {}/>" if 'arguments' in code else "<input/>"
    arguments = ""
    if 'arguments' in code:
        for argument in code["arguments"]:
            arguments+="{}=\"{}\"".format(list(argument.items())[0][0], list(argument.items())[0][1])
    if arguments != "":
        return html.format(arguments)
    else:
        return html

def fatal(error: str):
    print("[JSON2HTML] \033[1;37;41m[FATAL]:\033[1;37;40m {}\033[1;37;40m".format(error))

def warning(warning: str):
    print("[JSON2HTML] \033[1;37;43m[WARNING]:\033[1;37;40m {}\033[1;37;40m".format(warning))