"""
محلل HTML لاستخراج البيانات من صفحات خمسات
يستخدم BeautifulSoup لتحليل HTML واستخراج البيانات باستخدام محددات CSS مرنة
"""

from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Any
import re

from config.constants import LIST_SELECTORS, DETAIL_SELECTORS, PAGINATION_SELECTORS
from utils.helpers import clean_text, normalize_url, extract_number_from_text


class HTMLParser:
    """
    فئة لتحليل HTML صفحات خمسات واستخراج البيانات
    
    تستخدم استراتيجية fallback متعددة المحددات لضمان المرونة
    """
    
    def __init__(self, base_url: str):
        """
        تهيئة المحلل
        
        Args:
            base_url (str): الرابط الأساسي للموقع
        """
        self.base_url = base_url
    
    def parse(self, html_content: str) -> BeautifulSoup:
        """
        تحليل محتوى HTML وإرجاع كائن BeautifulSoup
        
        Args:
            html_content (str): محتوى HTML الخام
            
        Returns:
            BeautifulSoup: كائن BeautifulSoup للتحليل
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
    
    def extract_requests_from_list(self, html_content: str) -> List[Dict[str, Any]]:
        """
        استخراج قائمة الطلبات من صفحة القائمة الرئيسية
        
        Args:
            html_content (str): محتوى HTML لصفحة القائمة
            
        Returns:
            List[Dict]: قائمة من الطلبات المستخرجة
        """
        soup = self.parse(html_content)
        requests = []
        
        # البحث عن عناصر الطلبات باستخدام محددات متعددة
        request_items = self._find_with_fallback(soup, LIST_SELECTORS['request_item'])
        
        for item in request_items:
            try:
                request_data = self._parse_request_item(item)
                if request_data and request_data.get('url'):
                    requests.append(request_data)
            except Exception as e:
                # استمرار في حالة وجود خطأ في عنصر واحد
                continue
        
        return requests
    
    def _parse_request_item(self, item) -> Dict[str, Any]:
        """
        تحليل عنصر طلب واحد واستخراج بياناته
        
        Args:
            item: عنصر HTML للطلب
            
        Returns:
            Dict: بيانات الطلب
        """
        data = {}
        
        # استخراج العنوان والرابط
        title_elem = self._find_first_with_fallback(item, LIST_SELECTORS['title'])
        if title_elem:
            data['title'] = clean_text(title_elem.get_text())
            data['url'] = normalize_url(self.base_url, title_elem.get('href', ''))
        else:
            data['title'] = "عنوان غير متوفر"
            data['url'] = ""
        
        # استخراج الوقت
        time_elem = self._find_first_with_fallback(item, LIST_SELECTORS['time'])
        if time_elem:
            data['raw_time'] = clean_text(time_elem.get_text())
        else:
            data['raw_time'] = ""
        
        # استخراج المؤلف
        author_elem = self._find_first_with_fallback(item, LIST_SELECTORS['author'])
        if author_elem:
            data['author'] = clean_text(author_elem.get_text())
        else:
            data['author'] = "غير معروف"
        
        # استخراج التصنيف
        category_elem = self._find_first_with_fallback(item, LIST_SELECTORS['category'])
        if category_elem:
            data['category'] = clean_text(category_elem.get_text())
        else:
            data['category'] = "عام"
        
        return data
    
    def extract_details_from_page(self, html_content: str) -> Dict[str, Any]:
        """
        استخراج التفاصيل الكاملة من صفحة الطلب
        
        Args:
            html_content (str): محتوى HTML لصفحة التفاصيل
            
        Returns:
            Dict: التفاصيل الكاملة للطلب
        """
        soup = self.parse(html_content)
        details = {}
        
        # استخراج العنوان
        title_elem = self._find_first_with_fallback(soup, DETAIL_SELECTORS['title'])
        details['title'] = clean_text(title_elem.get_text()) if title_elem else ""
        
        # استخراج المحتوى
        content_elem = self._find_first_with_fallback(soup, DETAIL_SELECTORS['content'])
        details['content'] = clean_text(content_elem.get_text()) if content_elem else ""
        
        # استخراج الميزانية
        budget_elem = self._find_first_with_fallback(soup, DETAIL_SELECTORS['budget'])
        if budget_elem:
            budget_text = clean_text(budget_elem.get_text())
            details['budget'] = budget_text
            # محاولة استخراج الرقم من النص
            details['budget_numeric'] = extract_number_from_text(budget_text)
        else:
            details['budget'] = "غير محدد"
            details['budget_numeric'] = None
        
        # استخراج المهارات
        skills_elems = self._find_all_with_fallback(soup, DETAIL_SELECTORS['skills'])
        details['skills'] = [clean_text(elem.get_text()) for elem in skills_elems]
        
        # استخراج المرفقات
        attachments_elems = self._find_all_with_fallback(soup, DETAIL_SELECTORS['attachments'])
        details['attachments'] = [clean_text(elem.get_text()) for elem in attachments_elems]
        
        # استخراج الموعد النهائي
        deadline_elem = self._find_first_with_fallback(soup, DETAIL_SELECTORS['deadline'])
        details['deadline'] = clean_text(deadline_elem.get_text()) if deadline_elem else ""
        
        # استخراج عدد العروض
        proposals_elem = self._find_first_with_fallback(soup, DETAIL_SELECTORS['proposals_count'])
        if proposals_elem:
            proposals_text = clean_text(proposals_elem.get_text())
            details['proposals_count'] = extract_number_from_text(proposals_text)
        else:
            details['proposals_count'] = 0
        
        return details
    
    def extract_pagination_info(self, html_content: str) -> Dict[str, Any]:
        """
        استخراج معلومات الترقيم (Pagination)
        
        Args:
            html_content (str): محتوى HTML للصفحة
            
        Returns:
            Dict: معلومات الترقيم
        """
        soup = self.parse(html_content)
        pagination = {
            'has_next': False,
            'next_url': '',
            'current_page': 1,
            'total_pages': None
        }
        
        # البحث عن زر الصفحة التالية
        next_button = self._find_first_with_fallback(soup, PAGINATION_SELECTORS['next_button'])
        if next_button:
            pagination['has_next'] = True
            pagination['next_url'] = normalize_url(self.base_url, next_button.get('href', ''))
        
        # البحث عن رقم الصفحة الحالية
        current_page_elem = self._find_first_with_fallback(soup, PAGINATION_SELECTORS['current_page'])
        if current_page_elem:
            page_text = clean_text(current_page_elem.get_text())
            page_number = extract_number_from_text(page_text)
            if page_number:
                pagination['current_page'] = page_number
        
        return pagination
    
    def _find_with_fallback(self, soup: BeautifulSoup, selectors: List[str]) -> List:
        """
        البحث باستخدام محددات متعددة مع fallback
        
        Args:
            soup: كائن BeautifulSoup
            selectors: قائمة محددات CSS بالترتيب المفضل
            
        Returns:
            List: قائمة العناصر encontrados
        """
        for selector in selectors:
            try:
                elements = soup.select(selector)
                if elements:
                    return elements
            except Exception:
                continue
        
        return []
    
    def _find_first_with_fallback(self, soup: BeautifulSoup, selectors: List[str]):
        """
        البحث عن أول عنصر باستخدام محددات متعددة مع fallback
        
        Args:
            soup: كائن BeautifulSoup
            selectors: قائمة محددات CSS
            
        Returns:
            أول عنصر تم العثور عليه أو None
        """
        for selector in selectors:
            try:
                element = soup.select_one(selector)
                if element:
                    return element
            except Exception:
                continue
        
        return None
    
    def _find_all_with_fallback(self, soup: BeautifulSoup, selectors: List[str]) -> List:
        """
        البحث عن جميع العناصر باستخدام محددات متعددة مع fallback
        
        Args:
            soup: كائن BeautifulSoup
            selectors: قائمة محددات CSS
            
        Returns:
            List: قائمة العناصر
        """
        all_elements = []
        
        for selector in selectors:
            try:
                elements = soup.select(selector)
                if elements:
                    all_elements.extend(elements)
            except Exception:
                continue
        
        # إزالة التكرارات
        unique_elements = []
        seen = set()
        for elem in all_elements:
            elem_id = id(elem)
            if elem_id not in seen:
                seen.add(elem_id)
                unique_elements.append(elem)
        
        return unique_elements
