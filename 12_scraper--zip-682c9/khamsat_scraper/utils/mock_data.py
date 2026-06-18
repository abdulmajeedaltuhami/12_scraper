"""
بيانات تجريبية لمحاكاة موقع خمسات (Mock Data for Testing)
تستخدم لاختبار البنية البرمجية عندما يكون الموقع محمي بـ Cloudflare
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any

# محاكاة الوقت الحالي
NOW = datetime.now()

def generate_mock_requests() -> List[Dict[str, Any]]:
    """
    توليد بيانات طلبات وهمية مشابهة لخمسات
    
    Returns:
        List[Dict]: قائمة من الطلبات الوهمية
    """
    mock_data = [
        {
            "title": "أحتاج إلى مصمم جرافيك لتصميم شعار شركة",
            "content": "مرحباً، أبحث عن مصمم جرافيك محترف لتصميم شعار لشركة تقنية ناشئة. يجب أن يكون التصميم عصري وبسيط.",
            "budget": "50-100 دولار",
            "skills": ["تصميم جرافيك", "Adobe Illustrator", "تصميم شعارات"],
            "url": "https://khamsat.com/community/requests/1",
            "raw_time": "منذ ساعتين",
            "parsed_time": NOW - timedelta(hours=2),
            "author": "أحمد محمد",
            "attachments_count": 2,
            "proposals_count": 15
        },
        {
            "title": "مطلوب مبرمج بايثون لتطوير سكربت جمع بيانات",
            "content": "أحتاج إلى مبرمج خبير في بايثون لبناء سكريبت web scraping لجمع بيانات من مواقع معينة. يجب أن يدعم pagination و JSON output.",
            "budget": "100-250 دولار",
            "skills": ["Python", "Web Scraping", "BeautifulSoup", "Selenium"],
            "url": "https://khamsat.com/community/requests/2",
            "raw_time": "منذ 5 ساعات",
            "parsed_time": NOW - timedelta(hours=5),
            "author": "سارة علي",
            "attachments_count": 1,
            "proposals_count": 23
        },
        {
            "title": "تطوير موقع ووردبريس متعدد اللغات",
            "content": "أريد تطوير موقع إلكتروني باستخدام ووردبريس يدعم العربية والإنجليزية. يجب أن يكون سريع ومتجاوب مع الجوال.",
            "budget": "200-500 دولار",
            "skills": ["WordPress", "PHP", "تطوير ويب", "تصميم متجاوب"],
            "url": "https://khamsat.com/community/requests/3",
            "raw_time": "منذ يوم واحد",
            "parsed_time": NOW - timedelta(days=1),
            "author": "خالد العمري",
            "attachments_count": 3,
            "proposals_count": 41
        },
        {
            "title": "ترجمة ملف تقني من الإنجليزية للعربية",
            "content": "لدي ملف PDF تقني حوالي 50 صفحة يحتاج ترجمة احترافية من الإنجليزية إلى العربية في مجال الهندسة.",
            "budget": "75-150 دولار",
            "skills": ["ترجمة", "اللغة الإنجليزية", "اللغة العربية", "كتابة تقنية"],
            "url": "https://khamsat.com/community/requests/4",
            "raw_time": "منذ يومين",
            "parsed_time": NOW - timedelta(days=2),
            "author": "منى السيد",
            "attachments_count": 1,
            "proposals_count": 18
        },
        {
            "title": "إنشاء تطبيق موبايل للتجارة الإلكترونية",
            "content": "أبحث عن مطور تطبيقات موبايل لإنشاء تطبيق iOS و Android لمتجر إلكتروني. يجب أن يدعم الدفع الإلكتروني وتتبع الطلبات.",
            "budget": "500-1000 دولار",
            "skills": ["Flutter", "React Native", "تطوير تطبيقات", "Firebase"],
            "url": "https://khamsat.com/community/requests/5",
            "raw_time": "منذ 3 أيام",
            "parsed_time": NOW - timedelta(days=3),
            "author": "فهد الراشد",
            "attachments_count": 5,
            "proposals_count": 67
        },
        {
            "title": "تعديل على كود PHP موجود",
            "content": "لدي نظام إدارة محتوى مبني بـ PHP وأحتاج لإضافة بعض الميزات الجديدة وإصلاح مشاكل في قاعدة البيانات.",
            "budget": "30-60 دولار",
            "skills": ["PHP", "MySQL", "تطوير ويب"],
            "url": "https://khamsat.com/community/requests/6",
            "raw_time": "منذ 4 أيام",
            "parsed_time": NOW - timedelta(days=4),
            "author": "ياسر محمود",
            "attachments_count": 0,
            "proposals_count": 9
        },
        {
            "title": "تصميم هوية بصرية كاملة لمشروع مطعم",
            "content": "مطلوب مصمم محترف لتصميم هوية بصرية شاملة لمطعم جديد تشمل الشعار، القائمة، البطاقات الدعائية، والتغليف.",
            "budget": "150-300 دولار",
            "skills": ["تصميم جرافيك", "هوية بصرية", "Adobe Photoshop", "Illustrator"],
            "url": "https://khamsat.com/community/requests/7",
            "raw_time": "منذ 5 أيام",
            "parsed_time": NOW - timedelta(days=5),
            "author": "ليلى حسن",
            "attachments_count": 2,
            "proposals_count": 34
        },
        {
            "title": "كتابة محتوى تسويقي لمنتج جديد",
            "content": "أحتاج كاتب محتوى محترف لكتابة وصف تسويقي جذاب لمنتج إلكتروني جديد سيتم إطلاقه قريباً.",
            "budget": "25-50 دولار",
            "skills": ["كتابة محتوى", "تسويق إلكتروني", "SEO", "اللغة العربية"],
            "url": "https://khamsat.com/community/requests/8",
            "raw_time": "منذ أسبوع واحد",
            "parsed_time": NOW - timedelta(weeks=1),
            "author": "عمر فاروق",
            "attachments_count": 1,
            "proposals_count": 28
        },
        {
            "title": "إدارة حملات إعلانية على فيسبوك وجوجل",
            "content": "أبحث عن خبير تسويق رقمي لإدارة حملات إعلانية ممولة على منصات فيسبوك وإنستغرام وجوجل أدز.",
            "budget": "100-200 دولار",
            "skills": ["Facebook Ads", "Google Ads", "تسويق إلكتروني", "تحليل بيانات"],
            "url": "https://khamsat.com/community/requests/9",
            "raw_time": "منذ 10 أيام",
            "parsed_time": NOW - timedelta(days=10),
            "author": "نورة القحطاني",
            "attachments_count": 0,
            "proposals_count": 45
        },
        {
            "title": "برمجة لعبة بسيطة للأطفال",
            "content": "مطلوب مطور ألعاب لبرمجة لعبة تعليمية بسيطة للأطفال باستخدام Unity أو محرك ألعاب آخر.",
            "budget": "200-400 دولار",
            "skills": ["Unity", "تطوير ألعاب", "C#", "تصميم ألعاب"],
            "url": "https://khamsat.com/community/requests/10",
            "raw_time": "منذ 15 يوم",
            "parsed_time": NOW - timedelta(days=15),
            "author": "حسن إبراهيم",
            "attachments_count": 3,
            "proposals_count": 12
        },
        {
            "title": "تحليل بيانات إكسل وإنشاء تقارير",
            "content": "لدي مجموعة كبيرة من البيانات في Excel وأحتاج محلل بيانات لاستخراج insights وإنشاء تقارير مرئية.",
            "budget": "50-100 دولار",
            "skills": ["Excel", "تحليل بيانات", "Power BI", "إحصاء"],
            "url": "https://khamsat.com/community/requests/11",
            "raw_time": "منذ 20 يوم",
            "parsed_time": NOW - timedelta(days=20),
            "author": "ريم عبدالله",
            "attachments_count": 2,
            "proposals_count": 16
        },
        {
            "title": "إنشاء بوت تليجرام للرد التلقائي",
            "content": "أحتاج مبرمج لإنشاء بوت على تليجرام يقوم بالرد التلقائي على الأسئلة الشائعة وتوجيه المستخدمين.",
            "budget": "40-80 دولار",
            "skills": ["Python", "Telegram Bot API", "برمجة"],
            "url": "https://khamsat.com/community/requests/12",
            "raw_time": "منذ شهر واحد",
            "parsed_time": NOW - timedelta(days=30),
            "author": "ماجد السعيد",
            "attachments_count": 0,
            "proposals_count": 21
        }
    ]
    
    return mock_data


def get_mock_pagination_info() -> Dict[str, Any]:
    """
    الحصول على معلومات الترقيم الوهمية
    
    Returns:
        Dict: معلومات الصفحات
    """
    return {
        "current_page": 1,
        "total_pages": 5,
        "total_requests": 58,
        "has_next": True,
        "has_prev": False,
        "next_url": "https://khamsat.com/community/requests?page=2",
        "prev_url": None
    }


if __name__ == "__main__":
    # اختبار الدوال
    print("=" * 80)
    print("اختبار البيانات الوهمية")
    print("=" * 80)
    
    requests = generate_mock_requests()
    print(f"\n✅ عدد الطلبات المُولدة: {len(requests)}")
    
    print("\n📋 عينة من الطلبات:")
    for i, req in enumerate(requests[:3], 1):
        print(f"\n{i}. {req['title']}")
        print(f"   الوقت: {req['raw_time']}")
        print(f"   الميزانية: {req['budget']}")
        print(f"   المقترحات: {req['proposals_count']}")
    
    pagination = get_mock_pagination_info()
    print(f"\n📄 معلومات الترقيم:")
    print(f"   الصفحة الحالية: {pagination['current_page']}")
    print(f"   إجمالي الصفحات: {pagination['total_pages']}")
    print(f"   إجمالي الطلبات: {pagination['total_requests']}")
