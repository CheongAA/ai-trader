from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import os

class ChartImageCollector:
    def __init__(self, exchange, save_dir="screenshot"):
        """
        차트 이미지 수집기 초기화
        
        Args:
            save_dir (str): 스크린샷을 저장할 디렉토리 경로
        """
        self.save_dir = save_dir
        self.exchange = exchange
        self._init_chrome_options()
        self._ensure_save_directory()
    
    def _init_chrome_options(self):
        """Chrome 브라우저 옵션 초기화"""
        self.chrome_options = Options()
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--force-device-scale-factor=1')
        self.chrome_options.add_argument('--start-maximized')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
    
    def _ensure_save_directory(self):
        """저장 디렉토리 존재 확인 및 생성"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            print(f"'{self.save_dir}' 폴더가 생성되었습니다.")
    
    def _init_driver(self):
        """웹드라이버 초기화"""
        return webdriver.Chrome(options=self.chrome_options)
    
    def _generate_filename(self, prefix="chart", interval="1hour"):
        """
        파일명 생성
        
        Args:
            prefix (str): 파일명 접두사
            interval (str): 차트 간격 (예: "1hour", "4hour", "1day")
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.save_dir, f"{prefix}_{interval}_{timestamp}.png")
    
    
    def _wait_for_element(self, driver, by, value, timeout=10):
        """
        요소 대기
        
        Args:
            driver: 웹드라이버 인스턴스
            by: 요소를 찾을 방법 (By.ID, By.XPATH 등)
            value: 찾을 요소의 값
            timeout: 대기 시간 (초)
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))
    
    def capture_chart(self, wait_time):
        """
        차트 캡처
        
        Args:
            url (str): 차트 페이지 URL
            xpath_list (str[]): 클릭 액션이 실행되는 xpath 리스트
            wait_time (int): 페이지 로딩 대기 시간 (초)
        
        Returns:
            str: 저장된 파일 경로
        """
        driver = self._init_driver()
        
        try:
            # 페이지 로딩
            driver.get(self.exchange.get_url())
            time.sleep(wait_time)
            
            # xpath 리스트의 각 요소에 대해 클릭 실행
            for xpath in self.exchange.get_chart_xpath_list():
                try:
                    element = driver.find_element(By.XPATH, xpath)
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    element.click()
                    time.sleep(wait_time)

                except Exception as click_error:
                    print(f"XPath '{xpath}' 클릭 중 에러 발생: {str(click_error)}")
                    continue

            # 스크린샷 저장
            filename = self._generate_filename()
            driver.save_screenshot(filename)
            print(f"차트가 성공적으로 저장되었습니다: {filename}")
            
            return filename
            
        except Exception as e:
            print(f"에러가 발생했습니다: {str(e)}")
            return None
            
        finally:
            driver.quit()
