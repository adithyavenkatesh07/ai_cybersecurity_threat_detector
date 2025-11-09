import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import socket
from collections import Counter
import time
from textblob import TextBlob

class URLAnalyzer:
    def __init__(self):
        self.suspicious_keywords = [
            'login', 'verify', 'account', 'update', 'secure', 'banking',
            'paypal', 'amazon', 'signin', 'confirm', 'suspended'
        ]

    def analyze(self, url):
        """
        Analyzes a URL to extract a comprehensive set of features, including
        SEO metrics, performance data, and content analysis.
        """
        start_time = time.time()
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            page_load_time = time.time() - start_time
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Basic URL features
            base_features = {
                'url_length': len(url),
                'has_ip': self._has_ip_address(url),
                'has_suspicious_keywords': self._check_suspicious_keywords(url),
                'subdomain_count': self._count_subdomains(url),
                'has_https': url.startswith('https://'),
                'domain_age': self._estimate_domain_age(url),
                'special_char_count': self._count_special_chars(url),
                'has_redirect': self._check_redirects(url)
            }
            
            # Advanced content and SEO analysis
            content_analysis = self._analyze_content(soup, url)
            
            # Performance metrics
            performance_metrics = self._analyze_performance(response, page_load_time)
            
            # Combine all data
            features = {
                **base_features,
                **content_analysis,
                **performance_metrics
            }
            
            return features

        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return {'error': str(e)}

    def _analyze_content(self, soup, base_url):
        """
        Analyzes the HTML content of a page for SEO and content metrics.
        """
        text = soup.get_text(separator=' ', strip=True)
        words = text.lower().split()
        word_count = len(words)
        
        # SEO Metrics
        headings = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}
        internal_links, external_links = self._analyze_links(soup, base_url)
        
        # Content Analysis
        sentiment = TextBlob(text).sentiment
        readability = self._calculate_readability(text) # Simplified
        
        # Keyword Density
        keyword_density = self._calculate_keyword_density(words)
        
        return {
            'seo_metrics': {
                'heading_counts': headings,
                'internal_links': internal_links,
                'external_links': external_links,
                'keyword_density': keyword_density[:10] # Top 10 keywords
            },
            'content_analysis': {
                'word_count': word_count,
                'sentiment': {
                    'polarity': sentiment.polarity,
                    'subjectivity': sentiment.subjectivity
                },
                'readability_score': readability
            }
        }

    def _analyze_links(self, soup, base_url):
        internal_count = 0
        external_count = 0
        base_netloc = urlparse(base_url).netloc
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
                continue
            
            parsed_href = urlparse(href)
            if parsed_href.netloc and parsed_href.netloc != base_netloc:
                external_count += 1
            else:
                internal_count += 1
                
        return internal_count, external_count

    def _calculate_readability(self, text):
        # Flesch-Kincaid reading ease (simplified version)
        sentences = text.count('.') + text.count('!') + text.count('?')
        words = len(text.split())
        if sentences == 0 or words == 0:
            return 0
        
        return 206.835 - 1.015 * (words / sentences)
    
    def _calculate_keyword_density(self, words):
        # Exclude common stop words
        stop_words = set(['the', 'a', 'and', 'is', 'in', 'it', 'of', 'for', 'on'])
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        word_counts = Counter(filtered_words)
        
        total_words = len(filtered_words)
        if total_words == 0:
            return []
            
        density = [{'keyword': k, 'count': v, 'density': (v / total_words) * 100} for k, v in word_counts.most_common(20)]
        return density
        
    def _analyze_performance(self, response, page_load_time):
        """
        Analyzes performance-related metrics from the HTTP response.
        """
        total_size_kb = len(response.content) / 1024
        
        # This is a simplified asset size calculation.
        # A full implementation would require parsing CSS/JS for more resources.
        asset_sizes = {
            'html_kb': total_size_kb, # Approximation
            'images_kb': 0, # Requires parsing and fetching images
            'css_kb': 0,
            'js_kb': 0
        }
        
        return {
            'performance_metrics': {
                'page_load_time_s': round(page_load_time, 2),
                'total_page_size_kb': round(total_size_kb, 2),
                'asset_size_distribution_kb': asset_sizes
            }
        }
        
    def _has_ip_address(self, url):
        pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        return bool(re.search(pattern, url))
    
    def _check_suspicious_keywords(self, url):
        url_lower = url.lower()
        return any(keyword in url_lower for keyword in self.suspicious_keywords)
    
    def _count_subdomains(self, url):
        parsed = urlparse(url)
        domain = parsed.netloc
        return domain.count('.') - 1 if domain.count('.') > 1 else 0
    
    def _estimate_domain_age(self, url):
        # Simplified - in production, use WHOIS lookup
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            # Return estimated age (0 = new, 1 = old)
            return 1 if len(domain) > 0 else 0
        except:
            return 0
    
    def _count_special_chars(self, url):
        special_chars = ['@', '?', '-', '=', '.', '#', '%', '+', '$', '!', '*', ',', '//']
        return sum(url.count(char) for char in special_chars)
    
    def _check_redirects(self, url):
        try:
            response = requests.get(url, timeout=5, allow_redirects=False)
            return response.status_code in [301, 302, 303, 307, 308]
        except:
            return False