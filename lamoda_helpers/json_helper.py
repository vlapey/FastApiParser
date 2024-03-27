import json


def get_script_with_page_state_json(soup):
    script = next(x for x in soup.findAll('script') if x.text.find("var __NUXT__") != -1)

    return script


def get_json_string_by_marker_string(script, start_marker_string, end_marker_string, end_offset = 0):
    start_index_of_pagination_section = script.text.find(start_marker_string) + len(start_marker_string)
    end_index_of_pagination_section = script.text.find(end_marker_string, start_index_of_pagination_section) + end_offset
    json_string = script.text[start_index_of_pagination_section:end_index_of_pagination_section]

    return json_string


def get_categories_from_json_string(json_string):
    json_object = json.loads(json_string)
    categories_json = json_object[0]['nodes']
    categories = list(map(lambda x: {'name': x['info']['title'], 'href': x['info']['url']}, categories_json))

    return categories


def get_count_of_pages_from_json_string(json_string):
    json_object = json.loads(json_string)
    count_of_pages = int(json_object['pages'])

    return count_of_pages
