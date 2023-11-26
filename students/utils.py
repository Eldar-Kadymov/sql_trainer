from datetime import datetime
import pytz

def format_date(submission_date):
    moscow_timezone = pytz.timezone('Europe/Moscow')

    submission_date_moscow = submission_date.astimezone(moscow_timezone)

    formatted_date = submission_date_moscow.strftime('%d %b %Y, %H:%M:%S')

    months_translation = {
        'Jan': 'Янв',
        'Feb': 'Фев',
        'Mar': 'Мар',
        'Apr': 'Апр',
        'May': 'Май',
        'Jun': 'Июн',
        'Jul': 'Июл',
        'Aug': 'Авг',
        'Sep': 'Сен',
        'Oct': 'Окт',
        'Nov': 'Ноя',
        'Dec': 'Дек'
    }

    for eng_month, rus_month in months_translation.items():
        formatted_date = formatted_date.replace(eng_month, rus_month)

    return formatted_date
