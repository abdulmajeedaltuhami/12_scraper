"""
وحدة تصدير البيانات (Data Exporter)
تصدير البيانات إلى ملفات CSV و JSON بتنسيقات منظمة
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import os

from config.constants import CSV_COLUMNS
from config.settings import EXPORT_CSV, EXPORT_JSON, OUTPUT_BASE_FOLDER
from utils.colors import ColorPrinter
from utils.logger import ScraperLogger


class DataExporter:
    """
    فئة لتصدير البيانات المستخرجة إلى ملفات
    
    تدعم:
    - CSV مع UTF-8 BOM لدعم العربية
    - JSON منسق
    - تنظيم المجلدات بالوقت
    """
    
    def __init__(self, logger: ScraperLogger, printer: ColorPrinter):
        """
        تهيئة مصدر البيانات
        
        Args:
            logger (ScraperLogger): مسجل الأحداث
            printer (ColorPrinter): الطابعة الملونة
        """
        self.logger = logger
        self.printer = printer
        
        # إنشاء مجلد المخرجات باسم زمني
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_folder = Path(f"{OUTPUT_BASE_FOLDER}_{timestamp}")
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"تم إنشاء مجلد المخرجات: {self.output_folder}")
        self.printer.print_success(f"مجلد المخرجات: {self.output_folder.name}")
    
    def export_all(self, all_requests: List[Dict], filtered_requests: List[Dict]):
        """
        تصدير جميع البيانات (CSV و JSON)
        
        Args:
            all_requests (List[Dict]): جميع الطلبات
            filtered_requests (List[Dict]): الطلبات المصفاة
        """
        self.printer.print_header("بدء عملية حفظ البيانات")
        self.logger.info("بدء تصدير البيانات")
        
        # تصدير CSV
        if EXPORT_CSV:
            self._export_csv(all_requests, "all_requests.csv")
            self._export_csv(filtered_requests, "filtered_requests.csv")
        
        # تصدير JSON
        if EXPORT_JSON:
            self._export_json(all_requests, "all_requests.json")
            self._export_json(filtered_requests, "filtered_requests.json")
        
        # تصدير تقرير ملخص
        self._export_summary_report(all_requests, filtered_requests)
        
        self.printer.print_success("اكتملت عملية حفظ البيانات بنجاح!")
        self.logger.info(f"تم حفظ البيانات في المجلد: {self.output_folder}")
    
    def _export_csv(self, data: List[Dict], filename: str):
        """
        تصدير البيانات إلى ملف CSV
        
        Args:
            data (List[Dict]): البيانات
            filename (str): اسم الملف
        """
        if not data:
            self.logger.warning(f"لا توجد بيانات لحفظها في {filename}")
            return
        
        filepath = self.output_folder / filename
        
        try:
            # فتح الملف مع UTF-8 BOM لدعم العربية في Excel
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=CSV_COLUMNS,
                    extrasaction='ignore'
                )
                
                # كتابة العنوان
                writer.writeheader()
                
                # كتابة البيانات
                for row in data:
                    # تحويل القيم غير القابلة للتسلسل
                    processed_row = self._process_row(row)
                    writer.writerow(processed_row)
            
            self.printer.print_success(f"تم حفظ {len(data)} سجل في {filename}")
            self.logger.info(f"تم حفظ CSV: {filepath} ({len(data)} سجل)")
            
        except Exception as e:
            self.printer.print_error(f"فشل حفظ CSV: {e}")
            self.logger.error(f"فشل حفظ CSV {filename}: {e}", exc_info=True)
    
    def _export_json(self, data: List[Dict], filename: str):
        """
        تصدير البيانات إلى ملف JSON
        
        Args:
            data (List[Dict]): البيانات
            filename (str): اسم الملف
        """
        if not data:
            self.logger.warning(f"لا توجد بيانات لحفظها في {filename}")
            return
        
        filepath = self.output_folder / filename
        
        try:
            # تجهيز البيانات للتصدير
            export_data = {
                'metadata': {
                    'exported_at': datetime.now().isoformat(),
                    'total_records': len(data),
                    'source': 'Khamsat.com',
                    'format': 'JSON'
                },
                'data': []
            }
            
            for item in data:
                processed_item = self._process_row(item)
                export_data['data'].append(processed_item)
            
            # كتابة JSON منسق
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(
                    export_data,
                    jsonfile,
                    ensure_ascii=False,
                    indent=2,
                    default=str  # لتحويل datetime وغيرها
                )
            
            self.printer.print_success(f"تم حفظ {len(data)} سجل في {filename}")
            self.logger.info(f"تم حفظ JSON: {filepath} ({len(data)} سجل)")
            
        except Exception as e:
            self.printer.print_error(f"فشل حفظ JSON: {e}")
            self.logger.error(f"فشل حفظ JSON {filename}: {e}", exc_info=True)
    
    def _process_row(self, row: Dict) -> Dict:
        """
        معالجة صف بيانات للتصدير
        
        Args:
            row (Dict): الصف الأصلي
            
        Returns:
            Dict: الصف المعالج
        """
        processed = {}
        
        for key, value in row.items():
            if value is None:
                processed[key] = ""
            elif isinstance(value, datetime):
                processed[key] = value.isoformat()
            elif isinstance(value, list):
                # تحويل القوائم إلى نص مفصول بفواصل
                processed[key] = ' | '.join(str(v) for v in value)
            elif isinstance(value, dict):
                processed[key] = json.dumps(value, ensure_ascii=False, default=str)
            else:
                processed[key] = str(value)
        
        return processed
    
    def _export_summary_report(self, all_requests: List[Dict], filtered_requests: List[Dict]):
        """
        تصدير تقرير ملخص عن العملية
        
        Args:
            all_requests (List[Dict]): جميع الطلبات
            filtered_requests (List[Dict]): الطلبات المصفاة
        """
        filepath = self.output_folder / "summary_report.txt"
        
        try:
            from utils.helpers import calculate_statistics
            
            stats_all = calculate_statistics(all_requests)
            stats_filtered = calculate_statistics(filtered_requests)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("تقرير استخراج بيانات خمسات\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"تاريخ التصدير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("-" * 40 + "\n")
                f.write("إحصائيات عامة (جميع الطلبات):\n")
                f.write("-" * 40 + "\n")
                f.write(f"إجمالي الطلبات: {stats_all.get('total', 0)}\n")
                f.write(f"طلبات بميزانية: {stats_all.get('with_budget', 0)}\n")
                f.write(f"طلبات بدون ميزانية: {stats_all.get('without_budget', 0)}\n")
                f.write(f"متوسط العروض: {stats_all.get('avg_proposals', 0)}\n")
                if stats_all.get('oldest_date'):
                    f.write(f"أقدم طلب: {stats_all['oldest_date']}\n")
                if stats_all.get('newest_date'):
                    f.write(f"أحدث طلب: {stats_all['newest_date']}\n")
                
                f.write("\n")
                f.write("-" * 40 + "\n")
                f.write("إحصائيات الطلبات المصفاة:\n")
                f.write("-" * 40 + "\n")
                f.write(f"إجمالي الطلبات المصفاة: {stats_filtered.get('total', 0)}\n")
                f.write(f"طلبات بميزانية: {stats_filtered.get('with_budget', 0)}\n")
                f.write(f"طلبات بدون ميزانية: {stats_filtered.get('without_budget', 0)}\n")
                f.write(f"متوسط العروض: {stats_filtered.get('avg_proposals', 0)}\n")
                if stats_filtered.get('oldest_date'):
                    f.write(f"أقدم طلب: {stats_filtered['oldest_date']}\n")
                if stats_filtered.get('newest_date'):
                    f.write(f"أحدث طلب: {stats_filtered['newest_date']}\n")
                
                f.write("\n")
                f.write("=" * 80 + "\n")
                f.write("تم التصدير بنجاح!\n")
                f.write("=" * 80 + "\n")
            
            self.printer.print_success(f"تم حفظ التقرير الملخص: summary_report.txt")
            self.logger.info(f"تم حفظ التقرير: {filepath}")
            
        except Exception as e:
            self.printer.print_error(f"فشل حفظ التقرير: {e}")
            self.logger.error(f"فشل حفظ التقرير: {e}", exc_info=True)
    
    def get_output_folder(self) -> Path:
        """
        الحصول على مسار مجلد المخرجات
        
        Returns:
            Path: مسار المجلد
        """
        return self.output_folder
