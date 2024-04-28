from bs4 import BeautifulSoup
import cssutils
import os

def remove_unused_css(html_file, css_file):
    # Парсим HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    html_selectors = set()
    for tag in soup.find_all(True):
        html_selectors.add(tag.name)
        if 'class' in tag.attrs:
            html_selectors.update(tag['class'])
        if 'id' in tag.attrs:
            html_selectors.add('#' + tag['id'])

    # Парсим CSS
    css_parser = cssutils.CSSParser()
    with open(css_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    css = css_parser.parseString(css_content)

    # Удаляем неиспользуемые селекторы
    new_css = cssutils.css.CSSStyleSheet()
    for rule in css:
        if isinstance(rule, cssutils.css.CSSStyleRule):
            selectors = rule.selectorText.split(',')
            keep_rule = False
            for selector in selectors:
                selector = selector.strip()
                if selector.startswith('.') or selector.startswith('#'):
                    if selector in html_selectors or (selector[1:] in html_selectors):
                        keep_rule = True
                        break
                else:
                    keep_rule = True
            if keep_rule:
                new_css.add(rule)
        else:
            new_css.add(rule)
    
    # Создаем новый CSS-текст с пустыми строками между правилами
    new_css_text = '\n\n'.join(rule.cssText for rule in new_css.cssRules)

    # Сохраняем изменения в новом CSS файле
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(new_css_text)

    return css_file

# Определяем текущую директорию
current_directory = os.path.dirname(os.path.abspath(__file__))

# Формируем абсолютные пути к файлам HTML и CSS
html_file = os.path.join(current_directory, 'index.html')
css_file = os.path.join(current_directory, 'css', 'style.css')

# Пример использования
remove_unused_css(html_file, css_file)

print("Ваш файл успешно изменен")
