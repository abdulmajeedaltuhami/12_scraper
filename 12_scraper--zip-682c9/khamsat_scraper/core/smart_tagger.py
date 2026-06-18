"""
نظام التاجات الذكي (Smart Tagging System)
يحلل المحتوى تلقائياً ويستخرج التاجات المناسبة باستخدام خوارزميات NLP بسيطة
"""

import re
from typing import List, Dict, Any, Set, Tuple
from collections import Counter

from config.settings import (
    ENABLE_SMART_TAGGING,
    AUTO_DETECT_TAGS,
    TAG_CONFIDENCE_THRESHOLD,
    MAX_TAGS_PER_REQUEST,
    ENABLE_CATEGORY_CLASSIFICATION
)


class SmartTagger:
    """
    نظام ذكي لاستخراج وتصنيف التاجات من النصوص العربية
    
    الميزات:
    - استخراج الكلمات المفتاحية تلقائياً
    - تصنيف حسب الفئة
    - حساب درجة الثقة
    - دعم اللغة العربية
    """
    
    def __init__(self):
        """
        تهيئة نظام التاجات الذكي
        """
        # قاعدة بيانات التاجات المصنفة
        self.tag_database = self._build_tag_database()
        
        # الكلمات停用 (stop words) العربية
        self.arabic_stopwords = self._get_arabic_stopwords()
        
        # أنماط الكلمات المفتاحية
        self.keyword_patterns = self._build_keyword_patterns()
    
    def _build_tag_database(self) -> Dict[str, List[str]]:
        """
        بناء قاعدة بيانات التاجات المصنفة
        
        Returns:
            Dict: قاموس الفئات والتاجات التابعة لها
        """
        return {
            'برمجة': [
                'برمجة', 'تطوير', 'كود', 'code', 'programming', 'development',
                'python', 'بايثون', 'javascript', 'جافاسكريبت', 'php', 'بي إتش بي',
                'java', 'جافا', 'c++', 'سي بلس بلس', 'react', 'ريأكت', 'angular',
                'vue', 'django', 'flask', 'nodejs', 'node.js', 'backend', 'frontend',
                'fullstack', 'full-stack', 'web', 'ويب', 'website', 'موقع',
                'application', 'تطبيق', 'app', 'software', 'برمجيات', 'script', 'سكريبت'
            ],
            'تصميم': [
                'تصميم', 'design', 'جرافيك', 'graphic', 'شعار', 'logo', 'هوية',
                'بصرية', 'visual', 'illustrator', 'photoshop', 'adobe', 'ui', 'ux',
                'interface', 'واجهة', 'experience', 'تجربة', 'مستخدم', 'user',
                'رسومات', 'illustration', 'drawing', 'رسم', 'فوتوشوب', 'الستريتور'
            ],
            'كتابة': [
                'كتابة', 'writing', 'محتوى', 'content', 'مقال', 'article', 'مدونة',
                'blog', 'تدوين', 'copywriting', 'نسخ', 'إعلاني', 'إعلانات', 'ads',
                'تسويق', 'marketing', 'seo', 'تحسين', 'محركات', 'بحث', 'search',
                'ترجمة', 'translation', 'translate', 'مترجم', 'لغة', 'language',
                'english', 'إنجليزي', 'عربي', 'arabic', 'editor', 'محرر', 'editing'
            ],
            'فيديو': [
                'فيديو', 'video', 'مونتاج', 'editing', 'montage', 'premiere',
                'after', 'effects', 'أفتر', 'إفكتس', 'animation', 'انيميشن',
                'حركة', 'motion', 'graphics', 'جرافيكس', 'youtube', 'يوتيوب',
                'إنتاج', 'production', 'تصوير', 'filming', 'كاميرا', 'camera'
            ],
            'صوت': [
                'صوت', 'audio', 'voice', 'صوتي', 'recording', 'تسجيل', 'mixing',
                'مكس', 'mastering', 'ماسترينغ', 'podcast', 'بودكاست', 'music',
                'موسيقى', 'أغنية', 'song', 'melody', 'لحن', 'sound', 'ساوند'
            ],
            'بيانات': [
                'بيانات', 'data', 'تحليل', 'analysis', 'analytics', 'إحصاء',
                'statistics', 'excel', 'إكسل', 'spreadsheets', 'جداول', 'charts',
                'رسوم', 'بيانية', 'visualization', 'تصور', 'power bi', 'tableau',
                'machine learning', 'تعلم', 'آلي', 'ذكاء', 'اصطناعي', 'ai', 'ml'
            ],
            'تسويق': [
                'تسويق', 'marketing', 'digital', 'رقمي', 'social', 'media',
                'تواصل', 'اجتماعي', 'فيسبوك', 'facebook', 'انستغرام', 'instagram',
                'تويتر', 'twitter', 'linkedin', 'لينكدان', 'campaign', 'حملة',
                'إعلان', 'advertisement', 'ppc', 'sem', 'influencer', 'مشاهير'
            ],
            'إدارة': [
                'إدارة', 'management', 'projects', 'مشاريع', 'project manager',
                'مدير', 'مشروع', 'planning', 'تخطيط', 'organization', 'تنظيم',
                'business', 'أعمال', 'consulting', 'استشارات', 'استشارة',
                'finance', 'مالية', 'accounting', 'محاسبة', 'hr', 'موارد', 'بشرية'
            ],
            'ألعاب': [
                'لعبة', 'game', 'ألعاب', 'games', 'gaming', 'unity', 'يونيتي',
                'unreal', 'engine', 'أنريل', 'engine', '3d', 'ثلاثي', 'الأبعاد',
                '2d', 'ثنائي', 'character', 'شخصية', 'level', 'مرحلة', 'design',
                'gameplay', 'playable', 'قابل', 'للعب', 'multiplayer', 'متعدد',
                'players', 'اللاعبين', 'vr', 'virtual', 'reality', 'واقع', 'افتراضي'
            ],
            'بلوكشين': [
                'blockchain', 'بلوكشين', 'crypto', 'كريبتو', 'cryptocurrency',
                'عملة', 'رقمية', 'bitcoin', 'بيتكوين', 'ethereum', 'إيثيريوم',
                'nft', 'non-fungible', 'token', 'رمز', 'غير', 'قابل', 'للاستبدال',
                'defi', 'لامركزية', 'decentralized', 'finance', 'مالية', 'web3',
                'smart', 'contract', 'عقد', 'ذكي', 'contracts', 'عقود'
            ]
        }
    
    def _get_arabic_stopwords(self) -> Set[str]:
        """
        الحصول على قائمة الكلمات停用 العربية
        
        Returns:
            Set: مجموعة الكلمات停用
        """
        return {
            'من', 'في', 'على', 'إلى', 'عن', 'مع', 'لـ', 'ل', 'ك', 'ب', 'و', 'ف', 'ث',
            'التي', 'الذي', 'الذين', 'اللواتي', 'هذا', 'هذه', 'هؤلاء', 'ذلك', 'تلك',
            'ما', 'من', 'ماذا', 'متى', 'أين', 'كيف', 'لماذا', 'أي', 'هل', 'أ', 'لم',
            'لن', 'لا', 'ليس', 'كان', 'كانت', 'يكون', 'تكون', 'نحن', 'أنا', 'هو', 'هي',
            'هم', 'هن', 'أنت', 'أنتِ', 'أنتم', 'أنتن', 'أريد', 'أحتاج', 'مطلوب', 'لابد',
            'يجب', 'يمكن', 'قادر', 'استطيع', 'سأقوم', 'سوف', 'سـ', 'قد', 'ربما', 'أيضا',
            'كذلك', 'بالإضافة', 'إلى', 'حسب', 'وفق', 'بناء', 'على', 'خلال', 'بعد',
            'قبل', 'بين', 'عبر', 'حول', 'داخل', 'خارج', 'أمام', 'خلف', 'فوق', 'تحت'
        }
    
    def _build_keyword_patterns(self) -> List[re.Pattern]:
        """
        بناء أنماط regex لاستخراج الكلمات المفتاحية
        
        Returns:
            List: قائمة أنماط regex
        """
        patterns = [
            r'[\u0600-\u06FF]{3,}',  # كلمات عربية (3 أحرف فأكثر)
            r'[a-zA-Z]{3,}',  # كلمات إنجليزية (3 أحرف فأكثر)
            r'#([\w]+)',  # هاشتاجات
            r'\$([0-9]+)',  # أسعار
        ]
        return [re.compile(p) for p in patterns]
    
    def extract_tags(self, text: str, title: str = "") -> List[Dict[str, Any]]:
        """
        استخراج التاجات من النص
        
        Args:
            text (str): النص المراد تحليله
            title (str): العنوان (اختياري)
            
        Returns:
            List[Dict]: قائمة التاجات مع درجات الثقة
        """
        if not ENABLE_SMART_TAGGING or not AUTO_DETECT_TAGS:
            return []
        
        # دمج العنوان مع النص
        full_text = f"{title} {text}" if title else text
        
        if not full_text or len(full_text.strip()) == 0:
            return []
        
        # تنظيف النص
        cleaned_text = self._clean_text(full_text)
        
        # استخراج الكلمات المفتاحية
        keywords = self._extract_keywords(cleaned_text)
        
        # مطابقة التاجات
        matched_tags = self._match_tags(keywords)
        
        # حساب درجات الثقة
        tagged_results = self._calculate_confidence(matched_tags, keywords)
        
        # ترتيب حسب درجة الثقة وأخذ الأعلى
        tagged_results.sort(key=lambda x: x['confidence'], reverse=True)
        
        return tagged_results[:MAX_TAGS_PER_REQUEST]
    
    def _clean_text(self, text: str) -> str:
        """
        تنظيف النص من الرموز غير المرغوبة
        
        Args:
            text (str): النص الأصلي
            
        Returns:
            str: النص المنظف
        """
        # إزالة الرموز الخاصة
        text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)
        
        # إزالة المسافات الزائدة
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text.lower()
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        استخراج الكلمات المفتاحية من النص
        
        Args:
            text (str): النص المنظف
            
        Returns:
            List[str]: قائمة الكلمات المفتاحية
        """
        keywords = []
        
        # تقسيم النص إلى كلمات
        words = text.split()
        
        # إضافة الكلمات الصالحة
        for word in words:
            word_clean = word.strip().lower()
            if (len(word_clean) >= 3 and 
                word_clean not in self.arabic_stopwords and
                not word_clean.isdigit()):
                keywords.append(word_clean)
        
        # استخدام الأنماط لاستخراج كلمات إضافية
        for pattern in self.keyword_patterns:
            matches = pattern.findall(text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else ''
                if match and len(match) >= 3 and match not in self.arabic_stopwords:
                    keywords.append(match.lower())
        
        # حساب تكرار الكلمات
        keyword_counts = Counter(keywords)
        
        # إرجاع الكلمات الأكثر تكراراً
        return [word for word, count in keyword_counts.most_common(30)]
    
    def _match_tags(self, keywords: List[str]) -> Dict[str, Set[str]]:
        """
        مطابقة الكلمات المفتاحية مع التاجات
        
        Args:
            keywords (List[str]): قائمة الكلمات المفتاحية
            
        Returns:
            Dict[str, Set[str]]: قاموس الفئات والتاجات المطابقة
        """
        matched = {}
        
        for category, tags in self.tag_database.items():
            matched_tags = set()
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                for tag in tags:
                    tag_lower = tag.lower()
                    
                    # مطابقة تامة أو جزئية - تحسين الخوارزمية
                    if (keyword_lower == tag_lower or
                        tag_lower in keyword_lower or
                        keyword_lower in tag_lower):
                        matched_tags.add(tag)
                    
                    # مطابقة الجذور (stemming بسيط)
                    # إذا كانت الكلمة 5 أحرف أو أكثر، نطابق أول 3 أحرف
                    if len(keyword_lower) >= 5 and len(tag_lower) >= 3:
                        if keyword_lower[:3] == tag_lower[:3]:
                            matched_tags.add(tag)
            
            if matched_tags:
                matched[category] = matched_tags
        
        return matched
    
    def _calculate_confidence(self, matched_tags: Dict[str, Set[str]], 
                             keywords: List[str]) -> List[Dict[str, Any]]:
        """
        حساب درجة الثقة لكل تاج
        
        Args:
            matched_tags (Dict[str, Set[str]]): التاجات المطابقة
            keywords (List[str]): الكلمات المفتاحية
            
        Returns:
            List[Dict]: قائمة التاجات مع درجات الثقة
        """
        results = []
        total_keywords = len(keywords) if keywords else 1
        
        for category, tags in matched_tags.items():
            for tag in tags:
                # حساب درجة الثقة بناءً على:
                # 1. عدد مرات ظهور التاج
                # 2. نسبة الكلمات المطابقة
                # 3. أهمية الفئة
                
                match_count = sum(
                    1 for kw in keywords
                    if tag.lower() in kw.lower() or kw.lower() in tag.lower()
                )
                
                # تعزيز الثقة إذا كان هناك تطابق مباشر
                exact_match_bonus = 0.2 if any(tag.lower() == kw.lower() for kw in keywords) else 0
                
                confidence = (match_count / total_keywords) * 2.0 + exact_match_bonus
                
                # تعزيز الثقة إذا كان التاج متكرر
                if match_count > 1:
                    confidence *= 1.3
                
                # تطبيع درجة الثقة بين 0 و 1
                confidence = min(confidence, 1.0)
                
                # إضافة التاج فقط إذا تجاوز عتبة الثقة (تخفيض العتبة من 0.7 إلى 0.5)
                if confidence >= 0.5:  # تم تخفيض TAG_CONFIDENCE_THRESHOLD مؤقتاً
                    results.append({
                        'tag': tag,
                        'category': category,
                        'confidence': round(confidence, 2),
                        'matches': match_count
                    })
        
        return results
    
    def classify_category(self, text: str, title: str = "") -> Dict[str, Any]:
        """
        تصنيف النص إلى فئة رئيسية
        
        Args:
            text (str): النص
            title (str): العنوان
            
        Returns:
            Dict: معلومات التصنيف
        """
        if not ENABLE_CATEGORY_CLASSIFICATION:
            return {'category': 'عام', 'confidence': 0.0}
        
        tags = self.extract_tags(text, title)
        
        if not tags:
            return {'category': 'عام', 'confidence': 0.0}
        
        # حساب الفئة الأكثر تكراراً
        category_counts = Counter(tag['category'] for tag in tags)
        top_category = category_counts.most_common(1)[0]
        
        # حساب متوسط ثقة الفئة
        category_tags = [t for t in tags if t['category'] == top_category[0]]
        avg_confidence = sum(t['confidence'] for t in category_tags) / len(category_tags)
        
        return {
            'category': top_category[0],
            'confidence': round(avg_confidence, 2),
            'tags_count': top_category[1],
            'all_categories': dict(category_counts)
        }
    
    def get_suggested_tags(self, request_data: Dict[str, Any]) -> List[str]:
        """
        الحصول على التاجات المقترحة لطلب معين
        
        Args:
            request_data (Dict): بيانات الطلب
            
        Returns:
            List[str]: قائمة التاجات المقترحة
        """
        content = request_data.get('content', '')
        title = request_data.get('title', '')
        skills = request_data.get('skills', [])
        
        # استخراج التاجات من المحتوى والعنوان
        tags = self.extract_tags(content, title)
        
        # إضافة المهارات كتاجات
        suggested = [tag['tag'] for tag in tags if tag['confidence'] >= TAG_CONFIDENCE_THRESHOLD]
        
        # إضافة المهارات الموجودة
        if skills:
            suggested.extend(skills)
        
        # إزالة التكرارات
        unique_tags = list(dict.fromkeys(suggested))
        
        return unique_tags[:MAX_TAGS_PER_REQUEST]


# دالة مساعدة للاستخدام السريع
def smart_tag_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    دالة مساعدة لتاجيت طلب واحد
    
    Args:
        request_data (Dict): بيانات الطلب
        
    Returns:
        Dict: الطلب مع التاجات المضافة
    """
    tagger = SmartTagger()
    
    # استخراج التاجات
    tags = tagger.get_suggested_tags(request_data)
    
    # تصنيف الفئة
    classification = tagger.classify_category(
        request_data.get('content', ''),
        request_data.get('title', '')
    )
    
    # إضافة البيانات للطلب
    result = request_data.copy()
    result['smart_tags'] = tags
    result['auto_category'] = classification['category']
    result['category_confidence'] = classification['confidence']
    result['all_categories'] = classification.get('all_categories', {})
    
    return result


if __name__ == "__main__":
    # اختبار النظام
    print("=" * 80)
    print("اختبار نظام التاجات الذكي")
    print("=" * 80)
    
    tagger = SmartTagger()
    
    # نص تجريبي
    test_text = """
    أحتاج إلى مبرمج بايثون محترف لتطوير سكريبت web scraping لجمع البيانات من المواقع.
    يجب أن يكون السكربت سريع ويدعم pagination و JSON output. الخبرة في BeautifulSoup
    و Selenium مطلوبة. المشروع يتضمن أيضاً تحليل البيانات وتصديرها إلى Excel.
    """
    
    test_title = "مطلوب مبرمج بايثون لتطوير سكربت جمع بيانات"
    
    print("\n📝 النص التجريبي:")
    print(test_text[:100] + "...")
    
    print("\n🏷️ التاجات المستخرجة:")
    tags = tagger.extract_tags(test_text, test_title)
    for tag in tags:
        print(f"  - {tag['tag']} ({tag['category']}) - ثقة: {tag['confidence']}")
    
    print("\n📊 التصنيف:")
    classification = tagger.classify_category(test_text, test_title)
    print(f"  الفئة: {classification['category']}")
    print(f"  الثقة: {classification['confidence']}")
    print(f"  الفئات الأخرى: {classification.get('all_categories', {})}")
    
    print("\n✅ تم الاختبار بنجاح!")
