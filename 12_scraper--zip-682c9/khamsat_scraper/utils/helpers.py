"""
دوال مساعدة عامة لبرنامج استخراج بيانات خمسات
تتضمن دوال لتنظيف النصوص، التأخير العشوائي، تطبيع الروابط، إلخ.
"""

import random
import asyncio
import re
from urllib.parse import urljoin, urlparse


async def random_delay(min_seconds=1.5, max_seconds=3.5):
    """
    تأخير عشوائي لتجنب الحظر
    
    Args:
        min_seconds (float): الحد الأدنى للتأخير بالثواني
        max_seconds (float): الحد الأقصى للتأخير بالثواني
    """
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)


def clean_text(text):
    """
    تنظيف النص من المسافات الزائدة والرموز غير المرغوبة
    
    Args:
        text (str): النص الأصلي
        
    Returns:
        str: النص المنظف
    """
    if not text:
        return ""
    
    # إزالة المسافات الزائدة من البداية والنهاية
    text = text.strip()
    
    # استبدال المسافات المتعددة بمسافة واحدة
    text = re.sub(r'\s+', ' ', text)
    
    # إزالة الرموز غير المطبوعة (مع تحسين الأداء باستخدام list comprehension)
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
    
    return text


def clean_text_fast(text):
    """
    نسخة محسنة للأداء لتنظيف النصوص الكبيرة
    
    Args:
        text (str): النص الأصلي
        
    Returns:
        str: النص المنظف
    """
    if not text:
        return ""
    
    # استخدام translate لإزالة الأحرف غير المطبوعة - أسرع بكثير
    printable_chars = set(chr(i) for i in range(32, 127)) | {'\n', '\t'} | set(range(160, 55296))
    text = ''.join(char if ord(char) < 128 or char in '\n\t' or ord(char) > 159 else '' for char in text)
    
    # استبدال المسافات المتعددة بمسافة واحدة
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def normalize_url(base_url, relative_url):
    """
    تطبيع الرابط وتحويله إلى رابط مطلق
    
    Args:
        base_url (str): الرابط الأساسي للموقع
        relative_url (str): الرابط النسبي
        
    Returns:
        str: الرابط المطلق الكامل
    """
    if not relative_url:
        return ""
    
    # إذا كان الرابط يبدأ بـ http أو https، نرجعه كما هو
    if relative_url.startswith(('http://', 'https://')):
        return relative_url
    
    # تحويل الرابط النسبي إلى مطلق
    absolute_url = urljoin(base_url, relative_url)
    
    return absolute_url


def extract_number_from_text(text):
    """
    استخراج رقم من نص
    
    Args:
        text (str): النص الذي يحتوي على الرقم
        
    Returns:
        int: الرقم المستخرج أو None
    """
    if not text:
        return None
    
    # البحث عن أول رقم في النص
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    
    return None


def format_number(number):
    """
    تنسيق رقم بإضافة فواصل الآلاف
    
    Args:
        number (int): الرقم
        
    Returns:
        str: الرقم منسقاً
    """
    if number is None:
        return "غير محدد"
    
    return f"{number:,}"


def truncate_text(text, max_length=100, suffix="..."):
    """
    قص النص إذا تجاوز طول معين
    
    Args:
        text (str): النص الأصلي
        max_length (int): الطول الأقصى
        suffix (str): اللاحقة للإضافة عند القص
        
    Returns:
        str: النص المقصوص
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def sanitize_filename(filename):
    """
    تنظيف اسم الملف من الأحرف غير المسموح بها
    
    Args:
        filename (str): اسم الملف الأصلي
        
    Returns:
        str: اسم الملف المنظف
    """
    # الأحرف غير المسموح بها في أسماء الملفات
    invalid_chars = r'[<>:"/\\|?*]'
    
    # استبدال الأحرف غير المسموح بها بشرطة سفلية
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # إزالة المسافات الزائدة
    sanitized = sanitized.strip()
    
    # تحديد الطول الأقصى لاسم الملف
    max_length = 255
    if len(sanitized) > max_length:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        sanitized = name[:max_length - len(ext) - 1] + '.' + ext if ext else name[:max_length]
    
    return sanitized


def calculate_statistics(requests_list):
    """
    حساب إحصائيات عامة عن قائمة الطلبات
    
    Args:
        requests_list (list): قائمة الطلبات
        
    Returns:
        dict: قاموس الإحصائيات
    """
    if not requests_list:
        return {
            'total': 0,
            'with_budget': 0,
            'without_budget': 0,
            'avg_proposals': 0,
            'oldest_date': None,
            'newest_date': None
        }
    
    total = len(requests_list)
    with_budget = sum(1 for req in requests_list if req.get('budget'))
    without_budget = total - with_budget
    
    proposals_list = [
        req.get('proposals_count', 0) 
        for req in requests_list 
        if req.get('proposals_count') is not None
    ]
    avg_proposals = sum(proposals_list) / len(proposals_list) if proposals_list else 0
    
    dates = [
        req.get('parsed_time') 
        for req in requests_list 
        if req.get('parsed_time')
    ]
    oldest_date = min(dates) if dates else None
    newest_date = max(dates) if dates else None
    
    return {
        'total': total,
        'with_budget': with_budget,
        'without_budget': without_budget,
        'avg_proposals': round(avg_proposals, 2),
        'oldest_date': oldest_date,
        'newest_date': newest_date
    }


def chunks(lst, n):
    """
    تقسيم قائمة إلىChunks بحجم معين
    
    Args:
        lst (list): القائمة الأصلية
        n (int): حجم كل chunk
        
    Yields:
        list: chunk من القائمة
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def fetch_all_with_semaphore(semaphore, coroutines):
    """
    تنفيذ جميع coroutines مع semaphore للتحكم بالتزامن
    
    Args:
        semaphore (asyncio.Semaphore): semaphore للتحكم
        coroutines (list): قائمة coroutines للتنفيذ
        
    Returns:
        list: نتائج التنفيذ
    """
    async def wrapped_coroutine(coro):
        async with semaphore:
            return await coro
    
    tasks = [wrapped_coroutine(coro) for coro in coroutines]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return results
