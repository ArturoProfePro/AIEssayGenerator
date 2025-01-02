import g4f
from docx import Document
from docx.shared import Pt
from docx.enum.style import WD_STYLE_TYPE

def generate_plan(topic):
    """Генерирует план реферата с помощью GPT."""
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            provider= g4f.Provider.Copilot,
            messages=[
                {"role": "system", "content": "Ты должен написать план реферата. И ответ должен только быть в виде нумеровонного списка пунктов план, без подробностей."},
                {"role": "user", "content": f"Составь краткий план реферата из 8 пунктов на тему: {topic}"},
            ],
        )
        return response
    except Exception as e:
        print(f"Ошибка при генерации плана: {e}")
        return None

def generate_content(plan_item, plan):
    """Генерирует текст для пункта плана, сохраняя контекст."""

    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            provider= g4f.Provider.Copilot,
            messages=[
                {"role": "system", "content": "Ты - опытный автор научных текстов. Напиши подробный текст для данного пункта плана реферата, учитывая предыдущий контекст."},
                {"role": "user", "content": f"Напиши Пункт плана реферата: {plan_item} из Плана {plan}. Но в ответе не пиши назв пункта, только содержание ничего лишнего"},
            ],
        )
        return response
    except Exception as e:
        print(f"Ошибка при генерации контента: {e}")
        create_docx(topic, plan, content)
        print(f"Реферат сохранен в файл referat_{topic.replace(' ', '_')}.docx")
       

        return None

def create_docx(topic, plan, content):
    """Создает документ docx с рефератом."""
    document = Document()

    # Стили
    styles = document.styles
    # Стиль заголовка 1
    heading1_style = styles.add_style('Heading1Custom', WD_STYLE_TYPE.PARAGRAPH)
    heading1_style.base_style = styles['Heading 1']
    heading1_font = heading1_style.font
    heading1_font.name = 'Times New Roman'
    heading1_font.size = Pt(16)
    heading1_font.bold = True

    # Стиль обычного текста
    normal_style = styles.add_style('NormalCustom', WD_STYLE_TYPE.PARAGRAPH)
    normal_style.base_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(14)


    document.add_heading(f"Реферат на тему: {topic}", level=1)

    document.add_page_break()

    document.add_paragraph("План", style='Heading1Custom')
    
    for iplan in plan:
        document.add_paragraph(iplan, style='Heading1Custom')

    document.add_page_break()

    for i, (plan_item, item_content) in enumerate(zip(plan, content)):
        document.add_paragraph(plan_item, style='Heading1Custom')
        document.add_paragraph(item_content, style='NormalCustom')
        

    document.save(f"referat_{topic.replace(' ', '_')}.docx")

if __name__ == "__main__":
    topics = [
        "Периодический закон и периодическая система. Периодичность изменения свойств элементов в периодах и группах;",
"Состав и строение атома. Радиоактивность;",
        "Катализ. Гомогенный и гетерогенный катализ. Катализаторы;",
        "Экологическое воздействие оксидов азота, нитратов и диоксида серы на окружающую среду;",
        "Проблемы охраны окружающей среды при производстве металлов;",

        #"Виды природопользования;",
        #"Геоэкономика;",
        #"Геополитика;",
        #"Территориальные модели мирового хозяйства;",

        #"Классификация Углеводов.Свойства и Функции;",
        #"Жиры и Липиды;",
        #"Классификация белков,Строение белков;",
        #"Строение молукулы ДНК,Функция ДНК;",
    ]
    for topic in topics:
        plan_text = generate_plan(topic)


        if plan_text:
            print("Сгенерированный план:")
            print(plan_text)

            try:
                plan = [item.strip() for item in plan_text.split('\n') if item.strip()] # Разделение на пункты
                content = []
                context = ""
                for plan_item in plan:
                    item_content = generate_content(plan_item, plan)
                    if item_content:
                        content.append(item_content)
                        context += item_content + "\n"
                        print(f'добавлен {plan_item}')
                    else:
                        print("Ошибка при генерации контента для пункта плана.")
                        exit()

                create_docx(topic, plan, content)
                print(f"Реферат сохранен в файл referat_{topic.replace(' ', '_')}.docx")
            except ValueError:
                print("Ошибка: Некорректный формат плана, убедитесь что GPT вернул нумерованный список")
        else:
            print("Не удалось сгенерировать план.")