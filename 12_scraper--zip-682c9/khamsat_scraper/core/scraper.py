"""
محرك استخراج البيانات الرئيسي (Scraper Engine)
ينسق جميع العمليات: جلب الصفحات، التحليل، التصفح، استخراج التفاصيل، والحفظ
"""

import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import random

from config.settings import (
    BASE_URL, DAYS_LIMIT, MAX_PAGES, REQUEST_TIMEOUT,
    MAX_RETRIES, RETRY_DELAY, DELAY_RANGE, USER_AGENTS,
    ENABLE_PAGINATION, STOP_ON_OLD_REQUEST, MAX_CONCURRENT_REQUESTS,
    INCLUDE_FULL_DETAILS, USE_MOCK_DATA, ENABLE_SMART_TAGGING,
    MIN_REQUESTS_PER_PAGE
)
from config.constants import MESSAGES
from core.parser import HTMLParser
from utils.time_parser import ArabicTimeParser
from utils.helpers import random_delay, normalize_url
from utils.colors import ColorPrinter
from utils.logger import ScraperLogger

# استيراد البيانات الوهمية عند الحاجة
if USE_MOCK_DATA:
    from utils.mock_data import generate_mock_requests

# استيراد نظام التاجات الذكي
if ENABLE_SMART_TAGGING:
    from core.smart_tagger import SmartTagger, smart_tag_request


class KhamsatScraper:
    """
    المحرك الرئيسي لاستخراج بيانات طلبات خمسات
    
    يدعم:
    - Pagination (تصفح الصفحات)
    - استخراج التفاصيل الكاملة
    - التوقف عند الوصول لشرط زمني
    - معالجة أخطاء شاملة
    """
    
    def __init__(self, logger: ScraperLogger, printer: ColorPrinter):
        """
        تهيئة المحرك
        
        Args:
            logger (ScraperLogger): مسجل الأحداث
            printer (ColorPrinter): الطابعة الملونة
        """
        self.logger = logger
        self.printer = printer
        self.base_url = BASE_URL
        self.parser = HTMLParser(BASE_URL)
        
        # تخزين النتائج
        self.all_requests: List[Dict[str, Any]] = []
        self.filtered_requests: List[Dict[str, Any]] = []
        
        # Semaphore للتحكم بالتزامن
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        
        # متغيرات التتبع
        self.current_page = 1
        self.stop_condition_met = False
        self.requests_count = 0
        
        # تهيئة نظام التاجات الذكي
        self.tagger = SmartTagger() if ENABLE_SMART_TAGGING else None
    
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """
        جلب محتوى صفحة مع retry logic
        
        Args:
            session: جلسة aiohttp
            url (str): الرابط
            
        Returns:
            str: محتوى HTML أو None
        """
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ar-SA,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
        }
        
        # استخدام TCP Keepalive و اتصال فعال
        connector_kwargs = {
            'limit': MAX_CONCURRENT_REQUESTS,
            'limit_per_host': MAX_CONCURRENT_REQUESTS,
            'enable_cleanup_closed': True,
            'force_close': False,
        }
        
        for attempt in range(MAX_RETRIES):
            try:
                async with session.get(url, headers=headers, timeout=REQUEST_TIMEOUT) as response:
                    if response.status == 200:
                        html = await response.text(encoding='utf-8')
                        self.logger.info(f"تم جلب الصفحة بنجاح: {url}")
                        return html
                    else:
                        self.logger.warning(f"رمز استجابة غير ناجح: {response.status}")
                        
            except asyncio.TimeoutError:
                self.logger.error(f"انتهت مهلة الطلب للمحاولة {attempt + 1}")
            except aiohttp.ClientError as e:
                self.logger.error(f"خطأ في العميل: {e}")
            except Exception as e:
                self.logger.error(f"خطأ غير متوقع: {e}", exc_info=True)
            
            if attempt < MAX_RETRIES - 1:
                wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                self.logger.info(f"إعادة المحاولة بعد {wait_time} ثانية...")
                await asyncio.sleep(wait_time)
        
        return None
    
    async def fetch_pages_batch(self, session: aiohttp.ClientSession, urls: List[str]) -> List[Optional[str]]:
        """
        جلب عدة صفحات بشكل متوازٍ باستخدام semaphore
        
        Args:
            session: جلسة aiohttp
            urls (List[str]): قائمة الروابط
            
        Returns:
            List[Optional[str]]: قائمة محتويات HTML
        """
        async def fetch_with_semaphore(url: str) -> Optional[str]:
            async with self.semaphore:
                return await self.fetch_page(session, url)
        
        tasks = [fetch_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # معالجة الاستثناءات
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"فشل جلب الصفحة: {result}")
                processed_results.append(None)
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def scrape_all_pages(self):
        """
        الوظيفة الرئيسية لاستخراج جميع الطلبات من جميع الصفحات
        """
        self.printer.print_header("بدء عملية استخراج البيانات")
        self.logger.info("بدء استخراج البيانات من جميع الصفحات")
        
        time_limit = datetime.now() - timedelta(days=DAYS_LIMIT)
        self.printer.print_info(f"الحد الزمني: {DAYS_LIMIT} يوم (قبل {time_limit.strftime('%Y-%m-%d %H:%M')})")
        
        # استخدام البيانات الوهمية إذا كان مفعلاً
        if USE_MOCK_DATA:
            self.printer.print_warning("⚠️  وضع الاختبار مفعّل - استخدام بيانات وهمية")
            self.logger.info("استخدام البيانات الوهمية (MOCK DATA)")
            
            mock_requests = generate_mock_requests()
            
            for req in mock_requests:
                parsed_time = req.get('parsed_time')
                
                # التحقق من شرط التوقف
                if parsed_time and parsed_time < time_limit:
                    self.printer.print_warning(
                        f"🛑 تم إيقاف الاستخراج عند الوصول للحد الزمني ({DAYS_LIMIT} أيام)"
                    )
                    self.logger.info(f"تم إيقاف الاستخراج عند الطلب: {req.get('title', '')}")
                    self.stop_condition_met = True
                    break
                
                # إضافة الطلب للقائمة
                self.all_requests.append(req)
                self.requests_count += 1
                
                # استخراج التفاصيل الكاملة إذا كان مطلوباً
                if INCLUDE_FULL_DETAILS:
                    # في حالة البيانات الوهمية، التفاصيل موجودة بالفعل
                    pass
            
            # تطبيق الفلاتر
            self._apply_filters(time_limit)
            
            self.printer.print_success(
                MESSAGES['found_requests'].format(len(self.all_requests))
            )
            self.printer.print_success(
                MESSAGES['filtered_requests'].format(len(self.filtered_requests))
            )
            return
        
        # الكود الأصلي للموقع الحقيقي
        connector = aiohttp.TCPConnector(
            limit=MAX_CONCURRENT_REQUESTS,
            limit_per_host=MAX_CONCURRENT_REQUESTS,
            enable_cleanup_closed=True,
            force_close=False,
            ttl_dns_cache=300,
            use_dns_cache=True,
        )
        
        timeout = aiohttp.ClientTimeout(
            total=REQUEST_TIMEOUT,
            connect=10,
            sock_read=READ_TIMEOUT if 'READ_TIMEOUT' in dir() else 30,
            sock_connect=10
        )
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            current_url = self.base_url
            
            while current_url and not self.stop_condition_met:
                if self.current_page > MAX_PAGES:
                    self.printer.print_warning(f"تم الوصول للحد الأقصى للصفحات ({MAX_PAGES})")
                    break
                
                # جلب الصفحة
                self.printer.print_info(MESSAGES['fetching'].format(self.current_page))
                html = await self.fetch_page(session, current_url)
                
                if not html:
                    self.printer.print_error(f"فشل جلب الصفحة {self.current_page}")
                    break
                
                # حفظ HTML الأصلي (اختياري)
                # يمكن إضافته هنا
                
                # تحليل القائمة
                requests = self.parser.extract_requests_from_list(html)
                
                if not requests:
                    self.printer.print_warning("لم يتم العثور على طلبات في هذه الصفحة")
                    break
                
                self.printer.print_success(f"تم العثور على {len(requests)} طلب في الصفحة {self.current_page}")
                
                # معالجة كل طلب
                for req in requests:
                    # تحليل الوقت
                    parsed_time = ArabicTimeParser.parse(req.get('raw_time', ''))
                    req['parsed_time'] = parsed_time
                    req['extracted_at'] = datetime.now().isoformat()
                    
                    # التحقق من شرط التوقف
                    if parsed_time and parsed_time < time_limit:
                        self.printer.print_warning(
                            MESSAGES['stop_condition'].format(DAYS_LIMIT)
                        )
                        self.logger.info(f"تم إيقاف الاستخراج عند الطلب: {req.get('title', '')}")
                        self.stop_condition_met = True
                        break
                    
                    # إضافة الطلب للقائمة
                    self.all_requests.append(req)
                    self.requests_count += 1
                    
                    # تطبيق التاجات الذكية إذا كان مفعلاً
                    if self.tagger and ENABLE_SMART_TAGGING:
                        try:
                            tagged_req = smart_tag_request(req)
                            req.update(tagged_req)
                            self.logger.debug(f"تم تطبيق التاجات على الطلب: {req.get('title', '')[:50]}")
                        except Exception as e:
                            self.logger.warning(f"فشل تطبيق التاجات الذكية: {e}")
                    
                    # استخراج التفاصيل الكاملة إذا كان مطلوباً
                    if INCLUDE_FULL_DETAILS and req.get('url'):
                        details = await self._extract_full_details(session, req['url'])
                        req.update(details)
                    
                    # تأخير عشوائي مخفض لتحسين الأداء
                    if DELAY_RANGE[1] > 0:
                        await random_delay(*DELAY_RANGE)
                
                if self.stop_condition_met:
                    break
                
                # التحقق من عدد الطلبات في الصفحة (إصلاح مشكلة التوقف الخاطئ)
                if len(requests) < MIN_REQUESTS_PER_PAGE:
                    self.printer.print_info("عدد الطلبات في الصفحة أقل من الحد الأدنى - قد تكون هذه آخر صفحة")
                    # لا نتوقف هنا، بل نحاول الصفحة التالية
                
                # الانتقال للصفحة التالية
                if ENABLE_PAGINATION:
                    pagination_info = self.parser.extract_pagination_info(html)
                    if pagination_info.get('has_next'):
                        current_url = pagination_info.get('next_url', '')
                        self.current_page += 1
                        self.printer.print_info(f"الانتقال للصفحة {self.current_page}")
                    else:
                        self.printer.print_info(MESSAGES['no_more_pages'])
                        break
                else:
                    break
        
        # تطبيق الفلاتر
        self._apply_filters(time_limit)
        
        self.printer.print_success(
            MESSAGES['found_requests'].format(len(self.all_requests))
        )
        self.printer.print_success(
            MESSAGES['filtered_requests'].format(len(self.filtered_requests))
        )
    
    async def _extract_full_details(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """
        استخراج التفاصيل الكاملة لطلب واحد
        
        Args:
            session: جلسة aiohttp
            url (str): رابط صفحة التفاصيل
            
        Returns:
            Dict: التفاصيل الكاملة
        """
        async with self.semaphore:
            try:
                html = await self.fetch_page(session, url)
                if html:
                    details = self.parser.extract_details_from_page(html)
                    return details
            except Exception as e:
                self.logger.error(f"فشل استخراج التفاصيل من {url}: {e}")
        
        return {}
    
    async def _extract_full_details_batch(self, session: aiohttp.ClientSession, urls: List[str]) -> List[Dict[str, Any]]:
        """
        استخراج التفاصيل الكاملة لعدة طلبات بشكل متوازٍ
        
        Args:
            session: جلسة aiohttp
            urls (List[str]): قائمة روابط صفحات التفاصيل
            
        Returns:
            List[Dict]: قائمة التفاصيل الكاملة
        """
        async def extract_single(url: str) -> Dict[str, Any]:
            async with self.semaphore:
                try:
                    html = await self.fetch_page(session, url)
                    if html:
                        return self.parser.extract_details_from_page(html)
                except Exception as e:
                    self.logger.error(f"فشل استخراج التفاصيل من {url}: {e}")
                return {}
        
        tasks = [extract_single(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # معالجة الاستثناءات
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"فشل استخراج التفاصيل: {result}")
                processed_results.append({})
            else:
                processed_results.append(result)
        
        return processed_results
    
    def _apply_filters(self, time_limit: datetime):
        """
        تطبيق الفلاتر على الطلبات المستخرجة
        
        Args:
            time_limit (datetime): الحد الزمني
        """
        self.filtered_requests = [
            req for req in self.all_requests
            if req.get('parsed_time') and req['parsed_time'] >= time_limit
        ]
        
        self.logger.info(f"تم تصفية {len(self.filtered_requests)} طلب من أصل {len(self.all_requests)}")
    
    def get_results(self) -> Dict[str, List[Dict]]:
        """
        الحصول على النتائج
        
        Returns:
            Dict: قاموس يحتوي على all_requests و filtered_requests
        """
        return {
            'all_requests': self.all_requests,
            'filtered_requests': self.filtered_requests
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        الحصول على إحصائيات عن النتائج
        
        Returns:
            Dict: الإحصائيات
        """
        from utils.helpers import calculate_statistics
        
        stats = {
            'total_pages_scraped': self.current_page,
            'total_requests_found': len(self.all_requests),
            'filtered_requests': len(self.filtered_requests),
            'stop_condition_met': self.stop_condition_met
        }
        
        # إضافة إحصائيات مفصلة
        if self.filtered_requests:
            detailed_stats = calculate_statistics(self.filtered_requests)
            stats.update(detailed_stats)
        
        return stats
