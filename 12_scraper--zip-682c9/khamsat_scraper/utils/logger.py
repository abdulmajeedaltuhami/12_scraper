"""
نظام التسجيل المتقدم (Logging System)
يسجل جميع الأحداث في ملف وعلى الشاشة مع دعم rotation
"""

import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os
from pathlib import Path


class ScraperLogger:
    """
    فئة متقدمة لتسجيل الأحداث مع دعم:
    - التسجيل في ملف وفي نفس الوقت على الشاشة
    - Rotation للملفات لتجنب الحجم الكبير
    - تنسيق مخصص يدعم العربية
    - مستويات تسجيل متعددة
    """
    
    def __init__(self, log_folder="logs", log_level="INFO", 
                 log_to_file=True, log_to_console=True,
                 rotation_size="10 MB", backup_count=5):
        """
        تهيئة نظام التسجيل
        
        Args:
            log_folder (str): مجلد حفظ ملفات السجل
            log_level (str): مستوى التسجيل (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_to_file (bool): التسجيل في ملف
            log_to_console (bool): التسجيل على الشاشة
            rotation_size (str): حجم الدوران (مثال: "10 MB")
            backup_count (int): عدد النسخ الاحتياطية
        """
        self.log_folder = Path(log_folder)
        self.log_to_file = log_to_file
        self.log_to_console = log_to_console
        
        # إنشاء اسم ملف فريد بالوقت
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"scraper_log_{timestamp}.log"
        
        # إنشاء المجلد إذا لم يكن موجوداً
        if log_to_file:
            self.log_folder.mkdir(parents=True, exist_ok=True)
            self.log_path = self.log_folder / self.log_filename
        else:
            self.log_path = None
        
        # إعداد logger
        self.logger = logging.getLogger("KhamsatScraper")
        self.logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # إزالة handlers السابقة إن وجدت
        self.logger.handlers.clear()
        
        # تنسيق السجلات (يدعم العربية)
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler للملف
        if log_to_file and self.log_path:
            try:
                # تحويل حجم الدوران إلى بايت
                size_bytes = self._parse_size(rotation_size)
                
                file_handler = RotatingFileHandler(
                    self.log_path,
                    encoding='utf-8',
                    maxBytes=size_bytes,
                    backupCount=backup_count
                )
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
            except Exception as e:
                print(f"⚠️  تحذير: فشل إنشاء ملف السجل: {e}")
                self.log_to_file = False
        
        # Handler للشاشة
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # تسجيل رسالة البداية
        self.info("=" * 80)
        self.info("بدء تشغيل نظام تسجيل أحداث خمسات")
        self.info(f"مستوى التسجيل: {log_level}")
        self.info(f"التسجيل في ملف: {'نعم' if log_to_file else 'لا'}")
        self.info(f"التسجيل على الشاشة: {'نعم' if log_to_console else 'لا'}")
        if log_to_file:
            self.info(f"مسار ملف السجل: {self.log_path}")
        self.info("=" * 80)
    
    def _parse_size(self, size_str):
        """
        تحليل حجم الدوران من نص إلى بايت
        
        Args:
            size_str (str): الحجم كنص (مثال: "10 MB")
            
        Returns:
            int: الحجم بالبايت
        """
        size_str = size_str.strip().upper()
        multipliers = {
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4
        }
        
        for unit, multiplier in multipliers.items():
            if unit in size_str:
                number = float(size_str.replace(unit, '').strip())
                return int(number * multiplier)
        
        # إذا لم يتم تحديد وحدة، نعتبرها بايت
        return int(float(size_str))
    
    def debug(self, message):
        """تسجيل رسالة تصحيح"""
        self.logger.debug(message)
    
    def info(self, message):
        """تسجيل رسالة معلومات"""
        self.logger.info(message)
    
    def warning(self, message):
        """تسجيل رسالة تحذير"""
        self.logger.warning(message)
    
    def error(self, message, exc_info=False):
        """
        تسجيل رسالة خطأ
        
        Args:
            message (str): رسالة الخطأ
            exc_info (bool): تضمين معلومات الاستثناء
        """
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message, exc_info=False):
        """
        تسجيل رسالة حرجة
        
        Args:
            message (str): الرسالة الحرجة
            exc_info (bool): تضمين معلومات الاستثناء
        """
        self.logger.critical(message, exc_info=exc_info)
    
    def exception(self, message):
        """
        تسجيل استثناء مع معلومات التتبع
        
        Args:
            message (str): رسالة الخطأ
        """
        self.logger.exception(message)
    
    def get_log_path(self):
        """الحصول على مسار ملف السجل"""
        return str(self.log_path) if self.log_path else None
    
    def close(self):
        """إغلاق جميع handlers وتنظيف الموارد"""
        for handler in self.logger.handlers[:]:
            try:
                handler.close()
                self.logger.removeHandler(handler)
            except:
                pass
        self.info("تم إغلاق نظام التسجيل بنجاح")


# دالة مساعدة لإنشاء logger بسرعة
def setup_logger(log_folder="logs", log_level="INFO", 
                 log_to_file=True, log_to_console=True):
    """
    إنشاء وإرجاع مثيل ScraperLogger
    
    Returns:
        ScraperLogger: مثيل مسجل الأحداث
    """
    return ScraperLogger(
        log_folder=log_folder,
        log_level=log_level,
        log_to_file=log_to_file,
        log_to_console=log_to_console
    )
