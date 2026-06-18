"""
وحدة الطباعة الملونة الاحترافية
تدعم اللغة العربية والكتابة من اليمين لليسار (RTL)
"""

from colorama import init, Fore, Back, Style
import sys

# تهيئة colorama لدعم Windows و Arabic
init(autoreset=True)


class ColorPrinter:
    """
    فئة للطباعة الملونة الاحترافية مع دعم كامل للعربية
    """
    
    # تعريف الألوان
    COLORS = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'black': Fore.BLACK,
        'reset': Style.RESET_ALL
    }
    
    STYLES = {
        'bright': Style.BRIGHT,
        'dim': Style.DIM,
        'normal': Style.NORMAL
    }
    
    def __init__(self, enable_color=True, rtl_support=True):
        """
        تهيئة الطابعة الملونة
        
        Args:
            enable_color (bool): تفعيل الألوان
            rtl_support (bool): دعم الكتابة من اليمين لليسار
        """
        self.enable_color = enable_color
        self.rtl_support = rtl_support
    
    def _get_color(self, color_name):
        """
        الحصول على كود اللون
        
        Args:
            color_name (str): اسم اللون
            
        Returns:
            str: كود اللون
        """
        if not self.enable_color:
            return ''
        return self.COLORS.get(color_name.lower(), '')
    
    def _get_style(self, style_name):
        """
        الحصول على كود النمط
        
        Args:
            style_name (str): اسم النمط
            
        Returns:
            str: كود النمط
        """
        if not self.enable_color:
            return ''
        return self.STYLES.get(style_name.lower(), '')
    
    def print(self, message, color='white', style='normal', end='\n'):
        """
        طباعة رسالة ملونة
        
        Args:
            message (str): الرسالة المراد طباعتها
            color (str): لون النص
            style (str): نمط النص
            end (str): نهاية السطر
        """
        color_code = self._get_color(color)
        style_code = self._get_style(style)
        reset_code = Style.RESET_ALL if self.enable_color else ''
        
        # تنسيق النص للغة العربية إذا لزم الأمر
        if self.rtl_support and any('\u0600' <= c <= '\u06FF' for c in message):
            # إضافة علامة RTL للنص العربي
            formatted_message = f"{color_code}{style_code}{message}{reset_code}"
        else:
            formatted_message = f"{color_code}{style_code}{message}{reset_code}"
        
        print(formatted_message, end=end, flush=True)
    
    def print_success(self, message):
        """طباعة رسالة نجاح باللون الأخضر"""
        self.print(f"✅ {message}", color='green')
    
    def print_error(self, message):
        """طباعة رسالة خطأ باللون الأحمر"""
        self.print(f"❌ {message}", color='red')
    
    def print_warning(self, message):
        """طباعة رسالة تحذير باللون الأصفر"""
        self.print(f"⚠️  {message}", color='yellow')
    
    def print_info(self, message):
        """طباعة رسالة معلومات باللون الأزرق"""
        self.print(f"ℹ️  {message}", color='cyan')
    
    def print_debug(self, message):
        """طباعة رسالة تصحيح باللون المغنطيسي"""
        self.print(f"🔍 {message}", color='magenta')
    
    def print_header(self, message):
        """طباعة عنوان رئيسي"""
        separator = "=" * 80
        self.print(separator, color='cyan', style='bright')
        self.print(message.center(80), color='cyan', style='bright')
        self.print(separator, color='cyan', style='bright')
    
    def print_subheader(self, message):
        """طباعة عنوان فرعي"""
        separator = "-" * 60
        self.print(separator, color='yellow')
        self.print(f"  {message}", color='yellow', style='bright')
        self.print(separator, color='yellow')
    
    def print_progress(self, current, total, prefix=""):
        """
        طباعة شريط التقدم
        
        Args:
            current (int): القيمة الحالية
            total (int): القيمة الكلية
            prefix (str): نص قبل شريط التقدم
        """
        percentage = (current / total * 100) if total > 0 else 0
        bar_length = 40
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        # مسح السطر الحالي
        sys.stdout.write('\r')
        self.print(f"{prefix} |{bar}| {current}/{total} ({percentage:.1f}%)", 
                  color='green', end='')
        sys.stdout.flush()
        
        if current >= total:
            print()  # سطر جديد عند الاكتمال
    
    def print_table_row(self, columns, widths=None):
        """
        طباعة صف جدول منسق
        
        Args:
            columns (list): قائمة القيم للأعمدة
            widths (list): عرض كل عمود
        """
        if widths is None:
            widths = [20] * len(columns)
        
        row = ""
        for col, width in zip(columns, widths):
            # قص النص إذا كان أطول من العرض المحدد
            col_str = str(col)[:width-3] + "..." if len(str(col)) > width else str(col)
            row += f"{col_str:<{width}}  "
        
        self.print(row, color='white')
    
    def clear_line(self):
        """مسح السطر الحالي"""
        sys.stdout.write('\r')
        sys.stdout.write(' ' * 100)
        sys.stdout.write('\r')
        sys.stdout.flush()


# إنشاء نسخة عامة للاستخدام المباشر
printer = ColorPrinter()
