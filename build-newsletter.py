# -*- coding: utf-8 -*-
import csv
from datetime import datetime
from categorized_info import categorized_info
from utils import downloadFiles

# Define constants
DATE_FORMAT = "%d-%m-%Y"
DATE_FROM = "01-01-2023"  # Change this date as needed

TOP_BANNER = "https://innovacionyrobotica.com/newsletter_red-inv-robotica/banner_1-min.png"
BOTTOM_BANNER = "https://innovacionyrobotica.com/newsletter_red-inv-robotica/banner_2-min.png"
DEFAULT_IMG = "https://innovacionyrobotica.com/newsletter_red-inv-robotica/single-robot_0-min.png"
NUMERO_BOLETIN = "4"

# Load CSV data
news_data = []
with open('Información para el canal de investigadores (Respuestas) - Respuestas de formulario 1.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        news_data.append(row)

# Categorize news
categorized_news = {section: [] for section in [
    "Avances tecnológicos y proyectos destacados",
    "Propuesta para entrevista",
    "Eventos y conferencias",
    "Recursos educativos",
    "Oportunidades de financiamiento",
    "Propuesta de colaboración",
    "Noticias y tendencias",
    "Otros"
]}

for news in news_data:
    news_date = datetime.strptime(news['Marca temporal'], DATE_FORMAT)
    if news_date >= datetime.strptime(DATE_FROM, DATE_FORMAT):
        section = news.get('El contenido que deseas compartir es', 'Otros')
        categorized_news[section].append(news)
        downloadFiles(news)

# Filter news based on date
# filtered_news = {section: [] for section in categorized_news}
# 
# for section, news_list in categorized_news.items():
#     for news in news_list:
#         news_date = datetime.strptime(news['Marca temporal'], DATE_FORMAT)
#         if news_date >= datetime.strptime(DATE_FROM, DATE_FORMAT):
#             filtered_news[section].append(news)

# Generate HTML
with open('newsletter.html', 'w') as html_file:
    html_content = f'''<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <!-- Add your head content here -->
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Boletín mensual #{NUMERO_BOLETIN}</title>
                            <style>
                                body {{
                                    margin: 0;
                                    padding: 0;
                                    font-family: 'Roboto', Arial, sans-serif;
                                    background-color: #000;
                                    color: #fff;
                                }}
                            </style>
                            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400&display=swap" rel="stylesheet">
                        </head>
                        <body style="margin: 0; padding: 0; font-family: 'Roboto', Arial, sans-serif; background-color: #6198d7; color: #fff;">

                            <!-- Top Banner -->
                            <div style=" ">
                                <img src="{TOP_BANNER}" alt="Top Banner" style="max-width: 100%;">
                            </div>
                    '''

    for section, news_list in categorized_news.items(): #filtered_news.items():
        if news_list:
#             html_content += f'''
#             <div class="section">
#                 <h2>{section}</h2>
#                 <div class="columns">
#             '''

            html_content += f'''
            <div style="padding: 20px; background-color: #6198d7;">
                <h2 style="font-size: 24px;background-color: #6198d7;">{section}</h2>
                <div style="display: flex; flex-wrap: wrap; gap: 20px;">
            '''

            for news_i, news in enumerate(news_list):
#                num_columns = 2 if len(news_list) > 1 else 1
#                column_width = f'width: {100 / num_columns}%;' if num_columns == 2 else 'width: 100%;'
#                html_content += f'''
#                    <div class="column" style="{column_width}">
#                        <img src=f"{news.get('Image URL',DEFAULT_IMG)}" alt="{news['Title']}" style="max-width: 100%; height: auto; margin-bottom: 10px;">
#                        <p>{news['Content']}</p>
#                    </div>
#                '''

                if news_i % 2 == 0:
                    html_content += f'''
                        </div>
                        <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                    '''                    

                html_content += f'''
                    <div style="flex: 1;">
                        <img src="{news.get('Image URL',DEFAULT_IMG) if news.get('Image URL',DEFAULT_IMG) else DEFAULT_IMG}" alt="Imagen de la noticia {news_i}" style="width: 100%; max-width: 100%; height: auto; margin-bottom: 10px;">
                        <h3 style="font-size: 16px; margin-bottom: 5px; text-align: center; ">{news[categorized_info[section]['Title']]}</h3>
                        '''

                for content in categorized_info[section]['Content']:
                    if news[content]:
                        html_content += f'''<p style="font-size: 16px; line-height: 1.5; text-align: justify; ">{news[content]}</p>'''


                html_content += f'''
                    </div>
                    '''

            html_content += '''
                </div>
            </div>
            '''

    html_content += f'''<!-- Bottom Banner -->
                        <div style=""> 
                            <img src="{BOTTOM_BANNER}" alt="Bottom Banner" style="max-width: 100%;">
                        </div>
                        </body>
                        </html>'''

    html_file.write(html_content)

print("HTML file 'newsletter.html' has been generated.")
