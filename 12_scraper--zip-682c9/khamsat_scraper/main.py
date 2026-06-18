"""
نقطة الدخول الرئيسية لبرنامج استخراج بيانات خمسات
تجمع بين جميع الوحدات وتنفذ العملية الكاملة
"""

import asyncio
import sys
from datetime import datetime

# إضافة مسار الجذر للـ Python path
sys.path.insert(0, '.')

from config.settings import (
    LOG_LEVEL, LOG_TO_FILE, LOG_TO_CONSOLE,
    COLOR_OUTPUT, RTL_SUPPORT, VERBOSE_OUTPUT
)
from config.constants import MESSAGES
from utils.logger import ScraperLogger
from utils.colors import ColorPrinter
from core.scraper import KhamsatScraper
from core.exporter import DataExporter


async def main():
    """
    الدالة الرئيسية لتنفيذ البرنامج
    
    تنفذ الخطوات التالية:
    1. تهيئة نظام التسجيل والطباعة
    2. إنشاء محرك الاستخراج
    3. تنفيذ عملية الاستخراج
    4. تصدير النتائج
    5. عرض التقرير النهائي
    """
    
    # ============================================
    # الخطوة 1: تهيئة نظام التسجيل والطباعة
    # ============================================
    logger = ScraperLogger(
        log_level=LOG_LEVEL,
        log_to_file=LOG_TO_FILE,
        log_to_console=LOG_TO_CONSOLE
    )
    
    printer = ColorPrinter(
        enable_color=COLOR_OUTPUT,
        rtl_support=RTL_SUPPORT
    )
    
    # طباعة رسالة الترحيب
    printer.print_header("برنامج استخراج بيانات خمسات الاحترافي")
    printer.print_info(MESSAGES['start'])
    printer.print_info(f"تاريخ التشغيل: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    printer.print_subheader("إعدادات النظام")
    printer.print_info(f"مستوى التسجيل: {LOG_LEVEL}")
    printer.print_info(f"الألوان: {'مفعلة' if COLOR_OUTPUT else 'معطلة'}")
    printer.print_info(f"دعم العربية: {'مفعل' if RTL_SUPPORT else 'معطل'}")
    
    logger.info("تم تهيئة النظام بنجاح")
    
    # ============================================
    # الخطوة 2: إنشاء محرك الاستخراج
    # ============================================
    try:
        scraper = KhamsatScraper(logger=logger, printer=printer)
        logger.info("تم إنشاء محرك الاستخراج بنجاح")
    except Exception as e:
        printer.print_error(f"فشل إنشاء محرك الاستخراج: {e}")
        logger.error(f"خطأ حرج في التهيئة: {e}", exc_info=True)
        return 1
    
    # ============================================
    # الخطوة 3: تنفيذ عملية الاستخراج
    # ============================================
    try:
        await scraper.scrape_all_pages()
        logger.info("اكتملت عملية الاستخراج بنجاح")
    except KeyboardInterrupt:
        printer.print_warning("\nتم إيقاف البرنامج بواسطة المستخدم")
        logger.warning("تم إيقاف البرنامج بواسطة المستخدم (KeyboardInterrupt)")
        return 1
    except Exception as e:
        printer.print_error(f"حدث خطأ أثناء الاستخراج: {e}")
        logger.error(f"خطأ أثناء الاستخراج: {e}", exc_info=True)
        return 1
    
    # ============================================
    # الخطوة 4: تصدير النتائج
    # ============================================
    try:
        results = scraper.get_results()
        exporter = DataExporter(logger=logger, printer=printer)
        exporter.export_all(
            all_requests=results['all_requests'],
            filtered_requests=results['filtered_requests']
        )
        logger.info("تم تصدير النتائج بنجاح")
    except Exception as e:
        printer.print_error(f"فشل تصدير النتائج: {e}")
        logger.error(f"خطأ أثناء التصدير: {e}", exc_info=True)
        return 1
    
    # ============================================
    # الخطوة 5: عرض التقرير النهائي
    # ============================================
    try:
        stats = scraper.get_statistics()
        
        printer.print_header("التقرير النهائي")
        printer.print_table_row(["المؤشر", "القيمة"], widths=[30, 50])
        printer.print_table_row(["-" * 30, "-" * 50], widths=[30, 50])
        printer.print_table_row(["إجمالي الصفحات", str(stats.get('total_pages_scraped', 0))], widths=[30, 50])
        printer.print_table_row(["إجمالي الطلبات", str(stats.get('total_requests_found', 0))], widths=[30, 50])
        printer.print_table_row(["الطلبات المصفاة", str(stats.get('filtered_requests', 0))], widths=[30, 50])
        printer.print_table_row(["تحقق شرط التوقف", "نعم" if stats.get('stop_condition_met') else "لا"], widths=[30, 50])
        
        if stats.get('total', 0) > 0:
            printer.print_table_row(["طلبات بميزانية", str(stats.get('with_budget', 0))], widths=[30, 50])
            printer.print_table_row(["متوسط العروض", str(stats.get('avg_proposals', 0))], widths=[30, 50])
            
            if stats.get('oldest_date'):
                printer.print_table_row(["أقدم طلب", str(stats['oldest_date'])], widths=[30, 50])
            if stats.get('newest_date'):
                printer.print_table_row(["أحدث طلب", str(stats['newest_date'])], widths=[30, 50])
        
        printer.print_success("\n" + "=" * 80)
        printer.print_success("تم الانتهاء من عملية الاستخراج بنجاح!")
        printer.print_success(f"الملفات محفوظة في المجلد: {exporter.get_output_folder()}")
        printer.print_success("=" * 80)
        
        logger.info("تم عرض التقرير النهائي بنجاح")
        
    except Exception as e:
        printer.print_error(f"فشل عرض التقرير: {e}")
        logger.error(f"خطأ في التقرير النهائي: {e}", exc_info=True)
    
    # تنظيف الموارد
    logger.close()
    
    return 0


if __name__ == "__main__":
    """
    نقطة دخول البرنامج
    """
    try:
        # تحسين إعدادات asyncio للأداء
        import platform
        if platform.system() != 'Windows':
            # استخدام uvloop إذا كان متاحاً (أسرع من asyncio العادي)
            try:
                import uvloop
                asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
                print("✅ تم تفعيل uvloop لتحسين الأداء")
            except ImportError:
                pass
        
        # تشغيل البرنامج باستخدام asyncio
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except Exception as e:
        print(f"❌ خطأ حرج في مستوى النظام: {e}")
        sys.exit(1)
