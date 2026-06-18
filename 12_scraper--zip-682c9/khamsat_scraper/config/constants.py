"""
ثوابت النظام ومحددات CSS لاستخراج بيانات خمسات
هذا الملف يحتوي على جميع محددات CSS والثوابت المستخدمة في الاستخراج
"""

# ============================================
# محددات CSS للصفحة الرئيسية (قائمة الطلبات)
# ============================================
LIST_SELECTORS = {
    'request_item': [
        'div.thread--list-item',
        'div.thread-item',
        'li.request-item',
        'div.request-card',
        '[class*="thread"]',
        '[class*="request"]'
    ],
    'title': [
        'a.thread-title',
        'a.request-title',
        'h3 a',
        'h2 a',
        'a[href*="/community/requests/"]',
        '.title a'
    ],
    'time': [
        'small.timeago',
        'span.timeago',
        'span[class*="time"]',
        'small[class*="time"]',
        '.meta-time',
        '[class*="ago"]'
    ],
    'author': [
        'a.username',
        'span.author',
        '.user-name',
        '[class*="user"] a'
    ],
    'category': [
        'span.category',
        'a.category-link',
        '.request-category'
    ]
}

# ============================================
# محددات CSS لصفحة التفاصيل
# ============================================
DETAIL_SELECTORS = {
    'title': [
        'h1.thread-title',
        'h1.request-title',
        'h1',
        '.title h1'
    ],
    'content': [
        'div.thread-content',
        'div.post-content',
        'div.request-description',
        '.content',
        '.description',
        '[class*="content"]'
    ],
    'budget': [
        'span.budget',
        'div.budget',
        '.price',
        '[class*="budget"]',
        '[class*="price"]'
    ],
    'skills': [
        'div.skills',
        'span.skill',
        '.tags a',
        '[class*="skill"]',
        '.requirements li'
    ],
    'attachments': [
        'div.attachments',
        'ul.attachments li',
        '[class*="attach"]'
    ],
    'deadline': [
        'span.deadline',
        'div.deadline',
        '[class*="deadline"]',
        '[class*="due"]'
    ],
    'proposals_count': [
        'span.proposals',
        'div.proposals-count',
        '[class*="proposal"]'
    ]
}

# ============================================
# محددات CSS للـ Pagination
# ============================================
PAGINATION_SELECTORS = {
    'next_button': [
        'a.next',
        'li.next a',
        '.pagination-next a',
        '[rel="next"]',
        'a[aria-label="التالي"]'
    ],
    'page_number': [
        'li.page-item a',
        '.pagination li a',
        '[class*="page"] a'
    ],
    'current_page': [
        'li.active',
        '.pagination .active',
        '[class*="active"]'
    ]
}

# ============================================
# ثوابت النصوص العربية
# ============================================
ARABIC_TIME_KEYWORDS = {
    'now': ['الآن', 'حالياً', 'لتو'],
    'minute': ['دقيقة', 'دقيقتين', 'دقائق'],
    'hour': ['ساعة', 'ساعتين', 'ساعات'],
    'day': ['يوم', 'يومين', 'أيام', 'يوماً'],
    'week': ['أسبوع', 'أسبوعين', 'أسابيع', 'اسبوع'],
    'month': ['شهر', 'شهرين', 'أشهر'],
    'year': ['سنة', 'سنتين', 'سنوات', 'عام'],
    'ago': ['منذ', 'قبل']
}

# ============================================
# رسائل النظام
# ============================================
MESSAGES = {
    'start': '🚀 بدء تشغيل برنامج استخراج بيانات خمسات...',
    'fetching': '📡 جاري جلب الصفحة {}...',
    'parsing': '🔍 جاري تحليل البيانات...',
    'details': '📄 جاري استخراج تفاصيل الطلب: {}',
    'saving': '💾 جاري حفظ البيانات...',
    'complete': '✅ اكتمل الاستخراج بنجاح!',
    'error': '❌ حدث خطأ: {}',
    'warning': '⚠️ تحذير: {}',
    'stop_condition': '🛑 تم الوصول لشرط التوقف ({} يوم)',
    'no_more_pages': '📄 لا توجد صفحات إضافية',
    'found_requests': '📊 تم العثور على {} طلب',
    'filtered_requests': '🎯 تم تصفية {} طلب مطابق للشروط'
}

# ============================================
# أسماء الأعمدة في الملفات
# ============================================
CSV_COLUMNS = [
    'id',
    'title',
    'content',
    'author',
    'category',
    'budget',
    'skills',
    'attachments',
    'deadline',
    'proposals_count',
    'raw_time',
    'parsed_time',
    'url',
    'extracted_at'
]

JSON_FIELDS = [
    'id',
    'title',
    'content',
    'author',
    'category',
    'budget',
    'skills',
    'attachments',
    'deadline',
    'proposals_count',
    'time_info',
    'url',
    'metadata'
]
