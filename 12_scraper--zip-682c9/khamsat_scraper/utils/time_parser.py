"""
محلل الوقت العربي الذكي
يحول النصوص الزمنية العربية إلى كائنات datetime
"""

from datetime import datetime, timedelta
import re


class ArabicTimeParser:
    """
    فئة لتحليل النصوص الزمنية العربية وتحويلها إلى datetime
    
    تدعم الصيغ التالية:
    - منذ 3 أيام
    - منذ 5 ساعات
    - منذ 10 دقائق
    - منذ أسبوع / أسبوعين / أسابيع
    - منذ شهر / شهرين / أشهر
    - منذ سنة / سنتين / سنوات
    - منذ الآن / حالياً
    - تراكيب معقدة: منذ 3 أيام و 5 ساعات
    """
    
    # خرائط الكلمات العربية للأرقام والوحدات الزمنية
    TIME_UNITS = {
        'دقيقة': 'minutes',
        'دقيقتين': 'minutes',
        'دقائق': 'minutes',
        'ساعة': 'hours',
        'ساعتين': 'hours',
        'ساعات': 'hours',
        'يوم': 'days',
        'يومين': 'days',
        'أيام': 'days',
        'يوماً': 'days',
        'أسبوع': 'weeks',
        'أسبوعين': 'weeks',
        'أسابيع': 'weeks',
        'اسبوع': 'weeks',
        'اسبوعين': 'weeks',
        'شهر': 'months',
        'شهرين': 'months',
        'أشهر': 'months',
        'سنة': 'years',
        'سنتين': 'years',
        'سنوات': 'years',
        'عام': 'years',
        'أعوام': 'years'
    }
    
    # كلمات تشير إلى الحاضر
    PRESENT_KEYWORDS = ['الآن', 'حالياً', 'لتو', 'الآن']
    
    # كلمات تشير إلى الماضي
    PAST_KEYWORDS = ['منذ', 'قبل']
    
    @classmethod
    def parse(cls, time_text):
        """
        تحليل نص زمني عربي وإرجاع كائن datetime
        
        Args:
            time_text (str): النص الزمني العربي
            
        Returns:
            datetime: كائن datetime أو None إذا فشل التحليل
        """
        if not time_text or not isinstance(time_text, str):
            return None
        
        # تنظيف النص
        time_text = time_text.strip()
        
        # التحقق من الكلمات الدالة على الحاضر
        for keyword in cls.PRESENT_KEYWORDS:
            if keyword in time_text:
                return datetime.now()
        
        # استخراج الأرقام والوحدات الزمنية
        total_delta = timedelta()
        
        # نمط للبحث عن الأرقام متبوعة بوحدات زمنية
        # مثال: "3 أيام" أو "5 ساعات" أو "أسبوعين"
        pattern = r'(\d+)\s*(' + '|'.join(cls.TIME_UNITS.keys()) + r')'
        
        matches = re.findall(pattern, time_text, re.IGNORECASE)
        
        # معالجة خاصة للحالات بدون أرقام (مثل: أسبوعين، شهرين، يومين)
        special_cases = {
            'أسبوعين': 2,
            'اسبوعين': 2,
            'شهرين': 2,
            'يومين': 2,
            'ساعتين': 2,
            'دقيقتين': 2,
            'سنتين': 2,
            'سنوات': 1,  # جمع
            'أشهر': 1,   # جمع
            'أيام': 1,   # جمع
            'ساعات': 1,  # جمع
            'دقائق': 1,  # جمع
            'أعوام': 1,  # جمع
            'أسابيع': 1  # جمع
        }
        
        for special_word, count in special_cases.items():
            if special_word in time_text and not matches:
                unit_type = cls.TIME_UNITS.get(special_word)
                if unit_type == 'weeks':
                    total_delta += timedelta(weeks=count)
                elif unit_type == 'months':
                    total_delta += timedelta(days=count * 30)
                elif unit_type == 'years':
                    total_delta += timedelta(days=count * 365)
                elif unit_type == 'days':
                    total_delta += timedelta(days=count)
                elif unit_type == 'hours':
                    total_delta += timedelta(hours=count)
                elif unit_type == 'minutes':
                    total_delta += timedelta(minutes=count)
                break
        
        if not matches:
            # محاولة بديلة: البحث عن الأرقام العربية (١، ٢، ٣...)
            arabic_numerals = {
                '٠': 0, '١': 1, '٢': 2, '٣': 3, '٤': 4,
                '٥': 5, '٦': 6, '٧': 7, '٨': 8, '٩': 9
            }
            
            # تحويل الأرقام العربية إلى أرقام عربية غربية
            converted_text = time_text
            for arabic, western in arabic_numerals.items():
                converted_text = converted_text.replace(arabic, str(western))
            
            matches = re.findall(pattern, converted_text, re.IGNORECASE)
        
        for number, unit in matches:
            number = int(number)
            unit_type = cls.TIME_UNITS.get(unit)
            
            if unit_type == 'minutes':
                total_delta += timedelta(minutes=number)
            elif unit_type == 'hours':
                total_delta += timedelta(hours=number)
            elif unit_type == 'days':
                total_delta += timedelta(days=number)
            elif unit_type == 'weeks':
                total_delta += timedelta(weeks=number)
            elif unit_type == 'months':
                # تقريب: شهر = 30 يوم
                total_delta += timedelta(days=number * 30)
            elif unit_type == 'years':
                # تقريب: سنة = 365 يوم
                total_delta += timedelta(days=number * 365)
        
        # إذا تم العثور على وحدات زمنية
        if total_delta.total_seconds() > 0:
            return datetime.now() - total_delta
        
        # إذا فشل التحليل، نرجع None
        return None
    
    @classmethod
    def is_older_than(cls, time_text, days):
        """
        التحقق مما إذا كان النص الزمني أقدم من عدد معين من الأيام
        
        Args:
            time_text (str): النص الزمني العربي
            days (int): عدد الأيام للمقارنة
            
        Returns:
            bool: True إذا كان أقدم، False otherwise
        """
        parsed_time = cls.parse(time_text)
        
        if parsed_time is None:
            return False
        
        threshold = datetime.now() - timedelta(days=days)
        return parsed_time < threshold
    
    @classmethod
    def get_relative_description(cls, dt):
        """
        الحصول على وصف نسبي للكائن datetime
        
        Args:
            dt (datetime): كائن datetime
            
        Returns:
            str: وصف نسبي بالعربية
        """
        if not dt:
            return "غير معروف"
        
        now = datetime.now()
        diff = now - dt
        
        if diff.total_seconds() < 60:
            return "منذ أقل من دقيقة"
        elif diff.total_seconds() < 3600:
            minutes = int(diff.total_seconds() / 60)
            return f"منذ {minutes} دقيقة"
        elif diff.total_seconds() < 86400:
            hours = int(diff.total_seconds() / 3600)
            return f"منذ {hours} ساعة"
        elif diff.days < 7:
            return f"منذ {diff.days} يوم"
        elif diff.days < 30:
            weeks = diff.days // 7
            return f"منذ {weeks} أسبوع"
        elif diff.days < 365:
            months = diff.days // 30
            return f"منذ {months} شهر"
        else:
            years = diff.days // 365
            return f"منذ {years} سنة"


# دوال مساعدة للاستخدام المباشر
def parse_arabic_time(time_text):
    """
    تحليل نص زمني عربي
    
    Args:
        time_text (str): النص الزمني
        
    Returns:
        datetime: كائن datetime أو None
    """
    return ArabicTimeParser.parse(time_text)


def is_older_than_days(time_text, days):
    """
    التحقق مما إذا كان الزمن أقدم من عدد أيام
    
    Args:
        time_text (str): النص الزمني
        days (int): عدد الأيام
        
    Returns:
        bool: True إذا كان أقدم
    """
    return ArabicTimeParser.is_older_than(time_text, days)
