import json
import os
from tempfile import mkstemp, mkdtemp

from selenium.webdriver import PhantomJS


def generate_image(structure):
    image_path = os.path.join(mkdtemp(), 'okc.png')
    html_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'okc.html',
    )
    url = 'file://{}'.format(html_path)
    driver = PhantomJS(service_log_path=mkstemp()[1])
    driver.set_window_size(2000, 500)
    driver.get(url)
    driver.execute_script('setText({});'.format(json.dumps(structure)))
    driver.set_window_size(*driver.execute_script('return getSize();'))
    driver.save_screenshot(image_path)
    return image_path


if __name__ == '__main__':
    from blank import get_structure
    print generate_image([segment.context() for segment in get_structure()])
